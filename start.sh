#!/bin/bash

# Start LeetCode Blind 75 IDE with Apple Silicon GPU acceleration

echo "🚀 Starting LeetCode Blind 75 IDE"
echo "=================================="
echo ""
echo "Features:"
echo "  ✅ 75 LeetCode problems categorized by topic"
echo "  ✅ AI-powered hints using Llama-2-7B"
echo "  ✅ Apple Silicon GPU acceleration (Metal)"
echo "  ✅ Code editor with syntax highlighting"
echo "  ✅ Instant test runner"
echo ""
echo "Server will start at: http://127.0.0.1:5000"
echo ""
echo "Note: LLM loads lazily on first hint request (~10-15 seconds)"
echo "      Subsequent hints will be instant!"
echo ""

cd "$(dirname "$0")"
python3 app.py

