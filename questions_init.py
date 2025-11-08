#!/usr/bin/env python3
"""
Initialize the Blind 75 questions database
Comprehensive database with all 75 problems organized by groups
"""

import json
import os
import re

QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'questions.json')

def initialize_questions():
    """Initialize the questions database with Blind 75 problems."""
    # Import from comprehensive database
    try:
        from complete_blind75 import get_all_blind75_questions
        questions = get_all_blind75_questions()
        print("Loaded comprehensive Blind 75 questions database")
    except ImportError:
        # Fallback to basic questions if comprehensive file not available
        print("Using fallback questions (comprehensive database not available)")
        questions = {
        "two_sum": {
            "id": "two_sum",
            "title": "Two Sum",
            "difficulty": "Easy",
            "category": "Arrays",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "examples": [
                {
                    "input": {"nums": [2, 7, 11, 15], "target": 9},
                    "output": [0, 1],
                    "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
                },
                {
                    "input": {"nums": [3, 2, 4], "target": 6},
                    "output": [1, 2],
                    "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."
                }
            ],
            "constraints": [
                "2 <= nums.length <= 10^4",
                "-10^9 <= nums[i] <= 10^9",
                "-10^9 <= target <= 10^9",
                "Only one valid answer exists."
            ],
            "template": """class Solution:
    def twoSum(self, nums, target):
        # Your code here
        pass
""",
            "test_cases": [
                {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]},
                {"input": {"nums": [3, 2, 4], "target": 6}, "expected": [1, 2]},
                {"input": {"nums": [3, 3], "target": 6}, "expected": [0, 1]}
            ],
            "hints": [
                "Use a hash map to store numbers you've seen",
                "For each number, check if target - number exists in the map"
            ],
            "solution": """class Solution:
    def twoSum(self, nums, target):
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []
"""
        },
        "valid_palindrome": {
            "id": "valid_palindrome",
            "title": "Valid Palindrome",
            "difficulty": "Easy",
            "category": "Two Pointers",
            "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.",
            "examples": [
                {
                    "input": {"s": "A man, a plan, a canal: Panama"},
                    "output": True,
                    "explanation": "amanaplanacanalpanama is a palindrome."
                },
                {
                    "input": {"s": "race a car"},
                    "output": False,
                    "explanation": "raceacar is not a palindrome."
                }
            ],
            "constraints": [
                "1 <= s.length <= 2 * 10^5",
                "s consists only of printable ASCII characters."
            ],
            "template": """class Solution:
    def isPalindrome(self, s):
        # Your code here
        pass
""",
            "test_cases": [
                {"input": {"s": "A man, a plan, a canal: Panama"}, "expected": True},
                {"input": {"s": "race a car"}, "expected": False},
                {"input": {"s": " "}, "expected": True}
            ],
            "hints": [
                "Use two pointers: one at the start, one at the end",
                "Skip non-alphanumeric characters",
                "Compare characters after converting to lowercase"
            ],
            "solution": """class Solution:
    def isPalindrome(self, s):
        left = 0
        right = len(s) - 1
        
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while right > left and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True
"""
        },
        "best_time_to_buy_sell_stock": {
            "id": "best_time_to_buy_sell_stock",
            "title": "Best Time to Buy and Sell Stock",
            "difficulty": "Easy",
            "category": "Arrays",
            "description": "You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
            "examples": [
                {
                    "input": {"prices": [7, 1, 5, 3, 6, 4]},
                    "output": 5,
                    "explanation": "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5."
                },
                {
                    "input": {"prices": [7, 6, 4, 3, 1]},
                    "output": 0,
                    "explanation": "In this case, no transactions are done and the max profit = 0."
                }
            ],
            "constraints": [
                "1 <= prices.length <= 10^5",
                "0 <= prices[i] <= 10^4"
            ],
            "template": """class Solution:
    def maxProfit(self, prices):
        # Your code here
        pass
""",
            "test_cases": [
                {"input": {"prices": [7, 1, 5, 3, 6, 4]}, "expected": 5},
                {"input": {"prices": [7, 6, 4, 3, 1]}, "expected": 0},
                {"input": {"prices": [2, 4, 1]}, "expected": 2}
            ],
            "hints": [
                "Keep track of the minimum price seen so far",
                "Calculate profit for each day and track the maximum"
            ],
            "solution": """class Solution:
    def maxProfit(self, prices):
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            min_price = min(min_price, price)
            max_profit = max(max_profit, price - min_price)
        
        return max_profit
"""
        },
        "contains_duplicate": {
            "id": "contains_duplicate",
            "title": "Contains Duplicate",
            "difficulty": "Easy",
            "category": "Arrays",
            "description": "Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.",
            "examples": [
                {
                    "input": {"nums": [1, 2, 3, 1]},
                    "output": True
                },
                {
                    "input": {"nums": [1, 2, 3, 4]},
                    "output": False
                }
            ],
            "constraints": [
                "1 <= nums.length <= 10^5",
                "-10^9 <= nums[i] <= 10^9"
            ],
            "template": """class Solution:
    def containsDuplicate(self, nums):
        # Your code here
        pass
""",
            "test_cases": [
                {"input": {"nums": [1, 2, 3, 1]}, "expected": True},
                {"input": {"nums": [1, 2, 3, 4]}, "expected": False},
                {"input": {"nums": [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]}, "expected": True}
            ],
            "hints": [
                "Use a set to track seen numbers",
                "If you see a number that's already in the set, return True"
            ],
            "solution": """class Solution:
    def containsDuplicate(self, nums):
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
"""
        },
        "move_zeroes": {
            "id": "move_zeroes",
            "title": "Move Zeroes",
            "difficulty": "Easy",
            "category": "Two Pointers",
            "description": "Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.",
            "examples": [
                {
                    "input": {"nums": [0, 1, 0, 3, 12]},
                    "output": [1, 3, 12, 0, 0],
                    "explanation": "Note that you must do this in-place without making a copy of the array."
                }
            ],
            "constraints": [
                "1 <= nums.length <= 10^4",
                "-2^31 <= nums[i] <= 2^31 - 1"
            ],
            "template": """class Solution:
    def moveZeroes(self, nums):
        # Your code here
        # Modify nums in-place instead of returning
        pass
""",
            "test_cases": [
                {"input": {"nums": [0, 1, 0, 3, 12]}, "expected": [1, 3, 12, 0, 0]},
                {"input": {"nums": [0]}, "expected": [0]}
            ],
            "hints": [
                "Use two pointers: one for reading, one for writing",
                "Write non-zero elements first, then fill remaining with zeros"
            ],
            "solution": """class Solution:
    def moveZeroes(self, nums):
        write_pos = 0
        for read_pos in range(len(nums)):
            if nums[read_pos] != 0:
                nums[write_pos] = nums[read_pos]
                write_pos += 1
        
        for i in range(write_pos, len(nums)):
            nums[i] = 0
"""
        }
    }  # Close the fallback questions dictionary
    
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(questions, f, indent=2)
    
    print(f"Initialized {len(questions)} questions in {QUESTIONS_FILE}")

if __name__ == '__main__':
    initialize_questions()

