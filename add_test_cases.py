#!/usr/bin/env python3
"""
Add test cases to questions.json from blind75_questions.py
"""
import json
import os
import sys

# Import the questions with test cases
sys.path.insert(0, os.path.dirname(__file__))
from blind75_questions import get_all_questions

QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'questions.json')

def add_test_cases():
    """Add test cases to questions.json from blind75_questions.py"""
    
    # Load questions with test cases
    questions_with_tests = get_all_questions()
    
    # Load existing questions.json
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'r') as f:
            existing_questions = json.load(f)
    else:
        print(f"Error: {QUESTIONS_FILE} not found!")
        return
    
    # Update questions with test cases
    updated_count = 0
    for qid, question_data in questions_with_tests.items():
        if qid in existing_questions:
            # Update test cases if they exist in the source
            if 'test_cases' in question_data and question_data['test_cases']:
                existing_questions[qid]['test_cases'] = question_data['test_cases']
                updated_count += 1
                
                # Also update examples if they're missing
                if not existing_questions[qid].get('examples') and 'examples' in question_data:
                    existing_questions[qid]['examples'] = question_data['examples']
    
    # Save updated questions
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(existing_questions, f, indent=2)
    
    print(f"✅ Updated {updated_count} questions with test cases!")
    print(f"📝 Saved to {QUESTIONS_FILE}")

if __name__ == '__main__':
    add_test_cases()

