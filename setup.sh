#!/bin/bash

echo "🧠 Starting setup of the virtual environment for AI Session MVP..."

if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

echo "📦 Creating virtual environment .venv..."
python3 -m venv .venv

echo "⚙️ Activating virtual environment..."
source .venv/bin/activate

echo "🔍 Checking required environment variables..."

missing_env=false

if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating one..."
    touch .env
fi

set -o allexport
source .env
set +o allexport

for var in OPENAI_API_KEY SESSION_CODE
do
    if [ -z "${!var}" ]; then
        echo "⚠️  Missing environment variable: $var"
        read -p "Please enter a value for $var: " input_value
        while [ -z "$input_value" ]; do
            read -p "❗ Value for $var cannot be empty. Try again: " input_value
        done

        export "$var=$input_value"

        # Replace if it exists, if not, append to the end
        if grep -q "^$var=" .env; then
            sed -i '' -e "s/^$var=.*/$var=$input_value/" .env 2>/dev/null || \
            sed -i "s/^$var=.*/$var=$input_value/" .env
        else
            echo "$var=$input_value" >> .env
        fi
    fi

    if [ -z "${!var}" ]; then
        echo "⚠️  Still missing: $var"
        missing_env=true
    fi
done

if $missing_env; then
    echo "❌ Please provide all required variables."
    exit 1
else
    echo "✅ All environment variables are set."
fi

echo "🧪 Checking operating system dependencies..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🔧 macOS detected."
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew is not installed. Install it from https://brew.sh/"
    else
        echo "📦 Checking portaudio..."
        brew list portaudio &> /dev/null || brew install portaudio
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🔧 Linux detected."
    sudo apt update
    sudo apt install -y portaudio19-dev python3-pyaudio scrot
else
    echo "⚠️ Operating system not automatically supported. Install dependencies manually."
fi

echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete. You can start the system with:"
echo "   ./run.sh"
