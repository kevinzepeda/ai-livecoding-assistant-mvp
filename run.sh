#!/bin/bash

echo "🚀 Starting AI Livecoding Session system..."

if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

source .venv/bin/activate
echo "✅ Virtual environment activated."

echo "🌐 Starting FastAPI backend..."
uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!

sleep 2

echo "🔍 Checking backend status..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$STATUS" = "200" ]; then
    echo "✅ Backend is running correctly."
else
    echo "❌ Backend is not responding correctly (status code: $STATUS)."
    kill $BACKEND_PID
    exit 1
fi

echo "🎥 Starting audio and screen capture..."
python utils/screen_audio_capture.py

echo "🛑 Stopping backend..."
kill $BACKEND_PID
echo "✅ System shut down correctly."
