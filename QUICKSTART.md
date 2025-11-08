# 🚀 LeetCode Blind 75 IDE - Quick Start

## Start the IDE

### Option 1: Use the startup script (recommended)
```bash
./start.sh
```

### Option 2: Direct Python
```bash
python3 app.py
```

The server will start at: **http://127.0.0.1:5000**

---

## Features

### ✅ 75 LeetCode Problems
- Organized by category (Arrays, Strings, Trees, Graphs, DP, etc.)
- Difficulty badges (Easy, Medium, Hard)
- Full problem descriptions and test cases

### 🧠 AI-Powered Hints
- **RAG-based system** using 75+ problem solutions
- **Llama-2-7B LLM** running locally on your Mac
- **Apple Silicon GPU acceleration** (Metal) for fast inference
- **Context-aware hints** that read your current code

### 💡 Three Types of Hints
1. **General** (💡) - High-level approach and patterns
2. **Specific** (🎯) - Implementation details based on your progress
3. **Next Step** (📝) - Exact next line/block of code to write

### ⚡ Code Editor
- Syntax highlighting
- Auto-completion
- Instant test runner

---

## How It Works

### 1. Select a Problem
Click any problem from the sidebar (categorized by topic)

### 2. Write Your Code
Use the built-in editor with syntax highlighting

### 3. Get Intelligent Hints
- **First hint**: Takes ~10-15 seconds (LLM loads on-demand with GPU)
- **Subsequent hints**: Instant (<1 second)
- The AI reads your code and gives contextual advice

### 4. Run Tests
Click "▶ Run Tests" to validate your solution

---

## Apple Silicon GPU Acceleration

The IDE automatically detects your Apple Silicon chip and uses **Metal GPU acceleration**:

- **M1/M2/M3 Macs**: All 35 model layers run on GPU
- **Intel Macs**: Falls back to CPU
- **Performance**: 10-20x faster inference on Apple Silicon!

You'll see this message when LLM loads:
```
🚀 Apple Silicon detected! Using Metal GPU acceleration (35 layers)
```

---

## Tips

### Getting Better Hints
1. **Write some code first** - AI gives better hints when it can analyze your progress
2. **Use different hint types**:
   - Stuck on approach? → **General hint**
   - Know approach but not implementation? → **Specific hint**
   - Mid-coding and need next step? → **Next Step hint**

### Performance
- **First hint**: ~10-15 seconds (one-time LLM loading)
- **After that**: Instant hints (<1 second)
- **Lazy loading**: LLM only loads when you click "Get Hint"

### Resizable UI
- Drag the edges of any panel to resize
- Panel sizes are saved automatically
- Customize your workspace!

---

## Troubleshooting

### Server won't start?
```bash
# Check if port 5000 is in use
lsof -ti:5000 | xargs kill -9

# Restart
./start.sh
```

### LLM not loading?
Check that the model file exists:
```bash
ls -lh ~/Desktop/Coding/cortex-sdk/Chat_bot/rag_model/foundation_model/llama-2-7b-chat-hf-q2_k.gguf
```

### Hints are slow?
- **First hint**: Expected (LLM loading)
- **All hints slow**: Check if GPU acceleration is enabled in terminal output

---

## System Requirements

- **macOS**: 11.0+ (Big Sur or later)
- **Python**: 3.8+
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 3GB for model file
- **Apple Silicon**: M1/M2/M3 for GPU acceleration (optional)

---

## Dependencies

Install all required packages:
```bash
pip install flask llama-cpp-python --break-system-packages
```

---

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running

Or kill it manually:
```bash
pkill -f "python.*app.py"
```

---

## Next Steps

1. Open http://127.0.0.1:5000
2. Pick a problem (try "Two Sum" for easy start)
3. Write some code
4. Click "💡 Get Hint"
5. Complete the solution!

Happy coding! 🎉

