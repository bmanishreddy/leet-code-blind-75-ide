#!/usr/bin/env python3
"""
Fix all question templates with proper parameters
"""

import json
import os

# Parameter mapping for each method
PARAM_MAP = {
    "twoSum": "nums, target",
    "isPalindrome": "s",
    "removeDuplicates": "nums",
    "moveZeroes": "nums",
    "mergeTwoLists": "list1, list2",
    "reverseList": "head",
    "getIntersectionNode": "headA, headB",
    "hasCycle": "head",
    "containsDuplicate": "nums",
    "isAnagram": "s, t",
    "firstUniqChar": "s",
    "maxSubArray": "nums",
    "maxProfit": "prices",
    "missingNumber": "nums",
    "isValid": "s",
    "maxDepth": "root",
    "isSameTree": "p, q",
    "isSymmetric": "root",
    "invertTree": "root",
    "isSubtree": "root, subRoot",
    "lowestCommonAncestor": "root, p, q",
    "removeNthFromEnd": "head, n",
    "threeSum": "nums",
    "lengthOfLongestSubstring": "s",
    "maxArea": "height",
    "characterReplacement": "s, k",
    "detectCycle": "head",
    "groupAnagrams": "strs",
    "isValidSudoku": "board",
    "subarraySum": "nums, k",
    "minWindow": "s, t",
    "MinStack": "",  # Constructor
    "evalRPN": "tokens",
    "dailyTemperatures": "temperatures",
    "search": "nums, target",  # For binary search
    "findMin": "nums",
    "kthSmallest": "root, k",
    "addTwoNumbers": "l1, l2",
    "reorderList": "head",
    "isValidBST": "root",
    "levelOrder": "root",
    "buildTree": "preorder, inorder",
    "numIslands": "grid",
    "cloneGraph": "node",
    "canFinish": "numCourses, prerequisites",
    "pacificAtlantic": "heights",
    "validTree": "n, edges",
    "countComponents": "n, edges",
    "exist": "board, word",
    "combinationSum": "candidates, target",
    "subsets": "nums",
    "permute": "nums",
    "climbStairs": "n",
    "rob": "nums",
    "uniquePaths": "m, n",
    "coinChange": "coins, amount",
    "lengthOfLIS": "nums",
    "numDecodings": "s",
    "wordBreak": "s, wordDict",
    "longestPalindrome": "s",
    "countSubstrings": "s",
    "maxProduct": "nums",
    "minPathSum": "grid",
    "rotate": "matrix",
    "spiralOrder": "matrix",
    "setZeroes": "matrix",
    "merge": "intervals",
    "insert": "intervals, newInterval",
    "LRUCache": "capacity",  # Constructor
    "encode": "strs",
    "trap": "height",
    "maxPathSum": "root",
    "serialize": "root",
    "ladderLength": "beginWord, endWord, wordList",
    "mergeKLists": "lists",
}

QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'questions.json')

def fix_templates():
    """Fix all question templates."""
    with open(QUESTIONS_FILE, 'r') as f:
        questions = json.load(f)
    
    fixed_count = 0
    for qid, question in questions.items():
        template = question.get('template', '')
        
        # Extract method name from template
        import re
        match = re.search(r'def\s+(\w+)\s*\(', template)
        if match:
            method_name = match.group(1)
            params = PARAM_MAP.get(method_name, "")
            
            if params:
                # Fix the template
                new_template = f"class Solution:\n    def {method_name}(self, {params}):\n        # Your code here\n        pass"
            else:
                # For constructors or methods without standard params
                new_template = f"class Solution:\n    def {method_name}(self):\n        # Your code here\n        pass"
            
            if template != new_template:
                question['template'] = new_template
                fixed_count += 1
    
    # Save fixed questions
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(questions, f, indent=2)
    
    print(f"Fixed {fixed_count} question templates")
    return fixed_count

if __name__ == '__main__':
    fix_templates()

