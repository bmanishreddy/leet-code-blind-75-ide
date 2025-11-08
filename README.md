# LeetCode Blind 75 IDE

A web-based IDE for practicing LeetCode Blind 75 problems with built-in test execution, hints, solutions, and algorithm visualizations.

## Features

- **78 Blind 75 Problems** - All problems pre-loaded with descriptions, examples, and test cases
- **Code Editor** - Syntax highlighting with CodeMirror
- **Run Tests** - Execute your code against test cases instantly
- **AI Hints** - Get hints using local Deepseek-Coder-1.3B LLM
- **Show Solution** - View optimal solutions with explanations
- **Algorithm Visualizations** - Step-by-step visual diagrams for all 78 problems
- **Progress Tracking** - Track how many times you've solved each problem
- **Keyboard Shortcuts** - Fast navigation and execution

## Quick Start with Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/bmanishreddy/leet-code-blind-75-ide.git
cd leet-code-blind-75-ide
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

3. Open browser:
```
http://localhost:5000
```

That's it! The app will be running in a container.

### Docker Commands

```bash
# Start the app
docker-compose up

# Start in background
docker-compose up -d

# Stop the app
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose up --build
```

## Manual Setup (Without Docker)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Open browser:
```
http://localhost:5000
```

## Usage

1. Select a problem from the left sidebar
2. Write your solution in the code editor
3. Click "Run Tests" to check your code
4. Use "Get Hint" if you're stuck
5. Click "Show Solution" to see the optimal approach
6. Try "Visualize Algorithm" to see how it works step-by-step

## Keyboard Shortcuts

- `Cmd/Ctrl + Enter` - Run Tests
- `Cmd/Ctrl + E` - Execute Code
- `Cmd/Ctrl + R` - Reset Code
- `Cmd/Ctrl + H` - Toggle Hints

## Project Structure

```
leet_code_blind_75_ide/
├── app.py                      # Flask backend
├── rag_hint_system.py          # Hint generation system
├── visualizations.py           # Hardcoded visualizations
├── knowledge_base.json         # Solutions and explanations
├── questions.json              # Problem definitions
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker orchestration
├── models/
│   └── deepseek-coder-1.3b-instruct.Q4_K_M.gguf
├── templates/
│   └── index.html              # Main UI
└── static/
    ├── css/
    │   ├── style.css
    │   └── resize.css
    └── js/
        ├── app.js
        └── resize.js
```

## LLM Model

The app uses Deepseek-Coder-1.3B for hint generation. The model is loaded lazily (only when you click "Get Hint" for the first time).

Model location: `models/deepseek-coder-1.3b-instruct.Q4_K_M.gguf`

If you don't have the model, hints will use fallback descriptions from the knowledge base.

## Test Cases

All problems have test cases. When you run tests:
- Your code is executed in a sandboxed environment
- Results show expected vs actual output
- Console output is captured and displayed
- Time complexity is shown in solutions

## Visualizations

Every problem has a custom ASCII visualization showing:
- Step-by-step algorithm execution
- Pointer movements (for two-pointer problems)
- State changes (for DP, hash maps, stacks)
- Array/tree traversals
- Time and space complexity

Examples: Two Sum, Binary Search, Climbing Stairs, Valid Parentheses, etc.

## Technical Details

- **Backend**: Flask (Python 3.10+)
- **Frontend**: Vanilla JavaScript, CodeMirror
- **LLM**: Deepseek-Coder-1.3B (via llama-cpp-python)
- **Container**: Docker with Python 3.10-slim base
- **Port**: 5000

## Notes

- Code execution has a 10-second timeout
- Only Python is supported currently
- Test cases run against your `Solution` class
- Success tracking is stored in browser localStorage
- Docker setup includes hot-reload for development

## License

Educational use only.
