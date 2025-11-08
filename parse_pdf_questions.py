#!/usr/bin/env python3
"""
Parse the OCR text from PDF and create complete questions database
"""

import json
import re

# OCR extracted text structure - I'll parse this to create all questions
# Based on the OCR output, I can see the structure

def create_question_basic(qid, leetcode_num, title, difficulty, category, description_template):
    """Create a basic question structure."""
    # Extract method name from title
    method_name_map = {
        "Two Sum": "twoSum",
        "Valid Palindrome": "isPalindrome", 
        "Remove Duplicates from Sorted Array": "removeDuplicates",
        "Move Zeroes": "moveZeroes",
        "Merge Two Sorted Lists": "mergeTwoLists",
        "Reverse Linked List": "reverseList",
        "Intersection of Two Linked Lists": "getIntersectionNode",
        "Linked List Cycle": "hasCycle",
        "Contains Duplicate": "containsDuplicate",
        "Valid Anagram": "isAnagram",
        "First Unique Character in a String": "firstUniqChar",
        "Maximum Subarray": "maxSubArray",
        "Best Time to Buy and Sell Stock": "maxProfit",
        "Missing Number": "missingNumber",
        "Valid Parentheses": "isValid",
        "Maximum Depth of Binary Tree": "maxDepth",
        "Same Tree": "isSameTree",
        "Symmetric Tree": "isSymmetric",
        "Invert Binary Tree": "invertTree",
        "Subtree of Another Tree": "isSubtree",
        "Lowest Common Ancestor of a Binary Search Tree": "lowestCommonAncestor",
        # Medium
        "Remove Nth Node From End of List": "removeNthFromEnd",
        "Two Sum II - Input Array Is Sorted": "twoSum",
        "3Sum": "threeSum",
        "Longest Substring Without Repeating Characters": "lengthOfLongestSubstring",
        "Container With Most Water": "maxArea",
        "Longest Repeating Character Replacement": "characterReplacement",
        "Linked List Cycle II": "detectCycle",
        "Group Anagrams": "groupAnagrams",
        "Valid Sudoku": "isValidSudoku",
        "Subarray Sum Equals K": "subarraySum",
        "Minimum Window Substring": "minWindow",
        "Min Stack": "MinStack",
        "Evaluate Reverse Polish Notation": "evalRPN",
        "Daily Temperatures": "dailyTemperatures",
        "Binary Search": "search",
        "Find Minimum in Rotated Sorted Array": "findMin",
        "Search in Rotated Sorted Array": "search",
        "Kth Smallest Element in a BST": "kthSmallest",
        "Add Two Numbers": "addTwoNumbers",
        "Reorder List": "reorderList",
        "Validate Binary Search Tree": "isValidBST",
        "Binary Tree Level Order Traversal": "levelOrder",
        "Construct Binary Tree from Preorder and Inorder Traversal": "buildTree",
        "Lowest Common Ancestor of a Binary Tree": "lowestCommonAncestor",
        "Number of Islands": "numIslands",
        "Clone Graph": "cloneGraph",
        "Course Schedule": "canFinish",
        "Pacific Atlantic Water Flow": "pacificAtlantic",
        "Graph Valid Tree": "validTree",
        "Number of Connected Components in an Undirected Graph": "countComponents",
        "Word Search": "exist",
        "Combination Sum": "combinationSum",
        "Subsets": "subsets",
        "Permutations": "permute",
        "Climbing Stairs": "climbStairs",
        "House Robber": "rob",
        "Unique Paths": "uniquePaths",
        "Coin Change": "coinChange",
        "Longest Increasing Subsequence": "lengthOfLIS",
        "Decode Ways": "numDecodings",
        "Word Break": "wordBreak",
        "Longest Palindromic Substring": "longestPalindrome",
        "Palindromic Substrings": "countSubstrings",
        "Maximum Product Subarray": "maxProduct",
        "Minimum Path Sum": "minPathSum",
        "Rotate Image": "rotate",
        "Spiral Matrix": "spiralOrder",
        "Set Matrix Zeroes": "setZeroes",
        "Merge Intervals": "merge",
        "Insert Interval": "insert",
        "LRU Cache": "LRUCache",
        "Encode and Decode Strings": "encode",
        # Hard
        "Trapping Rain Water": "trap",
        "Binary Tree Maximum Path Sum": "maxPathSum",
        "Serialize and Deserialize Binary Tree": "serialize",
        "Word Ladder": "ladderLength",
        "Merge k Sorted Lists": "mergeKLists",
    }
    
    method_name = method_name_map.get(title, "solve")
    
    # Parameter mapping for common methods
    param_map = {
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
        "evalRPN": "tokens",
        "dailyTemperatures": "temperatures",
        "search": "nums, target",
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
        "encode": "strs",
        "trap": "height",
        "maxPathSum": "root",
        "serialize": "root",
        "ladderLength": "beginWord, endWord, wordList",
        "mergeKLists": "lists",
    }
    
    params = param_map.get(method_name, "")
    
    # Create template
    if params:
        template = f"class Solution:\n    def {method_name}(self, {params}):\n        # Your code here\n        pass"
    else:
        template = f"class Solution:\n    def {method_name}(self):\n        # Your code here\n        pass"
    
    return {
        "id": qid,
        "title": title,
        "leetcode_number": leetcode_num,
        "difficulty": difficulty,
        "category": category,
        "description": description_template.format(title=title),
        "examples": [],
        "constraints": ["1 <= n <= 10^4", "Follow standard LeetCode constraints"],
        "template": template,
        "test_cases": [],
        "hints": [f"Think about {category} patterns", "Consider time and space complexity"]
    }

# Complete list from OCR (all 75 problems)
ALL_BLIND_75 = [
    # EASY - Two Pointers & Sliding Window (7)
    ("valid_palindrome", 125, "Valid Palindrome", "Easy", "Two Pointers"),
    ("remove_duplicates_sorted", 26, "Remove Duplicates from Sorted Array", "Easy", "Two Pointers"),
    ("move_zeroes", 283, "Move Zeroes", "Easy", "Two Pointers"),
    ("merge_two_sorted_lists", 21, "Merge Two Sorted Lists", "Easy", "Two Pointers"),
    ("intersection_two_linked_lists", 160, "Intersection of Two Linked Lists", "Easy", "Two Pointers"),
    ("reverse_linked_list", 206, "Reverse Linked List", "Easy", "Two Pointers"),
    ("linked_list_cycle", 141, "Linked List Cycle", "Easy", "Two Pointers"),
    
    # EASY - Hash Table / Set (4)
    ("two_sum", 1, "Two Sum", "Easy", "Hash Table"),
    ("contains_duplicate", 217, "Contains Duplicate", "Easy", "Hash Set"),
    ("valid_anagram", 242, "Valid Anagram", "Easy", "Hash Table"),
    ("first_unique_character", 387, "First Unique Character in a String", "Easy", "Hash Table"),
    
    # EASY - Array / Math (3)
    ("maximum_subarray", 53, "Maximum Subarray", "Easy", "DP"),
    ("best_time_to_buy_sell_stock", 121, "Best Time to Buy and Sell Stock", "Easy", "Two Pointers"),
    ("missing_number", 268, "Missing Number", "Easy", "Math/BitManip"),
    
    # EASY - Stack (1)
    ("valid_parentheses", 20, "Valid Parentheses", "Easy", "Stack"),
    
    # EASY - Tree / Binary Tree (6)
    ("max_depth_binary_tree", 104, "Maximum Depth of Binary Tree", "Easy", "DFS, Tree"),
    ("same_tree", 100, "Same Tree", "Easy", "DFS, Tree"),
    ("symmetric_tree", 101, "Symmetric Tree", "Easy", "DFS/BFS, Tree"),
    ("invert_binary_tree", 226, "Invert Binary Tree", "Easy", "DFS/BFS, Tree"),
    ("subtree_of_another_tree", 572, "Subtree of Another Tree", "Easy", "DFS/BFS, Tree"),
    ("lowest_common_ancestor_bst", 235, "Lowest Common Ancestor of a Binary Search Tree", "Easy", "DFS, Tree"),
    
    # MEDIUM - Two Pointers & Sliding Window (7)
    ("remove_nth_node_end", 19, "Remove Nth Node From End of List", "Medium", "Two Pointers"),
    ("two_sum_ii_sorted", 167, "Two Sum II - Input Array Is Sorted", "Medium", "Two Pointers"),
    ("3sum", 15, "3Sum", "Medium", "Two Pointers"),
    ("longest_substring_no_repeat", 3, "Longest Substring Without Repeating Characters", "Medium", "Sliding Window"),
    ("container_with_most_water", 11, "Container With Most Water", "Medium", "Two Pointers"),
    ("longest_repeating_char_replace", 424, "Longest Repeating Character Replacement", "Medium", "Sliding Window"),
    ("linked_list_cycle_ii", 142, "Linked List Cycle II", "Medium", "Two Pointers"),
    
    # MEDIUM - Hash Table / Set (4)
    ("group_anagrams", 49, "Group Anagrams", "Medium", "Hash Table"),
    ("valid_sudoku", 36, "Valid Sudoku", "Medium", "Hash Table"),
    ("subarray_sum_equals_k", 560, "Subarray Sum Equals K", "Medium", "Hash Map/PSum"),
    ("minimum_window_substring", 76, "Minimum Window Substring", "Medium", "Sliding Window"),
    
    # MEDIUM - Stack / Monotonic Stack (3)
    ("min_stack", 155, "Min Stack", "Medium", "Stack, Design"),
    ("evaluate_reverse_polish_notation", 150, "Evaluate Reverse Polish Notation", "Medium", "Stack"),
    ("daily_temperatures", 739, "Daily Temperatures", "Medium", "Monotonic Stack"),
    
    # MEDIUM - Binary Search (4)
    ("binary_search", 704, "Binary Search", "Medium", "Binary Search"),
    ("find_min_rotated_sorted_array", 153, "Find Minimum in Rotated Sorted Array", "Medium", "Binary Search"),
    ("search_rotated_sorted_array", 33, "Search in Rotated Sorted Array", "Medium", "Binary Search"),
    ("kth_smallest_element_bst", 230, "Kth Smallest Element in a BST", "Medium", "Binary Search"),
    
    # MEDIUM - Linked List (2)
    ("add_two_numbers", 2, "Add Two Numbers", "Medium", "List/Math"),
    ("reorder_list", 143, "Reorder List", "Medium", "Two Pointers"),
    
    # MEDIUM - Tree / Binary Tree (4)
    ("validate_binary_search_tree", 98, "Validate Binary Search Tree", "Medium", "DFS, Tree"),
    ("binary_tree_level_order_traversal", 102, "Binary Tree Level Order Traversal", "Medium", "BFS, Tree"),
    ("construct_binary_tree_pre_inorder", 105, "Construct Binary Tree from Preorder and Inorder Traversal", "Medium", "DFS, Tree"),
    ("lowest_common_ancestor_binary_tree", 236, "Lowest Common Ancestor of a Binary Tree", "Medium", "DFS, Tree"),
    
    # MEDIUM - Graph / BFS / DFS (6)
    ("number_of_islands", 200, "Number of Islands", "Medium", "BFS/DFS, Graph"),
    ("clone_graph", 133, "Clone Graph", "Medium", "BFS/DFS, Graph"),
    ("course_schedule", 207, "Course Schedule", "Medium", "TopoSort, Graph"),
    ("pacific_atlantic_water_flow", 417, "Pacific Atlantic Water Flow", "Medium", "BFS/DFS, Graph"),
    ("graph_valid_tree", 261, "Graph Valid Tree", "Medium", "UnionFind, Graph"),
    ("number_of_connected_components", 323, "Number of Connected Components in an Undirected Graph", "Medium", "UnionFind, Graph"),
    
    # MEDIUM - Backtracking (4)
    ("word_search", 79, "Word Search", "Medium", "Backtracking"),
    ("combination_sum", 39, "Combination Sum", "Medium", "Backtracking"),
    ("subsets", 78, "Subsets", "Medium", "Backtracking"),
    ("permutations", 46, "Permutations", "Medium", "Backtracking"),
    
    # MEDIUM - DP (11)
    ("climbing_stairs", 70, "Climbing Stairs", "Medium", "DP"),
    ("house_robber", 198, "House Robber", "Medium", "DP"),
    ("unique_paths", 62, "Unique Paths", "Medium", "DP"),
    ("coin_change", 322, "Coin Change", "Medium", "DP"),
    ("longest_increasing_subsequence", 300, "Longest Increasing Subsequence", "Medium", "DP"),
    ("decode_ways", 91, "Decode Ways", "Medium", "DP"),
    ("word_break", 139, "Word Break", "Medium", "DP"),
    ("longest_palindromic_substring", 5, "Longest Palindromic Substring", "Medium", "DP / Expand"),
    ("palindromic_substrings", 647, "Palindromic Substrings", "Medium", "DP"),
    ("maximum_product_subarray", 152, "Maximum Product Subarray", "Medium", "DP"),
    ("minimum_path_sum", 64, "Minimum Path Sum", "Medium", "DP"),
    
    # MEDIUM - Arrays / Matrix (3)
    ("rotate_image", 48, "Rotate Image", "Medium", "Array/Matrix"),
    ("spiral_matrix", 54, "Spiral Matrix", "Medium", "Array/Matrix"),
    ("set_matrix_zeroes", 73, "Set Matrix Zeroes", "Medium", "Array/Matrix"),
    
    # MEDIUM - Intervals (2)
    ("merge_intervals", 56, "Merge Intervals", "Medium", "Intervals"),
    ("insert_interval", 57, "Insert Interval", "Medium", "Intervals"),
    
    # MEDIUM - Design (2)
    ("lru_cache", 146, "LRU Cache", "Medium", "Design, Hash"),
    ("encode_decode_strings", 271, "Encode and Decode Strings", "Medium", "Design, String"),
    
    # HARD - Two Pointers & Sliding Window (1)
    ("trapping_rain_water", 42, "Trapping Rain Water", "Hard", "Two Pointers"),
    
    # HARD - Tree / Binary Tree (2)
    ("binary_tree_maximum_path_sum", 124, "Binary Tree Maximum Path Sum", "Hard", "DFS, Tree"),
    ("serialize_deserialize_binary_tree", 297, "Serialize and Deserialize Binary Tree", "Hard", "Design/DFS/BFS"),
    
    # HARD - Graph / BFS / DFS (1)
    ("word_ladder", 127, "Word Ladder", "Hard", "BFS, Graph"),
    
    # HARD - Linked List (1)
    ("merge_k_sorted_lists", 23, "Merge k Sorted Lists", "Hard", "Heap, LinkedList"),
]

def get_all_questions():
    """Generate all 75 questions."""
    questions = {}
    
    for qid, leetcode_num, title, difficulty, category in ALL_BLIND_75:
        # Create description based on title
        description = f"LeetCode {leetcode_num}: {title}. This is a {difficulty} problem in the {category} category."
        
        question = create_question_basic(qid, leetcode_num, title, difficulty, category, description)
        questions[qid] = question
    
    return questions

if __name__ == '__main__':
    questions = get_all_questions()
    print(f"Generated {len(questions)} questions")
    
    # Verify we have exactly 75 unique problems
    unique_leetcode_nums = set(q['leetcode_number'] for q in questions.values())
    print(f"Unique LeetCode problems: {len(unique_leetcode_nums)}")
    
    # Save to file
    with open('questions.json', 'w') as f:
        json.dump(questions, f, indent=2)
    
    print(f"Saved all {len(questions)} questions to questions.json")

