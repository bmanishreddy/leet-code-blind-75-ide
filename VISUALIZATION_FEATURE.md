# Algorithm Visualization Feature 📊

## Overview
The new **Visualize Algorithm** feature generates step-by-step visual diagrams to help understand algorithm solutions using AI-powered LLM.

## Features

### 1. Visual Step-by-Step Breakdown
- Breaks down algorithms into 5-7 clear, digestible steps
- Each step includes:
  - Step number and title
  - Visual ASCII representation
  - Brief explanation (1-2 sentences)

### 2. Smart Visualization
- Uses Deepseek-Coder-1.3B LLM to generate contextual diagrams
- Displays data structures visually:
  - Arrays: `[1, 2, 3, 4, 5]`
  - Pointers: `left→  ←right`
  - Trees: Indented or ASCII format
  - Hash maps: `{key: value}`
- Shows state changes between steps

### 3. Beautiful UI
- Purple gradient theme (#667eea to #764ba2)
- Animated hover effects on steps
- Scrollable content for long visualizations
- Regenerate button for new perspectives
- Fallback to structured template if LLM unavailable

## How to Use

1. **Select a Problem**: Choose any LeetCode Blind 75 problem
2. **Click Visualize**: Press the "📊 Visualize Algorithm" button in the hint panel
3. **View Steps**: Read through the step-by-step visual breakdown
4. **Regenerate**: Click "🔄 Regenerate" for a new visualization

## API Endpoint

### `POST /api/visualize`

**Request Body:**
```json
{
  "question": {
    "title": "Two Sum",
    "description": "Given an array...",
    "category": "Array"
  },
  "code": "def twoSum(self, nums, target):\n    ..."
}
```

**Response:**
```json
{
  "visualization": "STEP 1: Understand the Problem\n...",
  "title": "Algorithm Visualization: Two Sum",
  "available": true,
  "fallback": false
}
```

## Implementation Details

### Backend (`app.py`)
- `/api/visualize` endpoint at line 724-860
- Uses RAG hint system with LLM
- Generates 800-token responses
- Temperature: 0.6 for creative diagrams
- Structured fallback if LLM fails

### Frontend (`app.js`)
- `visualizeAlgorithm()` function at line 852-938
- Parses STEP-based format
- Escapes HTML for security
- Handles loading states
- Event listener at line 1255

### UI (`index.html`)
- Button added to hint panel at line 105-107
- Purple gradient styling
- Positioned between hints and solution

### Styling (`style.css`)
- `.visualization-display` - Main container
- `.visualization-step` - Each step card
- `.step-number` - Purple gradient badge
- `.step-content pre` - Code/diagram display
- Hover animations and transitions

## Performance

- **LLM Response Time**: ~2-5 seconds
- **Token Limit**: 800 tokens (balanced detail)
- **GPU Acceleration**: 28 layers on Apple Silicon
- **Fallback**: Instant structured template

## Example Output

```
STEP 1: Initialize Data Structure
Create a hash map to store values and indices
{value: index}
Explanation: Use a dictionary for O(1) lookups.

STEP 2: Iterate Through Array
For each number, check if complement exists
nums = [2, 7, 11, 15], target = 9
     i=0: 2 → check for 7
Explanation: Calculate complement = target - current.

STEP 3: Return Result
Found pair at indices [0, 1]
Explanation: Return as soon as match is found.
```

## Benefits

✅ **Educational**: Helps visualize algorithm flow
✅ **Interactive**: Regenerate for different perspectives  
✅ **AI-Powered**: Contextual to specific problems
✅ **Fast**: Under 5 seconds with GPU acceleration
✅ **Robust**: Fallback ensures always available
✅ **Beautiful**: Modern UI with smooth animations

## Future Enhancements

- [ ] Interactive step navigation (next/prev)
- [ ] Animated transitions between steps
- [ ] Export visualization as image
- [ ] Copy individual steps
- [ ] Language-specific visualizations
- [ ] Custom visualization templates per pattern (Two Pointers, Sliding Window, etc.)

## Testing

Test the feature:
1. Start the server: `python3 app.py`
2. Open browser: `http://localhost:5000`
3. Select "Two Sum" problem
4. Click "📊 Visualize Algorithm"
5. Verify steps render correctly

## Branch
- **Development**: `release/dev`
- **Status**: ✅ Complete and tested

---

**Created**: November 8, 2025  
**Author**: AI Assistant  
**LLM Model**: Deepseek-Coder-1.3B

