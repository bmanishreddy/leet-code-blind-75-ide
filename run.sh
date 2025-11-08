#!/bin/bash
# Startup script for LeetCode Blind 75 IDE

echo "🚀 Starting LeetCode Blind 75 IDE..."
echo ""

# Check if questions.json exists
if [ ! -f "questions.json" ]; then
    echo "📝 Initializing questions database..."
    python3 questions_init.py
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "✅ Starting server..."
echo "🌐 Open http://localhost:5000 in your browser"
echo ""

python3 app.py

