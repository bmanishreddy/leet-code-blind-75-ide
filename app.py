#!/usr/bin/env python3
"""
LeetCode Blind 75 IDE
A learning IDE with AI-powered hints for practicing Blind 75 questions
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
import json
import subprocess
import tempfile
import re
from typing import Dict, List, Optional
import traceback
from visualizations import get_visualization

# Add path for LLM integration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../cortex-sdk/Chat_bot')))

from rag_hint_system import rag_system

app = Flask(__name__)

# Initialize LLM for hints (lazy loading)
hint_llm = None
model_path = "/Users/manishb/Desktop/Coding/cortex-sdk/Chat_bot/rag_model/foundation_model/llama-2-7b-chat-hf-q2_k.gguf"

def get_hint_llm():
    """Lazy initialization of the hint LLM."""
    global hint_llm
    if hint_llm is None:
        try:
            from llama_cpp import Llama
            if os.path.exists(model_path):
                print(f"Loading LLM model from {model_path}...")
                hint_llm = Llama(
                    model_path=model_path,
                    n_ctx=2048,
                    n_threads=4,
                    n_gpu_layers=0,
                    verbose=False
                )
                print("LLM model loaded successfully!")
            else:
                print(f"Warning: Model not found at {model_path}. Hints will be disabled.")
        except Exception as e:
            print(f"Warning: Failed to load LLM: {e}. Hints will be disabled.")
    return hint_llm

# Load questions database
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'questions.json')

def load_questions() -> Dict:
    """Load questions from JSON file."""
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_questions(questions: Dict):
    """Save questions to JSON file."""
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(questions, f, indent=2)

@app.route('/')
def index():
    """Render the main IDE interface."""
    return render_template('index.html')

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get all questions."""
    questions = load_questions()
    return jsonify(questions)

@app.route('/api/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    """Get a specific question."""
    questions = load_questions()
    if question_id in questions:
        return jsonify(questions[question_id])
    return jsonify({"error": "Question not found"}), 404

@app.route('/api/questions/<question_id>/progress', methods=['POST'])
def update_progress(question_id):
    """Update progress for a question."""
    data = request.json
    questions = load_questions()
    
    if question_id in questions:
        if 'progress' not in questions[question_id]:
            questions[question_id]['progress'] = {}
        questions[question_id]['progress'].update(data)
        save_questions(questions)
        return jsonify({"success": True})
    return jsonify({"error": "Question not found"}), 404

@app.route('/api/compile', methods=['POST'])
def compile_code():
    """Compile and syntax check user code without running tests."""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        code = data.get('code', '')
        question_id = data.get('question_id', '')
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        # Try to compile the code (syntax check)
        try:
            compile(code, '<string>', 'exec')
            
            # Try to import and instantiate the class
            local_namespace = {}
            exec(code, local_namespace)
            
            if 'Solution' in local_namespace:
                # Success - code compiles and has Solution class
                return jsonify({
                    "success": True,
                    "message": "Code compiled successfully! No syntax errors found.",
                    "output": "✅ Syntax check passed\n✅ Solution class found"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "No 'Solution' class found in your code. Make sure to define a class named 'Solution'."
                })
                
        except SyntaxError as e:
            return jsonify({
                "success": False,
                "error": f"Syntax Error on line {e.lineno}:\n{e.msg}\n\n{e.text if e.text else ''}"
            })
        except IndentationError as e:
            return jsonify({
                "success": False,
                "error": f"Indentation Error on line {e.lineno}:\n{e.msg}"
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Runtime Error:\n{str(e)}"
            })
            
    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500

@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute user code immediately with examples or a simple test."""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        code = data.get('code', '')
        question_id = data.get('question_id', '')
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        # Load question to get examples
        questions = load_questions()
        question = questions.get(question_id, {}) if question_id else {}
        
        # Try to use examples from question, or create a simple test
        test_cases = []
        if question.get('examples'):
            # Convert examples to test cases
            for ex in question.get('examples', [])[:1]:  # Use first example
                if isinstance(ex, dict) and 'input' in ex:
                    test_cases.append({
                        'input': ex.get('input'),
                        'expected': ex.get('output')
                    })
        
        # If no examples, try to create a minimal test case
        if not test_cases:
            # Extract method signature to create a simple test
            method_match = re.search(r'def\s+\w+\s*\([^)]*\)', code)
            if method_match:
                method_sig = method_match.group(0)
                # Extract parameter names (skip 'self')
                params_match = re.search(r'\([^)]*\)', method_sig)
                if params_match:
                    params_str = params_match.group(0).strip('()')
                    # Split by comma and extract parameter names
                    params = [p.strip().split(':')[0].split('=')[0].strip() 
                             for p in params_str.split(',') if p.strip() != 'self']
                    
                    # Create test case based on parameter names
                    test_input = {}
                    for param in params:
                        if 'nums' in param or 'array' in param.lower():
                            test_input[param] = [1, 2, 3]
                        elif 'target' in param:
                            test_input[param] = 5
                        elif 's' in param or 'string' in param.lower() or param == 's':
                            test_input[param] = 'test'
                        elif 'n' == param or 'num' in param.lower():
                            test_input[param] = 5
                        elif 'list' in param.lower():
                            test_input[param] = [1, 2, 3]
                        else:
                            # Default value based on common patterns
                            test_input[param] = None
                    
                    if test_input:
                        test_cases.append({
                            'input': test_input,
                            'expected': None  # We'll just show the output
                        })
        
        if not test_cases:
            return jsonify({
                "success": False,
                "error": "Cannot execute: No test cases or examples available. Please use 'Run Tests' with a question that has test cases."
            })
        
        # Use the same execution logic as run_code
        return _execute_code_with_test_cases(code, test_cases, execute_mode=True)
        
    except Exception as e:
        return jsonify({"success": False, "error": f"Execution error: {str(e)}"}), 500

def _execute_code_with_test_cases(code, test_cases, execute_mode=False):
    """Shared code execution logic for both /api/run and /api/execute."""
    results = []
    errors = []
    
    # Extract method name from code (look for def in Solution class)
    method_name = None
    solution_match = re.search(r'class Solution[^:]*:\s*def\s+(\w+)\s*\(', code)
    if solution_match:
        method_name = solution_match.group(1)
    
    if not method_name:
        # Try to find any method definition
        method_match = re.search(r'def\s+(\w+)\s*\(', code)
        if method_match:
            method_name = method_match.group(1)
    
    if not method_name:
        errors.append({
            'test_case': 0,
            'error': 'Could not find a method definition in your code. Please define a method in the Solution class.'
        })
        return jsonify({
            'results': results,
            'errors': errors,
            'all_passed': False,
            'execute_mode': execute_mode
        })
    
    # Create a temporary file with the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        # Write user code
        f.write(code)
        f.write('\n\n')
        f.write('# Test runner code\n')
        f.write('import json\n')
        f.write('import sys\n')
        f.write('import io\n')
        f.write('\n')
        f.write('solution = Solution()\n')
        f.write('method = getattr(solution, "{}")\n'.format(method_name))
        f.write('\n')
        f.write('# Load test cases from stdin\n')
        f.write('test_cases = json.loads(sys.stdin.read())\n')
        f.write('\n')
        f.write('# Run each test case\n')
        f.write('for i, test_case in enumerate(test_cases):\n')
        f.write('    try:\n')
        f.write('        input_data = test_case.get("input", {})\n')
        f.write('        expected = test_case.get("expected")\n')
        f.write('        \n')
        f.write('        # Capture console output from user code\n')
        f.write('        old_stdout = sys.stdout\n')
        f.write('        sys.stdout = console_capture = io.StringIO()\n')
        f.write('        \n')
        f.write('        try:\n')
        f.write('            # Call the method\n')
        f.write('            if isinstance(input_data, dict):\n')
        f.write('                result = method(**input_data)\n')
        f.write('            elif isinstance(input_data, list):\n')
        f.write('                result = method(*input_data)\n')
        f.write('            else:\n')
        f.write('                result = method(input_data)\n')
        f.write('        finally:\n')
        f.write('            # Restore stdout and get console output\n')
        f.write('            console_output = console_capture.getvalue()\n')
        f.write('            sys.stdout = old_stdout\n')
        f.write('        \n')
        if execute_mode:
            # In execute mode, just show the output
            f.write('        print(json.dumps({\n')
            f.write('            "test_case": i + 1,\n')
            f.write('            "passed": True,\n')
            f.write('            "output": result,\n')
            f.write('            "expected": expected,\n')
            f.write('            "input": input_data,\n')
            f.write('            "console_output": console_output\n')
            f.write('        }, default=str))\n')
        else:
            # In test mode, compare with expected
            f.write('        # Skip test if no expected value provided\n')
            f.write('        if expected is None:\n')
            f.write('            print(json.dumps({\n')
            f.write('                "test_case": i + 1,\n')
            f.write('                "skipped": True,\n')
            f.write('                "passed": False,\n')
            f.write('                "output": result,\n')
            f.write('                "expected": None,\n')
            f.write('                "input": input_data,\n')
            f.write('                "console_output": console_output,\n')
            f.write('                "message": "No expected output provided for this test case"\n')
            f.write('            }, default=str))\n')
            f.write('        else:\n')
            f.write('            # Compare result with expected\n')
            f.write('            # For lists, check if they have same elements (may be order-independent)\n')
            f.write('            if isinstance(result, list) and isinstance(expected, list):\n')
            f.write('                # Try both sorted and unsorted comparison\n')
            f.write('                try:\n')
            f.write('                    passed = (sorted(result) == sorted(expected)) or (result == expected)\n')
            f.write('                except:\n')
            f.write('                    passed = result == expected\n')
            f.write('            else:\n')
            f.write('                passed = result == expected\n')
            f.write('            \n')
            f.write('            print(json.dumps({\n')
            f.write('                "test_case": i + 1,\n')
            f.write('                "passed": passed,\n')
            f.write('                "output": result,\n')
            f.write('                "expected": expected,\n')
            f.write('                "input": input_data,\n')
            f.write('                "console_output": console_output\n')
            f.write('            }, default=str))\n')
        f.write('    except Exception as e:\n')
        f.write('        # Try to get console output if available\n')
        f.write('        try:\n')
        f.write('            error_console = console_capture.getvalue() if "console_capture" in locals() else ""\n')
        f.write('            if sys.stdout != old_stdout:\n')
        f.write('                sys.stdout = old_stdout\n')
        f.write('        except:\n')
        f.write('            error_console = ""\n')
        f.write('        print(json.dumps({\n')
        f.write('            "test_case": i + 1,\n')
        f.write('            "passed": False,\n')
        f.write('            "error": str(e),\n')
        f.write('            "input": test_case.get("input", {}),\n')
        f.write('            "console_output": error_console\n')
        f.write('        }, default=str))\n')
        temp_file = f.name
    
    try:
        # Prepare test cases input
        test_input = json.dumps(test_cases)
        
        # Execute the code
        result = subprocess.run(
            ['python3', temp_file],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse output (each line is a JSON result)
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                if line.strip():
                    try:
                        result_data = json.loads(line)
                        if 'error' in result_data:
                            errors.append(result_data)
                        else:
                            results.append(result_data)
                    except json.JSONDecodeError:
                        pass
        else:
            # Code execution error
            error_msg = result.stderr or result.stdout or 'Unknown error'
            errors.append({
                'test_case': 0,
                'error': error_msg
            })
    
    except subprocess.TimeoutExpired:
        errors.append({
            'test_case': 0,
            'error': 'Code execution timed out (max 10 seconds)'
        })
    except Exception as e:
        errors.append({
            'test_case': 0,
            'error': f'Execution error: {str(e)}'
        })
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    return jsonify({
        'results': results,
        'errors': errors,
        'all_passed': len(errors) == 0 and len(results) > 0 and all(r.get('passed', False) for r in results),
        'execute_mode': execute_mode
    })

@app.route('/api/run', methods=['POST'])
def run_code():
    """Run user code with test cases."""
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        code = data.get('code', '')
        test_cases = data.get('test_cases', [])
        question_id = data.get('question_id', '')
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        # If no test cases provided, try to get from question examples
        if not test_cases:
            questions = load_questions()
            question = questions.get(question_id, {}) if question_id else {}
            
            # Convert examples to test cases
            if question.get('examples'):
                for ex in question.get('examples', []):
                    if isinstance(ex, dict) and 'input' in ex:
                        test_cases.append({
                            'input': ex.get('input'),
                            'expected': ex.get('output')
                        })
        
        if not test_cases:
            return jsonify({
                "error": "No test cases available for this question.",
                "details": "This question doesn't have test cases configured. Please use 'Execute Code' to run your code with examples, or contact the administrator to add test cases for this problem.",
                "suggestion": "Try using the 'Execute Code' button instead, which will use examples or generate simple test cases."
            }), 400
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400
    
    return _execute_code_with_test_cases(code, test_cases, execute_mode=False)

@app.route('/api/hint', methods=['POST'])
def get_hint():
    """Get a hint using RAG system."""
    try:
        data = request.get_json() if request.is_json else {}
        
        question = data.get('question', {})
        user_code = data.get('code', '')
        hint_type = data.get('hint_type', 'general')
        
        # Use RAG system for intelligent hints
        hint = rag_system.get_hint(question, user_code, hint_type)
        
        return jsonify({
            'hint': hint,
            'rag_available': True
        })
    except Exception as e:
        print(f"Error in hint endpoint: {e}")
        import traceback
        traceback.print_exc()
        # Return a friendly hint even on error
        return jsonify({
            'hint': 'Think about the problem step by step. Consider what data structure would help solve this efficiently?',
            'rag_available': False
        }), 200

def _build_hint_prompt(question: Dict, user_code: str, hint_type: str) -> str:
    """Build a prompt for hint generation with code analysis."""
    title = question.get('title', '')
    description = question.get('description', '')
    examples = question.get('examples', [])
    category = question.get('category', '')
    difficulty = question.get('difficulty', '')
    
    prompt = f"""You are a helpful coding tutor helping a student learn LeetCode problems.

Problem: {title}
Difficulty: {difficulty}
Category: {category}
Description: {description}

"""
    
    if examples:
        prompt += "Examples:\n"
        for ex in examples[:2]:
            prompt += f"- Input: {ex.get('input')}\n  Output: {ex.get('output')}\n"
            if ex.get('explanation'):
                prompt += f"  Explanation: {ex.get('explanation')}\n"
    
    prompt += f"\nStudent's current code:\n```python\n{user_code}\n```\n\n"
    
    # Add context-specific guidance based on hint type
    if hint_type == 'general':
        prompt += """Provide a gentle hint about the approach or algorithm pattern to use. 
Consider what patterns are already in the code and what might be missing.
Focus on the general strategy without giving away the solution.
Don't just repeat what they already have - guide them forward."""
    elif hint_type == 'specific':
        prompt += """Provide a specific hint about what might be wrong or what to consider next.
Look at their code structure and identify:
- What's missing that they need?
- What might be incorrect in their current approach?
- What's the next logical step based on their current code?
Be specific but don't give away the complete solution."""
    elif hint_type == 'next_step':
        prompt += """Provide the next logical step in solving this problem.
Based on their current code, what should they do next?
Be concrete and actionable - tell them exactly what to add or modify.
Example: "Add a variable to track..." or "Create a loop that..." or "Use a dictionary to..."
Keep it to one clear next step."""
    
    prompt += "\n\nProvide a helpful, encouraging hint:"
    
    return prompt

def _get_fallback_hint(question: Dict, user_code: str, hint_type: str) -> str:
    """Get a fallback hint when LLM is not available, using code analysis."""
    category = question.get('category', '').lower()
    title = question.get('title', '').lower()
    
    # Analyze code to see what user has done
    has_code = len(user_code.strip()) > 50
    has_loop = 'for ' in user_code or 'while ' in user_code
    has_dict = '{' in user_code or 'dict' in user_code.lower()
    has_set = 'set(' in user_code
    
    # Category-specific hints based on hint type
    if 'array' in category or 'list' in category or 'two pointer' in category:
        if hint_type == 'general':
            return "💡 Consider using two pointers or a hash map to track elements efficiently."
        elif hint_type == 'specific':
            if not has_dict:
                return "🎯 Use a dictionary (hash map) to store values as you iterate. This gives O(1) lookup time!"
            else:
                return "🎯 Good! Now think about what to store in your hash map - perhaps the value as key and index as value?"
        else:  # next_step
            if not has_loop:
                return "📝 Next: Start with 'for i, num in enumerate(nums):' to iterate through the array."
            else:
                return "📝 Next: Inside your loop, check if the complement exists in your hash map before adding the current value."
    
    elif 'hash' in category or 'map' in category or 'set' in title:
        if hint_type == 'general':
            return "💡 Hash maps provide O(1) lookup! Think about what you need to store and retrieve quickly."
        elif hint_type == 'specific':
            return "🎯 Create a dictionary to map each element to additional info (like its index, count, or related value)."
        else:
            return "📝 Next: Initialize an empty dict, then iterate through your input and populate it: seen = {}"
    
    elif 'tree' in category:
        if hint_type == 'general':
            return "💡 Tree problems often use recursion. Think about: base case, what to do at each node, and how to combine results."
        elif hint_type == 'specific':
            return "🎯 For binary trees, consider these traversals: in-order (left, root, right), pre-order (root, left, right), or post-order (left, right, root)."
        else:
            return "📝 Next: Define a helper function that takes a node as parameter. Handle the None case first (base case)."
    
    elif 'graph' in category:
        if hint_type == 'general':
            return "💡 Graph traversal: Use BFS (queue) for shortest paths or level-by-level. Use DFS (stack/recursion) for paths or connectivity."
        elif hint_type == 'specific':
            return "🎯 Always track visited nodes using a set to avoid cycles: visited = set(). Check 'if node not in visited' before processing."
        else:
            return "📝 Next: Initialize a queue (for BFS) or use recursion (for DFS), and a visited set. Start from your source node."
    
    elif 'dynamic programming' in category or 'dp' in category:
        if hint_type == 'general':
            return "💡 DP = Recursion + Memoization. Identify overlapping subproblems and optimal substructure."
        elif hint_type == 'specific':
            return "🎯 Create a DP array where dp[i] represents the answer for subproblem i. Define your base cases (like dp[0] = ...) first."
        else:
            return "📝 Next: Write the recurrence relation. How does dp[i] relate to previous values like dp[i-1]?"
    
    elif 'binary search' in category or 'search' in category:
        if hint_type == 'general':
            return "💡 Binary search works on sorted data. Eliminate half the search space each iteration → O(log n)."
        elif hint_type == 'specific':
            return "🎯 Set left=0, right=len(array)-1. In loop: mid=(left+right)//2. Compare array[mid] with target to adjust left or right."
        else:
            return "📝 Next: Use 'while left <= right:' and update left=mid+1 or right=mid-1 based on comparison."
    
    elif 'string' in category:
        if hint_type == 'general':
            return "💡 String problems often use: sliding window, two pointers, hash maps for character counting, or string manipulation."
        elif hint_type == 'specific':
            return "🎯 Use a hash map to count character frequencies: char_count = {} or collections.Counter()."
        else:
            return "📝 Next: Iterate through the string with 'for char in s:' and build your solution character by character."
    
    elif 'linked list' in category:
        if hint_type == 'general':
            return "💡 Linked list tip: Use two pointers (slow/fast) or dummy nodes to simplify edge cases."
        elif hint_type == 'specific':
            return "🎯 Create a dummy node: dummy = ListNode(0); dummy.next = head. This helps handle edge cases like empty lists."
        else:
            return "📝 Next: Traverse with 'while current:' and use 'current = current.next' to move forward."
    
    else:
        # Generic hints
        if hint_type == 'general':
            return "💡 Break down the problem: 1) What's the input/output? 2) What data structure fits? 3) What's the time complexity goal?"
        elif hint_type == 'specific':
            if not has_code:
                return "🎯 Start by writing the function signature and thinking about your approach before coding."
            else:
                return "🎯 Consider edge cases: empty input, single element, duplicates. Does your solution handle them?"
        else:
            return "📝 Next: Implement a brute force solution first, then think about optimizations."
    
    return "Think about the problem step by step and consider different approaches."

@app.route('/api/solution', methods=['POST'])
def get_solution():
    """Get the solution code directly from the knowledge base (no LLM)."""
    try:
        data = request.get_json() if request.is_json else {}
        question = data.get('question', {})
        
        if not question:
            return jsonify({
                'solution': None,
                'error': 'No question provided'
            }), 400
        
        # Get problem from knowledge base
        title = question.get('title', '').lower()
        problem_id = question.get('id', '')
        
        # Normalize formats (handle both underscores and hyphens)
        normalized_id = problem_id.replace('_', '-').lower() if problem_id else ''
        normalized_title = title.replace(' ', '-').replace('_', '-')
        
        # Try to find solution in knowledge base
        problem_kb = None
        problem_slug = None
        for slug, data in rag_system.knowledge_base.items():
            # Try multiple matching strategies
            if (slug == problem_id or 
                slug == normalized_id or
                slug.replace('-', '_') == problem_id or
                slug in title or 
                normalized_title in slug or
                slug in normalized_title or
                title.replace(' ', '-') in slug):
                problem_kb = data
                problem_slug = slug
                break
        
        if not problem_kb:
            return jsonify({
                'solution': None,
                'available': False,
                'message': 'Solution not available for this problem yet.'
            }), 200
        
        # Get solution details
        code_template = problem_kb.get('code_template', '')
        approach = problem_kb.get('approach', 'Unknown')
        explanation = problem_kb.get('explanation', '')
        time_complexity = problem_kb.get('time_complexity', 'N/A')
        space_complexity = problem_kb.get('space_complexity', 'N/A')
        
        if not code_template:
            return jsonify({
                'solution': None,
                'available': False,
                'message': 'Solution code not available for this problem.'
            }), 200
        
        return jsonify({
            'solution': code_template.strip(),
            'approach': approach,
            'explanation': explanation,
            'time_complexity': time_complexity,
            'space_complexity': space_complexity,
            'available': True,
            'problem_slug': problem_slug
        })
        
    except Exception as e:
        print(f"Error getting solution: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'solution': None,
            'available': False,
            'error': str(e)
        }), 500

def generate_visual_diagram(question):
    """Generate visual diagram programmatically using visualizations module."""
    return get_visualization(question.get('id', ''), question)

@app.route('/api/visualize', methods=['POST'])
def visualize_algorithm():
    """Generate step-by-step visual diagram programmatically."""
    try:
        data = request.get_json() if request.is_json else {}
        question = data.get('question', {})
        user_code = data.get('code', '')
        
        if not question:
            return jsonify({
                'visualization': None,
                'error': 'No question provided'
            }), 400
        
        title = question.get('title', 'Unknown Problem')
        
        # Generate visualization programmatically (no LLM needed)
        visualization = generate_visual_diagram(question)
        
        return jsonify({
            'visualization': visualization,
            'title': f"📊 Algorithm Visualization: {title}",
            'available': True
        })
            
    except Exception as e:
        print(f"Error generating visualization: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'visualization': None,
            'error': str(e),
            'available': False
        }), 500

if __name__ == '__main__':
    # Initialize questions if they don't exist
    if not os.path.exists(QUESTIONS_FILE):
        from questions_init import initialize_questions
        initialize_questions()
    
    app.run(host='0.0.0.0', debug=True, port=5000)

