import os
import io
import threading
import time
import base64
import json
import requests
from pathlib import Path
from datetime import datetime

import pyaudio
import wave
import whisper
import pyautogui
from pynput import keyboard
from PIL import Image
import websockets
import asyncio

# Configuration
USE_LOCAL_WHISPER = True  # Try to use local model
WHISPER_MODEL_NAME = "small"  # base | small | medium
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SESSION_CODE = os.getenv("SESSION_CODE", "demo123")
WS_URL = f"ws://localhost:8000/ws/session/{SESSION_CODE}"
AUDIO_FILENAME = "output.wav"
DURATION_LIMIT = 30  # maximum seconds per recording

def capture_screen():
    image = pyautogui.screenshot()
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        return output.getvalue()

def record_audio(filename, stop_event):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    frames = []
    start_time = time.time()

    while not stop_event.is_set() and (time.time() - start_time) < DURATION_LIMIT:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename):
    try:
        if USE_LOCAL_WHISPER:
            model = whisper.load_model(WHISPER_MODEL_NAME)
            result = model.transcribe(filename)
            return result["text"]
        else:
            raise Exception("Forzando fallback")
    except Exception as e:
        print(f"[Whisper local error]: {e}, usando API de OpenAI...")
        with open(filename, 'rb') as f:
            audio_data = f.read()
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"file": (filename, audio_data, "audio/wav")},
            data={"model": "whisper-1"}
        )
        return response.json().get("text", "")

async def send_to_ws(image_data, transcription):
    async with websockets.connect(WS_URL) as ws:
        message = {
            "type": "user_input",
            "image": base64.b64encode(image_data).decode(),
            "transcription": transcription,
            "timestamp": datetime.utcnow().isoformat()
        }
        await ws.send(json.dumps(message))
        print("[WS] Enviado al backend.")

def on_press(key):
    if key == keyboard.Key.f12 and not on_press.recording:
        print("[F12] Iniciando grabación...")
        on_press.recording = True
        on_press.stop_event = threading.Event()
        on_press.audio_thread = threading.Thread(target=record_audio, args=(AUDIO_FILENAME, on_press.stop_event))
        on_press.audio_thread.start()

def on_release(key):
    if key == keyboard.Key.f12 and on_press.recording:
        print("[F12] Finalizando grabación...")
        on_press.stop_event.set()
        on_press.audio_thread.join()
        on_press.recording = False

        screen = capture_screen()
        transcription = transcribe_audio(AUDIO_FILENAME)

        asyncio.run(send_to_ws(screen, transcription))

on_press.recording = False
on_press.stop_event = None
on_press.audio_thread = None

def start_capture_loop():
    print("🔴 Presiona F12 para iniciar una captura. Vuelve a presionar para terminar.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    start_capture_loop()
