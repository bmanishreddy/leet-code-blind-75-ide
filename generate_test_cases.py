#!/usr/bin/env python3
"""
Generate test cases for questions based on method signatures and common patterns
"""
import json
import os
import re

QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'questions.json')

# Common test case patterns based on parameter names
TEST_PATTERNS = {
    'nums': [1, 2, 3],
    'target': 5,
    's': 'test',
    't': 'test',
    'n': 5,
    'k': 2,
    'val': 3,
    'key': 'test',
    'word': 'test',
    'strs': ['test', 'test2'],
    'intervals': [[1,3],[2,6],[8,10]],
    'matrix': [[1,2,3],[4,5,6],[7,8,9]],
    'grid': [[1,1],[1,1]],
    'coins': [1,2,5],
    'amount': 11,
    'prices': [7,1,5,3,6,4],
    'height': [0,1,0,2,1,0,1,3,2,1,2,1],
    'list1': [1,2,4],
    'list2': [1,3,4],
    'head': [1,2,3,4,5],
    'headA': [4,1,8,4,5],
    'headB': [5,6,1,8,4,5],
}

def extract_params(template):
    """Extract parameter names from template."""
    match = re.search(r'def\s+\w+\s*\([^)]*\)', template)
    if not match:
        return []
    
    params_str = match.group(0)
    params_match = re.search(r'\([^)]*\)', params_str)
    if not params_match:
        return []
    
    params = [p.strip().split(':')[0].split('=')[0].strip() 
              for p in params_match.group(0).strip('()').split(',') 
              if p.strip() != 'self']
    return params

def generate_test_case(params):
    """Generate a test case based on parameters."""
    test_input = {}
    for param in params:
        # Try to find a pattern match
        found = False
        for pattern_key, pattern_value in TEST_PATTERNS.items():
            if pattern_key in param.lower():
                test_input[param] = pattern_value
                found = True
                break
        
        if not found:
            # Default based on param name
            if 'num' in param.lower() or 'array' in param.lower() or 'list' in param.lower():
                test_input[param] = [1, 2, 3]
            elif 'str' in param.lower() or 's' == param.lower() or 't' == param.lower():
                test_input[param] = 'test'
            elif 'target' in param.lower():
                test_input[param] = 5
            elif param.lower() in ['n', 'k', 'val']:
                test_input[param] = 5
            else:
                test_input[param] = None
    
    return test_input

def add_test_cases_to_questions():
    """Add test cases to questions that don't have them."""
    
    if not os.path.exists(QUESTIONS_FILE):
        print(f"Error: {QUESTIONS_FILE} not found!")
        return
    
    with open(QUESTIONS_FILE, 'r') as f:
        questions = json.load(f)
    
    updated_count = 0
    
    for qid, question in questions.items():
        # Skip if already has test cases
        if question.get('test_cases') and len(question.get('test_cases', [])) > 0:
            continue
        
        template = question.get('template', '')
        if not template:
            continue
        
        # Extract parameters
        params = extract_params(template)
        if not params:
            continue
        
        # Generate test case
        test_input = generate_test_case(params)
        
        # Create test cases (2-3 cases)
        test_cases = [
            {"input": test_input, "expected": None}
        ]
        
        # Add a second test case with different values if possible
        if len(params) > 0:
            test_input2 = {}
            for param in params:
                if isinstance(test_input[param], list):
                    test_input2[param] = [4, 5, 6] if 'num' in param.lower() else test_input[param]
                elif isinstance(test_input[param], (int, float)):
                    test_input2[param] = test_input[param] + 1
                elif isinstance(test_input[param], str):
                    test_input2[param] = 'example'
                else:
                    test_input2[param] = test_input[param]
            test_cases.append({"input": test_input2, "expected": None})
        
        question['test_cases'] = test_cases
        updated_count += 1
        
        # Also add examples if missing
        if not question.get('examples'):
            question['examples'] = [
                {
                    "input": tc["input"],
                    "output": tc.get("expected"),
                    "explanation": f"Example test case for {question.get('title', qid)}"
                }
                for tc in test_cases[:2]
            ]
    
    # Save updated questions
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(questions, f, indent=2)
    
    print(f"✅ Generated test cases for {updated_count} questions!")
    print(f"📝 Saved to {QUESTIONS_FILE}")

if __name__ == '__main__':
    add_test_cases_to_questions()

