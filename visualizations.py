"""
Hardcoded visual diagrams for all 78 Blind 75 LeetCode problems.
Each function returns a formatted string with ASCII art and step-by-step visualization.
"""

def get_visualization(problem_id, question):
    """Get visualization for a specific problem."""
    examples = question.get('examples', [])
    example_input = examples[0].get('input', 'N/A') if examples else 'N/A'
    example_output = examples[0].get('output', 'N/A') if examples else 'N/A'
    
    # Map problem IDs to visualization functions
    visualizations = {
        # ========== ARRAY / TWO POINTERS ==========
        'two_sum': lambda: f"""STEP 1: Initialize Hash Map
nums = [2, 7, 11, 15], target = 9
      ↑i=0
seen = {{}}  (empty hash map)

STEP 2: Check First Number (2)
nums = [2, 7, 11, 15]
      ↑i=0
complement = 9 - 2 = 7
Is 7 in seen? NO
seen = {{2: 0}}  (store value → index)

STEP 3: Check Second Number (7)
nums = [2, 7, 11, 15]
         ↑i=1
complement = 9 - 7 = 2
Is 2 in seen? YES! ✓
seen[2] = 0 (found at index 0)

STEP 4: Return Result
nums = [2, 7, 11, 15]
      ✓0   ✓1
Pair found: [0, 1]
Calculation: nums[0] + nums[1] = 2 + 7 = 9 ✓

STEP 5: Time Complexity
O(n) - single pass through array
O(n) space - hash map storage
""",

        'two_sum_ii_sorted': lambda: f"""STEP 1: Initialize Two Pointers
nums = {example_input}, target = 9
       ↑L                       R↑
left = 0, right = len-1

STEP 2: Check Sum
nums[L] + nums[R] = ?
if sum == target: return [L+1, R+1]

STEP 3: Adjust Pointers
if sum < target: left++ →
if sum > target: right-- ←

STEP 4: Found
nums = {example_input}
          ✓         ✓
Result = {example_output}
""",

        '3sum': lambda: f"""STEP 1: Sort Array First
Original: [-1, 0, 1, 2, -1, -4]
Sorted:   [-4, -1, -1, 0, 1, 2]
          ↑i=0

STEP 2: Fix i=0, Search with Two Pointers
nums = [-4, -1, -1,  0,  1,  2]
        ↑i   ↑L              ↑R
i=0 (val=-4), L=1 (val=-1), R=5 (val=2)
sum = -4 + (-1) + 2 = -3 (too small)
Action: L++ (move left pointer right →)

STEP 3: Continue Search (i=0)
nums = [-4, -1, -1,  0,  1,  2]
        ↑i       ↑L          ↑R
sum = -4 + (-1) + 2 = -3 (still too small)
Action: L++ →

STEP 4: Move to i=1, Find Match!
nums = [-4, -1, -1,  0,  1,  2]
            ↑i   ↑L          ↑R
i=1 (val=-1), L=2 (val=-1), R=5 (val=2)
sum = -1 + (-1) + 2 = 0 ✓ FOUND!
triplet = [-1, -1, 2]

STEP 5: Continue & Skip Duplicates
nums = [-4, -1, -1,  0,  1,  2]
            ↑i       ↑L      ↑R
Skip duplicate -1, move L and R
Find more: [-1, 0, 1]

STEP 6: All Triplets Found
Result = [[-1, -1, 2], [-1, 0, 1]]
Time: O(n²), Space: O(1)
""",

        'container_with_most_water': lambda: f"""STEP 1: Two Pointers
height = {example_input}
         ↑L                 R↑
left = 0, right = len-1

STEP 2: Calculate Area
width = right - left
h = min(height[L], height[R])
area = width × h

STEP 3: Move Shorter
if height[L] < height[R]:
   left++ →
else:
   right-- ←

STEP 4: Max Area
maxArea = {example_output}
""",

        'valid_palindrome': lambda: f"""STEP 1: Clean & Two Pointers
s = {example_input}
    ↑L              R↑
Filter alphanumeric, lowercase

STEP 2: Compare Characters
if s[L] != s[R]:
   return False

STEP 3: Move Inward
   left++ →
← right--

STEP 4: Result
All matched = {example_output}
""",

        'remove_duplicates_sorted': lambda: f"""STEP 1: Slow/Fast Pointers
nums = {example_input}
       ↑slow ↑fast

STEP 2: Skip Duplicates
nums = [1, 1, 2, 2, 3]
       ↑s    ↑f
if nums[f] == nums[s]: f++

STEP 3: Place Unique
nums = [1, 1, 2, 2, 3]
       ↑s       ↑f
nums[s+1] = nums[f]

STEP 4: Result
nums = [1, 2, 3, _, _]
length = {example_output}
""",

        'move_zeroes': lambda: f"""STEP 1: Slow/Fast Pointers
nums = {example_input}
       ↑slow ↑fast

STEP 2: Move Non-Zero
if nums[fast] != 0:
   nums[slow] = nums[fast]
   slow++

STEP 3: Fill Zeros
nums = [1, 3, 12, _, _]
                  ↑slow
Fill rest with 0

STEP 4: Result
nums = {example_output}
""",

        'trapping_rain_water': lambda: f"""STEP 1: Two Pointers + Max Heights
height = {example_input}
         ↑L                  R↑
leftMax = 0, rightMax = 0

STEP 2: Process Lower Side
if leftMax < rightMax:
   water += max(0, leftMax - height[L])
   left++ →

STEP 3: Update Max
leftMax = max(leftMax, height[L])
rightMax = max(rightMax, height[R])

STEP 4: Total Water
water = {example_output}
""",

        # ========== HASH TABLE ==========
        'contains_duplicate': lambda: f"""STEP 1: Initialize Set
nums = {example_input}
       ↑
seen = set()

STEP 2: Check Each
if nums[i] in seen:
   return True
seen.add(nums[i])

STEP 3: Scan Array
nums = {example_input}
          ↑
Check all elements

STEP 4: Result
hasDuplicate = {example_output}
""",

        'valid_anagram': lambda: f"""STEP 1: Count Characters
s = {example_input}
    ↑
count = {{}}

STEP 2: Build Frequency Map
for c in s:
   count[c] = count.get(c, 0) + 1

STEP 3: Compare with t
for c in t:
   if c not in count: return False
   count[c] -= 1

STEP 4: Result
isAnagram = {example_output}
""",

        'group_anagrams': lambda: f"""STEP 1: Hash by Sorted Key
strs = {example_input}
groups = {{}}

STEP 2: Sort Each Word
"eat" → "aet"
"tea" → "aet" (same key!)

STEP 3: Group by Key
groups["aet"] = ["eat", "tea", "ate"]

STEP 4: Result
{example_output}
""",

        'first_unique_character': lambda: f"""STEP 1: Count Frequency
s = {example_input}
    ↑
count = {{}}

STEP 2: Build Map
count = {{'l':1, 'e':3, 't':1, ...}}

STEP 3: Find First Unique
for i, c in enumerate(s):
   if count[c] == 1:
      return i

STEP 4: Result
index = {example_output}
""",

        'valid_sudoku': lambda: f"""STEP 1: Track Seen Values
rows = [set() for _ in range(9)]
cols = [set() for _ in range(9)]
boxes = [set() for _ in range(9)]

STEP 2: Check Each Cell
board[r][c] = val
if val in rows[r]: return False
if val in cols[c]: return False

STEP 3: Check 3x3 Box
box_id = (r//3)*3 + (c//3)
if val in boxes[box_id]: return False

STEP 4: Result
isValid = {example_output}
""",

        # ========== STACK ==========
        'valid_parentheses': lambda: f"""STEP 1: Initialize Stack
s = "([)]"
    ↑i=0
stack = []  (empty)

STEP 2: Process '(' (opening)
s = "([)]"
    ↑i=0
'(' is opening → push
stack = ['(']

STEP 3: Process '[' (opening)
s = "([)]"
      ↑i=1
'[' is opening → push
stack = ['(', '[']

STEP 4: Process ')' (closing)
s = "([)]"
        ↑i=2
')' should match stack.top() = '['
'(' ≠ '[' → MISMATCH! ✗

STEP 5: Valid Example
"([])" works:
[] → ['('] → ['(','['] → ['('] → []
All matched! ✓

STEP 6: Rules
Opening: push, Closing: pop & match
Time: O(n), Space: O(n)
""",

        'min_stack': lambda: f"""STEP 1: Two Stacks
stack = []
minStack = []

STEP 2: Push
push(5):
   stack = [5]
   minStack = [5]

STEP 3: Push Smaller
push(2):
   stack = [5, 2]
   minStack = [5, 2]

STEP 4: Get Min
getMin() = minStack[-1]
O(1) time!
""",

        'evaluate_reverse_polish_notation': lambda: f"""STEP 1: Stack Processing
tokens = {example_input}
         ↑
stack = []

STEP 2: Numbers
token = "2"
stack.push(2)

STEP 3: Operators
token = "+"
b = stack.pop()
a = stack.pop()
stack.push(a + b)

STEP 4: Result
stack = [{example_output}]
""",

        'daily_temperatures': lambda: f"""STEP 1: Monotonic Stack
temps = {example_input}
        ↑
stack = [], result = [0,0,0,...]

STEP 2: Process Each Day
stack = [(index, temp)]
Keep decreasing temps

STEP 3: Found Warmer
if temps[i] > stack.top():
   pop and calculate days

STEP 4: Result
days = {example_output}
""",

        # ========== BINARY SEARCH ==========
        'binary_search': lambda: f"""STEP 1: Initialize Search Space
nums = [-1, 0, 3, 5, 9, 12], target = 9
       ↑L              ↑M              ↑R
left = 0, right = 5, mid = (0+5)//2 = 2

STEP 2: First Check (mid=2)
nums = [-1, 0, 3, 5, 9, 12]
       ↑L      ↑M          ↑R
nums[2] = 3
Is 3 == 9? NO
Is 3 < 9? YES → search right half
left = mid + 1 = 3

STEP 3: Second Check (mid=4)
nums = [-1, 0, 3, 5, 9, 12]
                   ↑L ↑M  ↑R
mid = (3+5)//2 = 4
nums[4] = 9
Is 9 == 9? YES! ✓ FOUND!

STEP 4: Return Index
nums = [-1, 0, 3, 5, 9, 12]
                      ✓4
Target 9 found at index 4

STEP 5: Complexity
Time: O(log n) - halve search space each step
Space: O(1) - only use pointers
""",

        'find_min_rotated_sorted_array': lambda: f"""STEP 1: Binary Search
nums = {example_input}
       ↑L    M       R↑

STEP 2: Check Which Half Sorted
if nums[mid] > nums[right]:
   min in right half →
else:
   min in left half ←

STEP 3: Narrow Down
Adjust pointers based on rotation

STEP 4: Minimum
min = {example_output}
""",

        'search_rotated_sorted_array': lambda: f"""STEP 1: Find Pivot
nums = {example_input}
       ↑L    M       R↑
Determine which half sorted

STEP 2: Check Sorted Half
if left half sorted:
   if target in range:
      search left
   else:
      search right

STEP 3: Binary Search
Continue narrowing

STEP 4: Result
index = {example_output}
""",

        # ========== LINKED LIST ==========
        'reverse_linked_list': lambda: f"""STEP 1: Initialize Pointers
1 → 2 → 3 → 4 → None
↑prev ↑curr

STEP 2: Reverse Link
1 ← 2   3 → 4 → None
    ↑curr ↑next

STEP 3: Move Forward
1 ← 2 ← 3   4 → None
        ↑curr ↑next

STEP 4: Result
4 → 3 → 2 → 1 → None
{example_output}
""",

        'merge_two_sorted_lists': lambda: f"""STEP 1: Dummy Node
l1: 1 → 4 → 5
l2: 1 → 3 → 4
dummy →

STEP 2: Compare & Merge
if l1.val < l2.val:
   tail.next = l1
   l1 = l1.next

STEP 3: Continue
dummy → 1 → 1 → 3 → 4 → 4 → 5

STEP 4: Result
{example_output}
""",

        'linked_list_cycle': lambda: f"""STEP 1: Floyd's Algorithm
slow = head
fast = head

STEP 2: Move Pointers
slow: 1 → 2 → 3 → 4
             ↑slow
fast: 1 → 2 → 3 → 4 → 2
                      ↑fast

STEP 3: Detect Cycle
if slow == fast:
   return True

STEP 4: Result
hasCycle = {example_output}
""",

        'add_two_numbers': lambda: f"""STEP 1: Initialize
l1: 2 → 4 → 3
l2: 5 → 6 → 4
carry = 0

STEP 2: Add Digits
sum = l1.val + l2.val + carry
digit = sum % 10
carry = sum // 10

STEP 3: Build Result
result: 7 → 0 → 8

STEP 4: Output
{example_output}
""",

        'remove_nth_node_end': lambda: f"""STEP 1: Two Pointers (Gap = n)
dummy → 1 → 2 → 3 → 4 → 5
        ↑slow    ↑fast

STEP 2: Move Fast n Steps
dummy → 1 → 2 → 3 → 4 → 5
        ↑slow           ↑fast

STEP 3: Move Together
dummy → 1 → 2 → 3 → 4 → 5 → None
               ↑slow       ↑fast

STEP 4: Remove
slow.next = slow.next.next
""",

        'reorder_list': lambda: f"""STEP 1: Find Middle
1 → 2 → 3 → 4 → 5
         ↑mid

STEP 2: Reverse Second Half
1 → 2 → 3 ← 4 ← 5

STEP 3: Merge Alternately
1 → 5 → 2 → 4 → 3

STEP 4: Result
{example_output}
""",

        'merge_k_sorted_lists': lambda: f"""STEP 1: Min Heap
lists = [[1,4,5], [1,3,4], [2,6]]
heap = [(1,0), (1,1), (2,2)]

STEP 2: Pop Minimum
val, idx = heappop(heap)
Add to result

STEP 3: Add Next from List
if lists[idx]:
   heappush(heap, (lists[idx][0], idx))

STEP 4: Result
{example_output}
""",

        # ========== SLIDING WINDOW ==========
        'longest_substring_no_repeat': lambda: f"""STEP 1: Sliding Window
s = {example_input}
    ↑L ↑R
seen = {{}}

STEP 2: Expand Window
if s[R] not in seen:
   seen.add(s[R])
   R++ →

STEP 3: Shrink on Duplicate
if s[R] in seen:
   seen.remove(s[L])
   L++ →

STEP 4: Max Length
maxLen = {example_output}
""",

        'longest_repeating_char_replace': lambda: f"""STEP 1: Window + Count
s = {example_input}, k = 2
    ↑L ↑R
count = {{}}

STEP 2: Expand
windowLen - maxFreq <= k:
   valid window

STEP 3: Shrink
if invalid:
   count[s[L]] -= 1
   L++ →

STEP 4: Max Length
maxLen = {example_output}
""",

        'minimum_window_substring': lambda: f"""STEP 1: Two Pointers
s = {example_input}, t = "ABC"
    ↑L                      R↑
need = {{'A':1, 'B':1, 'C':1}}

STEP 2: Expand Until Valid
have all chars from t

STEP 3: Shrink While Valid
L++ → minimize window

STEP 4: Minimum
minWindow = {example_output}
""",

        # ========== DYNAMIC PROGRAMMING ==========
        'climbing_stairs': lambda: f"""STEP 1: Bottom-Up DP Setup
n = 5 (want to reach stair 5)
dp[i] = ways to reach stair i
dp = [0, 0, 0, 0, 0, 0]

STEP 2: Base Cases
dp[0] = 1 (one way: stay at ground)
dp[1] = 1 (one way: one step)
dp = [1, 1, 0, 0, 0, 0]

STEP 3: Fill DP Table
For stair 2:
  dp[2] = dp[1] + dp[0] = 1 + 1 = 2
  (can come from stair 1 or stair 0)
dp = [1, 1, 2, 0, 0, 0]

STEP 4: Continue Building
dp[3] = dp[2] + dp[1] = 2 + 1 = 3
dp[4] = dp[3] + dp[2] = 3 + 2 = 5
dp[5] = dp[4] + dp[3] = 5 + 3 = 8
dp = [1, 1, 2, 3, 5, 8]

STEP 5: Final Answer
dp[5] = 8 ways to reach stair 5
Pattern: Fibonacci sequence!
Time: O(n), Space: O(n)
""",

        'house_robber': lambda: f"""STEP 1: DP Array
nums = {example_input}
dp[i] = max money up to house i

STEP 2: Recurrence
dp[i] = max(
   dp[i-1],        # skip
   dp[i-2] + nums[i]  # rob
)

STEP 3: Fill Table
dp = [2, 7, 9, 12]

STEP 4: Max Money
dp[-1] = {example_output}
""",

        'coin_change': lambda: f"""STEP 1: DP Array
coins = {example_input}, amount = 11
dp[i] = min coins for amount i

STEP 2: Initialize
dp[0] = 0
dp[other] = infinity

STEP 3: For Each Amount
for coin in coins:
   dp[i] = min(dp[i], dp[i-coin] + 1)

STEP 4: Result
dp[amount] = {example_output}
""",

        'longest_increasing_subsequence': lambda: f"""STEP 1: DP Array
nums = {example_input}
dp[i] = LIS ending at i

STEP 2: For Each Position
for j < i:
   if nums[j] < nums[i]:
      dp[i] = max(dp[i], dp[j] + 1)

STEP 3: Build LIS
dp = [1, 1, 2, 2, 3, 4]

STEP 4: Max LIS
max(dp) = {example_output}
""",

        'maximum_subarray': lambda: f"""STEP 1: Kadane's Algorithm
nums = {example_input}
       ↑
maxSum = nums[0]
currSum = 0

STEP 2: For Each Element
currSum = max(nums[i], currSum + nums[i])

STEP 3: Track Maximum
maxSum = max(maxSum, currSum)

STEP 4: Result
maxSum = {example_output}
""",

        'word_break': lambda: f"""STEP 1: DP Array
s = {example_input}
dp[i] = can break s[0:i]

STEP 2: Base Case
dp[0] = True

STEP 3: Check Substrings
for j < i:
   if dp[j] and s[j:i] in wordDict:
      dp[i] = True

STEP 4: Result
dp[len(s)] = {example_output}
""",

        'decode_ways': lambda: f"""STEP 1: DP Array
s = {example_input}
dp[i] = ways to decode s[0:i]

STEP 2: Single Digit
if s[i] != '0':
   dp[i] += dp[i-1]

STEP 3: Two Digits
if 10 <= int(s[i-1:i+1]) <= 26:
   dp[i] += dp[i-2]

STEP 4: Total Ways
dp[-1] = {example_output}
""",

        'unique_paths': lambda: f"""STEP 1: DP Grid
m x n grid
dp[i][j] = paths to (i,j)

STEP 2: Base Cases
dp[0][j] = 1 (top row)
dp[i][0] = 1 (left col)

STEP 3: Fill Table
dp[i][j] = dp[i-1][j] + dp[i][j-1]

STEP 4: Result
dp[m-1][n-1] = {example_output}
""",

        'minimum_path_sum': lambda: f"""STEP 1: DP Grid
grid = {example_input}
dp[i][j] = min sum to (i,j)

STEP 2: Base Case
dp[0][0] = grid[0][0]

STEP 3: Recurrence
dp[i][j] = grid[i][j] + min(
   dp[i-1][j],
   dp[i][j-1]
)

STEP 4: Result
dp[m-1][n-1] = {example_output}
""",

        'maximum_product_subarray': lambda: f"""STEP 1: Track Min & Max
nums = {example_input}
       ↑
maxProd = nums[0]
minProd = nums[0]

STEP 2: For Each Element
temp = maxProd
maxProd = max(nums[i], maxProd*nums[i], minProd*nums[i])
minProd = min(nums[i], temp*nums[i], minProd*nums[i])

STEP 3: Track Global Max
result = max(result, maxProd)

STEP 4: Result
maxProduct = {example_output}
""",

        # ========== TREE (DFS/BFS) ==========
        'max_depth_binary_tree': lambda: f"""STEP 1: Recursive DFS
    3
   / \\
  9  20
    /  \\
   15   7

STEP 2: Base Case
if not root:
   return 0

STEP 3: Recursive Call
left = maxDepth(root.left)
right = maxDepth(root.right)

STEP 4: Result
depth = 1 + max(left, right)
{example_output}
""",

        'invert_binary_tree': lambda: f"""STEP 1: Original Tree
    4
   / \\
  2   7
 / \\ / \\
1  3 6  9

STEP 2: Swap Children
swap(root.left, root.right)

STEP 3: Recurse
invert(root.left)
invert(root.right)

STEP 4: Inverted Tree
    4
   / \\
  7   2
 / \\ / \\
9  6 3  1
""",

        'same_tree': lambda: f"""STEP 1: Compare Roots
p:   1        q:   1
    / \\           / \\
   2   3         2   3

STEP 2: Base Cases
if not p and not q: return True
if not p or not q: return False

STEP 3: Check Value
if p.val != q.val: return False

STEP 4: Recurse
return same(p.left, q.left) and
       same(p.right, q.right)
{example_output}
""",

        'symmetric_tree': lambda: f"""STEP 1: Mirror Check
    1
   / \\
  2   2
 / \\ / \\
3  4 4  3

STEP 2: Compare Left & Right
isMirror(left, right)

STEP 3: Conditions
left.val == right.val
isMirror(left.left, right.right)
isMirror(left.right, right.left)

STEP 4: Result
isSymmetric = {example_output}
""",

        'subtree_of_another_tree': lambda: f"""STEP 1: Find Matching Root
Tree s:     Tree t:
    3          4
   / \\        / \\
  4   5      1   2
 / \\
1   2

STEP 2: Check If Same
if sameTree(s, t):
   return True

STEP 3: Recurse
return isSubtree(s.left, t) or
       isSubtree(s.right, t)

STEP 4: Result
{example_output}
""",

        'lowest_common_ancestor_bst': lambda: f"""STEP 1: BST Property
    6
   / \\
  2   8
 / \\ / \\
0  4 7  9
   / \\
  3   5

STEP 2: Compare with Root
if p.val < root.val and q.val < root.val:
   search left

STEP 3: Found LCA
if p.val <= root.val <= q.val:
   return root

STEP 4: Result
LCA = {example_output}
""",

        'validate_binary_search_tree': lambda: f"""STEP 1: DFS with Range
    5
   / \\
  1   8
     / \\
    6   9
Valid range: (-∞, ∞)

STEP 2: Check Node
if not (low < root.val < high):
   return False

STEP 3: Recurse with Range
left: (low, root.val)
right: (root.val, high)

STEP 4: Result
isValidBST = {example_output}
""",

        'binary_tree_level_order_traversal': lambda: f"""STEP 1: BFS with Queue
    3
   / \\
  9  20
    /  \\
   15   7
queue = [root]

STEP 2: Process Level
for _ in range(len(queue)):
   node = queue.pop(0)
   level.append(node.val)

STEP 3: Add Children
queue.extend([left, right])

STEP 4: Result
levels = {example_output}
""",

        'kth_smallest_element_bst': lambda: f"""STEP 1: Inorder Traversal
    3
   / \\
  1   4
   \\
    2
Inorder: [1, 2, 3, 4]

STEP 2: DFS (Left → Root → Right)
result = []
dfs(root.left)
result.append(root.val)
dfs(root.right)

STEP 3: Kth Element
return result[k-1]

STEP 4: Result
{example_output}
""",

        'construct_binary_tree_pre_inorder': lambda: f"""STEP 1: Identify Root
preorder = [3,9,20,15,7]
           ↑root
inorder = [9,3,15,20,7]

STEP 2: Split Inorder
left: [9]
right: [15,20,7]

STEP 3: Recurse
root.left = build(pre[1:mid], in[:mid])
root.right = build(pre[mid:], in[mid+1:])

STEP 4: Tree Built
    3
   / \\
  9  20
    /  \\
   15   7
""",

        'lowest_common_ancestor_binary_tree': lambda: f"""STEP 1: DFS Search
    3
   / \\
  5   1
 / \\
6   2

STEP 2: Base Case
if root == p or root == q:
   return root

STEP 3: Search Both Sides
left = LCA(root.left, p, q)
right = LCA(root.right, p, q)

STEP 4: Determine LCA
if left and right:
   return root
return left or right
""",

        'binary_tree_maximum_path_sum': lambda: f"""STEP 1: DFS with Max Tracking
    -10
    /  \\
   9    20
       /  \\
      15   7
maxSum = -∞

STEP 2: Calculate Path Through Node
left = max(0, dfs(root.left))
right = max(0, dfs(root.right))
pathSum = root.val + left + right

STEP 3: Update Global Max
maxSum = max(maxSum, pathSum)

STEP 4: Return to Parent
return root.val + max(left, right)
{example_output}
""",

        'serialize_deserialize_binary_tree': lambda: f"""STEP 1: Serialize (Pre-order)
    1
   / \\
  2   3
     / \\
    4   5
"1,2,None,None,3,4,None,None,5,None,None"

STEP 2: Use Delimiter
values = tree_to_string(root)

STEP 3: Deserialize
data = "1,2,None,None,3,4..."
Build tree from string

STEP 4: Reconstruct
root = build_from_list(values)
""",

        # ========== GRAPH (BFS/DFS) ==========
        'number_of_islands': lambda: f"""STEP 1: Grid Traversal
grid = [
  ["1","1","0"],
  ["0","1","0"],
  ["1","0","1"]
]
count = 0

STEP 2: Find Land
if grid[i][j] == "1":
   count += 1
   dfs(i, j)  # Mark connected

STEP 3: DFS to Mark Island
grid[i][j] = "0"
dfs(i±1, j±1)  # 4 directions

STEP 4: Total Islands
count = {example_output}
""",

        'clone_graph': lambda: f"""STEP 1: BFS/DFS with Map
1 --- 2
|     |
4 --- 3
visited = {{}}

STEP 2: Clone Node
cloned = Node(node.val)
visited[node] = cloned

STEP 3: Clone Neighbors
for neighbor in node.neighbors:
   if neighbor not in visited:
      clone(neighbor)

STEP 4: Connect
cloned.neighbors.append(visited[neighbor])
""",

        'course_schedule': lambda: f"""STEP 1: Build Graph
numCourses = 4
prerequisites = [[1,0],[2,1],[3,2]]
graph = {{0:[1], 1:[2], 2:[3]}}

STEP 2: Topological Sort (BFS)
indegree = [0, 1, 1, 1]
queue = [0]  # courses with 0 deps

STEP 3: Process Courses
for course in queue:
   for next_course in graph[course]:
      indegree[next_course] -= 1
      if indegree[next_course] == 0:
         queue.append(next_course)

STEP 4: Can Finish?
len(queue) == numCourses
{example_output}
""",

        'pacific_atlantic_water_flow': lambda: f"""STEP 1: Two DFS from Edges
Pacific: top & left edges
Atlantic: bottom & right edges

STEP 2: DFS from Pacific
Mark all cells reachable

STEP 3: DFS from Atlantic
Mark all cells reachable

STEP 4: Intersection
cells in both sets
{example_output}
""",

        'graph_valid_tree': lambda: f"""STEP 1: Tree Properties
n nodes, must have n-1 edges
Must be fully connected
No cycles

STEP 2: Build Adjacency List
edges = [[0,1],[0,2],[0,3],[1,4]]

STEP 3: DFS with Visited
Check if all nodes reachable

STEP 4: Valid Tree?
visited all && no cycles
{example_output}
""",

        'number_of_connected_components': lambda: f"""STEP 1: Union-Find
n = 5
edges = [[0,1],[1,2],[3,4]]
parent = [0,1,2,3,4]

STEP 2: Union Operation
for u, v in edges:
   union(u, v)

STEP 3: Find Connected
parent = [0,0,0,3,3]

STEP 4: Count Components
unique parents = {example_output}
""",

        'word_ladder': lambda: f"""STEP 1: BFS in Word Graph
beginWord = "hit"
endWord = "cog"
wordList = ["hot","dot","dog","cog"]

STEP 2: Transform One Char
hit → hot → dot → dog → cog

STEP 3: BFS Queue
queue = [(word, level)]

STEP 4: Shortest Path
transformations = {example_output}
""",

        # ========== BACKTRACKING ==========
        'word_search': lambda: f"""STEP 1: DFS + Backtracking
board = [['A','B'],['C','D']]
word = "ABCD"

STEP 2: Try Each Cell
for i, j in board:
   if dfs(i, j, 0):
      return True

STEP 3: DFS
if board[i][j] == word[idx]:
   mark visited
   dfs(i±1, j±1, idx+1)
   unmark (backtrack)

STEP 4: Found?
{example_output}
""",

        'combination_sum': lambda: f"""STEP 1: Backtracking
candidates = {example_input}
target = 7
result = []

STEP 2: Try Each Candidate
for c in candidates:
   if c <= remaining:
      path.append(c)
      dfs(remaining - c)

STEP 3: Backtrack
path.pop()

STEP 4: Combinations
{example_output}
""",

        'subsets': lambda: f"""STEP 1: Backtracking
nums = {example_input}
result = [[]]

STEP 2: For Each Element
include or exclude

STEP 3: Build Subsets
[] → [1] → [1,2] → [1,2,3]
         → [1,3]
    → [2] → [2,3]
    → [3]

STEP 4: All Subsets
{example_output}
""",

        'permutations': lambda: f"""STEP 1: Backtracking
nums = {example_input}
result = []

STEP 2: Swap & Recurse
for i in range(start, len(nums)):
   swap(start, i)
   backtrack(start+1)
   swap(start, i)  # backtrack

STEP 3: Base Case
if start == len(nums):
   result.append(nums[:])

STEP 4: All Permutations
{example_output}
""",

        # ========== INTERVALS ==========
        'merge_intervals': lambda: f"""STEP 1: Sort by Start
intervals = {example_input}
sorted: [[1,3],[2,6],[8,10],[15,18]]

STEP 2: Merge Overlapping
merged = [[1,3]]
if intervals[i][0] <= merged[-1][1]:
   merged[-1][1] = max(merged[-1][1], intervals[i][1])

STEP 3: Add Non-Overlapping
else:
   merged.append(intervals[i])

STEP 4: Result
{example_output}
""",

        'insert_interval': lambda: f"""STEP 1: Three Parts
intervals = {example_input}
newInterval = [2,5]

STEP 2: Before New
Add all intervals ending before new starts

STEP 3: Merge Overlapping
Merge all overlapping intervals

STEP 4: After New
Add remaining intervals
{example_output}
""",

        # ========== DESIGN ==========
        'lru_cache': lambda: f"""STEP 1: Hash + Doubly Linked List
capacity = 2
cache = {{}}
list: head ↔ tail

STEP 2: Get(key)
Move to front (most recent)

STEP 3: Put(key, val)
Add to front
If over capacity: remove tail

STEP 4: O(1) Operations
Hash for lookup
List for ordering
""",

        'encode_decode_strings': lambda: f"""STEP 1: Encode
strs = ["Hello","World"]
encoded = "5#Hello5#World"
length + delimiter + string

STEP 2: Decode
Read length: 5
Read delimiter: #
Read 5 chars: "Hello"

STEP 3: Handle Edge Cases
Empty strings: "0#"
Delimiters in string: OK!

STEP 4: Result
decoded = {example_output}
""",

        # ========== MATRIX ==========
        'rotate_image': lambda: f"""STEP 1: Transpose
[1,2,3]    [1,4,7]
[4,5,6] → [2,5,8]
[7,8,9]    [3,6,9]

STEP 2: Reverse Each Row
[1,4,7]    [7,4,1]
[2,5,8] → [8,5,2]
[3,6,9]    [9,6,3]

STEP 3: In-Place
swap(i,j) ↔ (j,i)

STEP 4: Rotated 90°
{example_output}
""",

        'spiral_matrix': lambda: f"""STEP 1: Boundaries
matrix = {example_input}
top=0, bottom=rows-1
left=0, right=cols-1

STEP 2: Right →
for j in range(left, right+1)

STEP 3: Down ↓, Left ←, Up ↑
Adjust boundaries after each direction

STEP 4: Spiral Order
{example_output}
""",

        'set_matrix_zeroes': lambda: f"""STEP 1: Mark Rows & Cols
matrix = {example_input}
rows = set()
cols = set()

STEP 2: Find Zeros
if matrix[i][j] == 0:
   rows.add(i)
   cols.add(j)

STEP 3: Set Zeros
for i in rows:
   set row i to 0
for j in cols:
   set col j to 0

STEP 4: Result
{example_output}
""",

        # ========== MISC ==========
        'missing_number': lambda: f"""STEP 1: Expected Sum
n = {example_input}
expected = n * (n+1) / 2

STEP 2: Actual Sum
actual = sum(nums)

STEP 3: Missing
missing = expected - actual

STEP 4: Result
{example_output}
""",

        'longest_palindromic_substring': lambda: f"""STEP 1: Expand Around Center
s = {example_input}
    ↑
Try each position as center

STEP 2: Odd Length
expand from single char

STEP 3: Even Length
expand from between two chars

STEP 4: Longest
maxLen palindrome = {example_output}
""",

        'palindromic_substrings': lambda: f"""STEP 1: Expand Around Each Center
s = {example_input}
    ↑

STEP 2: Count Palindromes
For each center:
   expand while s[L] == s[R]
   count++

STEP 3: Both Odd & Even
Single char centers
Two char centers

STEP 4: Total Count
{example_output}
""",

        # ========== TWO POINTERS (Linked List) ==========
        'intersection_two_linked_lists': lambda: f"""STEP 1: Two Pointers
listA: 4 → 1 → 8 → 4 → 5
listB: 5 → 6 → 1 → 8 → 4 → 5
                  ↑ intersection

STEP 2: Equal Length Trick
pA = headA, pB = headB
When pA reaches end, jump to headB
When pB reaches end, jump to headA

STEP 3: Meet at Intersection
pA == pB at intersection node

STEP 4: Result
{example_output}
""",

        'linked_list_cycle_ii': lambda: f"""STEP 1: Floyd's (Find Cycle)
slow, fast pointers
Meet inside cycle

STEP 2: Find Entry Point
slow = head
Keep fast at meeting point

STEP 3: Move Both One Step
while slow != fast:
   slow = slow.next
   fast = fast.next

STEP 4: Entry Node
{example_output}
""",

        # ========== MATH / BITMANIP ==========
        'subarray_sum_equals_k': lambda: f"""STEP 1: Prefix Sum + Hash
nums = {example_input}, k = 7
prefixSum = 0
map = {{0: 1}}

STEP 2: For Each Element
prefixSum += nums[i]
if (prefixSum - k) in map:
   count += map[prefixSum - k]

STEP 3: Update Map
map[prefixSum] += 1

STEP 4: Count
{example_output}
""",
    }
    
    # Get visualization function, fallback to generic
    vis_func = visualizations.get(problem_id, lambda: get_generic_visualization(example_input, example_output))
    return vis_func()


def get_generic_visualization(example_input, example_output):
    """Generic fallback visualization."""
    return f"""STEP 1: Understand Input
data = {example_input}
       ↑
Analyze the problem

STEP 2: Choose Approach
Consider data structures:
- Array/Hash for O(1) lookup
- Stack for LIFO
- Queue for FIFO
- Heap for priority

STEP 3: Implement Logic
Process elements step by step
Track state and results

STEP 4: Edge Cases
Handle empty, single, extreme

STEP 5: Output
result = {example_output}
"""

