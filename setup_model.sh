#!/bin/bash
# Automatic model downloader for LeetCode Blind 75 IDE

MODEL_DIR="models"
MODEL_FILE="deepseek-coder-1.3b-instruct.Q4_K_M.gguf"
MODEL_URL="https://huggingface.co/TheBloke/deepseek-coder-1.3b-instruct-GGUF/resolve/main/deepseek-coder-1.3b-instruct.Q4_K_M.gguf"
MODEL_PATH="$MODEL_DIR/$MODEL_FILE"

echo "🤖 LeetCode Blind 75 IDE - Model Setup"
echo "========================================"
echo ""

# Create models directory
if [ ! -d "$MODEL_DIR" ]; then
    echo "📁 Creating models directory..."
    mkdir -p "$MODEL_DIR"
fi

# Check if model already exists
if [ -f "$MODEL_PATH" ]; then
    SIZE=$(du -h "$MODEL_PATH" | cut -f1)
    echo "✅ Model already exists ($SIZE)"
    echo "   Location: $MODEL_PATH"
    echo ""
    read -p "Re-download? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ Using existing model"
        exit 0
    fi
fi

# Download model
echo "📥 Downloading Deepseek-Coder-1.3B (833MB)..."
echo "   From: HuggingFace"
echo "   To: $MODEL_PATH"
echo ""
echo "⏳ This may take 2-5 minutes depending on your connection..."
echo ""

if command -v curl &> /dev/null; then
    curl -L --progress-bar -o "$MODEL_PATH" "$MODEL_URL"
elif command -v wget &> /dev/null; then
    wget --show-progress -O "$MODEL_PATH" "$MODEL_URL"
else
    echo "❌ Error: Neither curl nor wget found"
    echo "   Please install curl or wget and try again"
    exit 1
fi

# Verify download
if [ -f "$MODEL_PATH" ]; then
    SIZE=$(du -h "$MODEL_PATH" | cut -f1)
    echo ""
    echo "✅ Download complete!"
    echo "   File: $MODEL_PATH"
    echo "   Size: $SIZE"
    echo ""
    echo "🎉 Setup complete! Run 'python3 app.py' to start the IDE"
else
    echo ""
    echo "❌ Download failed. Please try again or download manually:"
    echo "   $MODEL_URL"
    exit 1
fi

