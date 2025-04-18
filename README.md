# 🧠 Multiagent AI Session System — MVP

This project allows you to start live interaction sessions with an intelligent agent that receives screenshots and voice transcriptions. Ideal for LiveCoding sessions, debugging, or remote assistance.

## 📦 General Requirements

- Python 3.9+
- Modern browser
- Terminal access
- On macOS: screen and microphone recording permissions enabled for the terminal

## 📁 Structure

```
.
├── backend/
├── frontend/
├── utils/
│   └── screen_audio_capture.py
├── requirements.txt
├── run.sh
├── setup.sh
└── README.md
```

---

## 🛠️ Setting up the virtual environment

1. Clone the repository:

```bash
git clone https://github.com/kevinzepeda/ai-livecoding-assistant-mvp.git
cd ai-livecode-assistant-mvp
```

2. Activate the environment:

- On **Linux/macOS**:

```bash
chmod +x setup.sh && ./setup.sh
```

- On **Windows**:

> ⚠️ **Note:** This project has not been tested or made available for Windows at this time. It is recommended to use a Linux-based or macOS operating system.

---

## 🖥️ System-specific Requirements

### macOS

Install `portaudio` to record audio:

```bash
brew install portaudio
pip install pyaudio
```

Make sure Terminal (or the app you're using) has permissions in:

- **System Preferences → Security & Privacy → Microphone**
- **System Preferences → Security & Privacy → Screen Recording**

### Linux

Make sure the following dependencies are installed:

```bash
sudo apt update
sudo apt install portaudio19-dev python3-pyaudio scrot
```

---

## 🔧 Required Environment Variables

Create a `.env` file or export these variables in your system:

```bash
OPENAI_API_KEY=your_openai_key
SESSION_CODE=demo123
```

---

## 🚀 How to run screen and audio capture

From a terminal, with the virtual environment activated:

```bash
chmod +x run.sh && ./run.sh
```

Press and hold `F12` to start recording. When released, the transcription and screenshot will be automatically sent to the backend.

---

## 💡 General System Logic

1. Press `F12`.
2. Audio recording starts.
3. When `F12` is released:
   - The screen is captured.
   - Audio is saved.
   - Transcription is generated (using local Whisper or API).
   - Image + text are sent via WebSocket.
   - The backend forwards the messages to the frontend in real time.
4. You can open the session from a mobile or desktop browser to view the conversation ChatGPT-style.

---

## ✨ Coming Soon

- "Always listening" mode
- Multi-agent support and automatic context classification
- Session admin interface