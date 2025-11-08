# LeetCode Blind 75 IDE

An interactive IDE for learning LeetCode Blind 75 questions with AI-powered hints using a local LLM.

## Features

- 🎯 **Curated Blind 75 Questions**: Pre-loaded with popular LeetCode problems
- 💡 **AI-Powered Hints**: Get contextual hints using a local Llama-2-7B model
- ✏️ **Code Editor**: Syntax-highlighted Python code editor
- ✅ **Test Runner**: Run your code against test cases with instant feedback
- 📊 **Progress Tracking**: Track your progress on each question
- 🎨 **Modern UI**: Dark theme interface optimized for coding

## Requirements

- Python 3.8+
- Flask
- llama-cpp-python (for LLM hints)
- The Llama model file (llama-2-7b-chat-hf-q2_k.gguf)

## Setup

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Ensure the LLM model is available:**

The IDE expects the model at:
```
/Users/manishb/Desktop/Coding/cortex-sdk/Chat_bot/rag_model/foundation_model/llama-2-7b-chat-hf-q2_k.gguf
```

If your model is in a different location, update the `model_path` variable in `app.py`.

3. **Initialize questions database:**

```bash
python questions_init.py
```

This will create a `questions.json` file with initial Blind 75 questions.

4. **Run the application:**

```bash
python app.py
```

5. **Open in browser:**

Navigate to `http://localhost:5000`

## Usage

1. **Select a Question**: Click on any question from the sidebar to load it
2. **Write Code**: Use the code editor to write your solution
3. **Get Hints**: Click "Get Hint" for AI-powered hints (General, Specific, or Next Step)
4. **Run Tests**: Click "Run Tests" to execute your code against test cases
5. **View Results**: See test results in the results panel

## Questions Database

The IDE includes **78 LeetCode Blind 75 problems** organized by:
- **Easy**: 21 problems (Two Pointers, Hash Tables, Arrays, Trees, etc.)
- **Medium**: 52 problems (DP, Graphs, Backtracking, Binary Search, etc.)
- **Hard**: 5 problems (Advanced algorithms)

All problems are organized by category groups:
- Two Pointers & Sliding Window
- Hash Table / Set
- Stack / Monotonic Stack
- Binary Search
- Tree / Binary Tree
- Graph / BFS / DFS
- Backtracking
- Dynamic Programming
- Arrays / Matrix
- Intervals
- Design
- And more...

## Question Structure

Each question includes:
- Title and description
- Difficulty level (Easy/Medium/Hard)
- Category
- Examples with explanations
- Constraints
- Test cases
- Solution template
- Hints

## Adding More Questions

You can add more questions by editing `questions.json` or using the `questions_init.py` script. Each question should follow this structure:

```json
{
  "question_id": {
    "id": "question_id",
    "title": "Question Title",
    "difficulty": "Easy",
    "category": "Arrays",
    "description": "Problem description...",
    "examples": [...],
    "constraints": [...],
    "template": "class Solution:\n    def method(self, ...):\n        pass",
    "test_cases": [...],
    "hints": [...],
    "solution": "..."
  }
}
```

## Hint System

The IDE provides three types of hints:

- **General Hint**: High-level approach or algorithm pattern
- **Specific Hint**: What might be wrong or what to consider
- **Next Step**: The next logical step in solving the problem

Hints are generated using the local Llama-2-7B model. If the model is not available, fallback hints based on category and difficulty are provided.

## Troubleshooting

### LLM Not Loading

If hints don't work:
1. Check that the model file exists at the specified path
2. Ensure `llama-cpp-python` is installed correctly
3. Check the console for error messages

### Test Execution Errors

If tests fail to run:
1. Ensure your code follows the template structure
2. Check that your Solution class has the correct method name
3. Review the error messages in the results panel

## Notes

- The LLM model is loaded lazily (only when first hint is requested)
- Code execution has a 10-second timeout
- Test cases are executed in a sandboxed environment

## License

This project is for educational purposes.

