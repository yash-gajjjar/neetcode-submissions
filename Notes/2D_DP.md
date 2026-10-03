# 2-D Dynamic Programming — DSA Interview Notes
*2-Dimensional DP Fundamentals · 0/1 Knapsack · Unbounded Knapsack · Longest Common Subsequence (LCS)*

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the diagrams by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each section.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right technique in <10 seconds.

All code examples in Python.

---

## 🔑 Cheat Sheet — All Four Sections at a Glance
| Section | State Definition | Time | Space (optimized) |
|---|---|---|---|
| 2-D DP Fundamentals | `dp[i][j]` = answer considering position `(i, j)` (e.g., a grid cell) | O(rows × cols) | O(cols) — one row at a time |
| 0/1 Knapsack | `dp[i][w]` = best value using first `i` items with capacity `w`, each item used **at most once** | O(n × capacity) | O(capacity) — 1D array, iterate weight **backward** |
| Unbounded Knapsack | Same shape, but items can be **reused unlimited times** | O(n × capacity) | O(capacity) — 1D array, iterate weight **forward** |
| LCS | `dp[i][j]` = length of the longest common subsequence between `text1[:i]` and `text2[:j]` | O(m × n) | O(min(m, n)) — two rolling rows |

**Core shared idea:** 2-D DP extends the same "define state, find recurrence, build bottom-up" idea from 1-D DP, but the state now needs **two dimensions** to fully describe a subproblem — either because you're navigating a literal 2D grid, or because you're tracking two independent quantities at once (items considered so far + remaining capacity; or progress through two separate sequences).

---

# 1. 2-Dimensional DP Fundamentals

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| State definition | `dp[i][j]` = answer to the subproblem ending at (or using up to) row `i`, column `j` |
| Common context | Grid traversal problems (paths, min/max cost) |
| Recurrence direction | Usually built from top-left to bottom-right, since each cell depends on the cell(s) above/to the left |
| Space optimization | If `dp[i][j]` only depends on row `i-1` (not further back), keep just the **previous row** instead of the full grid |

## Core Intuition
Grid-based DP problems ask: "how many ways / what's the min or max cost to get from the top-left to some cell, given you can only move right and/or down?" Each cell's answer is built from the cells that could have led into it — directly analogous to 1-D DP's `dp[i] = f(dp[i-1], dp[i-2], ...)`, just with two indices instead of one.

```
Unique Paths (only right/down moves allowed), 3x3 grid:

dp[i][j] = dp[i-1][j] + dp[i][j-1]   (ways to reach (i,j) = ways from above + ways from left)

1  1  1
1  2  3
1  3  6     ← dp[2][2] = dp[1][2] + dp[2][1] = 3 + 3 = 6
```

## Worked Pattern: Unique Paths
```python
def uniquePaths(m, n):
    dp = [[1] * n for _ in range(m)]     # first row and first column are all 1 (only one way to reach them)
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]
```
**Space-optimized version (only needs the previous row):**
```python
def uniquePaths_optimized(m, n):
    prev_row = [1] * n
    for i in range(1, m):
        curr_row = [1] * n
        for j in range(1, n):
            curr_row[j] = curr_row[j - 1] + prev_row[j]
        prev_row = curr_row
    return prev_row[n - 1]
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "number of unique paths from top-left to bottom-right, moving only right/down" | `dp[i][j] = dp[i-1][j] + dp[i][j-1]` |
| "minimum path sum to reach bottom-right" | `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])` |
| "maximum square of 1's in a binary matrix" | `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1` if `matrix[i][j] == 1` |
| "triangle minimum path sum" | Similar shape, but neighbor structure follows the triangle's row/column offsets |
| "dungeon game / minimum initial health" | 2-D DP computed **backward** from the bottom-right, since the "cost" propagates from the end toward the start |

## Common Pitfalls
- Initializing the first row/column incorrectly — these often have a different (simpler) recurrence than interior cells since they can only be reached from one direction.
- Building the table in the wrong traversal order — always confirm which cells a given `dp[i][j]` depends on, and iterate so those are filled first (usually top-to-bottom, left-to-right, but not always — e.g., Dungeon Game goes bottom-to-top).
- Forgetting that grid-based DP can often be space-optimized to O(cols) (one row at a time) — worth mentioning proactively as a follow-up optimization.

## Interview Talking Points
- Explicitly state the recurrence direction and why: "each cell only depends on the cell above and to the left, so I'll fill the table left-to-right, top-to-bottom."
- Mention the space optimization (rolling row) even if you implement the full 2D table first — shows awareness of the O(rows×cols) → O(cols) reduction.

---

# 2. 0/1 Knapsack

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Problem shape | Given items with weights and values, and a capacity limit, maximize value **without exceeding capacity**, each item usable **at most once** |
| State definition | `dp[i][w]` = max value achievable using the first `i` items with capacity `w` |
| Recurrence | `dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i]] + value[i])` if `weight[i] <= w`, else `dp[i-1][w]` |
| Space optimization | 1D array `dp[w]`, iterate `w` **backward** (high to low) to avoid reusing an item within the same iteration |

## Core Intuition
For each item, you make a binary choice: **include it** (gain its value, but reduce remaining capacity) or **exclude it** (keep capacity, no value gain). Because each item can only be used once, the recurrence must reference the "previous item" row (`dp[i-1][...]`) when including an item, not the current row — otherwise you'd allow reusing the same item multiple times (that's Unbounded Knapsack, §3).

```
Items: (weight, value) = (1,1), (3,4), (4,5), capacity = 4

dp[i][w] table (rows = items considered, cols = capacity 0..4):
           w=0  1   2   3   4
no items:   0   0   0   0   0
+item(1,1): 0   1   1   1   1
+item(3,4): 0   1   1   4   5
+item(4,5): 0   1   1   4   5

Answer: dp[3][4] = 5
```

## Why Iterate Backward in the Space-Optimized Version
```python
def knapsack01(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):   # backward!
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```
**Key idea:** iterating `w` from **high to low** ensures that when you compute `dp[w - weights[i]]`, you're reading a value that **hasn't been updated yet in this item's pass** — i.e., it still reflects "without the current item" (equivalent to `dp[i-1][...]`). Iterating forward (low to high) would let the current item's contribution leak into `dp[w - weights[i]]` before it's used, effectively allowing the item to be reused — which is exactly the Unbounded Knapsack recurrence instead.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "each item can be used at most once, maximize value within capacity" | 0/1 Knapsack, backward iteration for space optimization |
| "partition array into two subsets with equal sum" | 0/1 Knapsack in disguise — "can we pick a subset summing to `total/2`?" (a boolean/feasibility variant) |
| "target sum" (assign +/- to reach a target) | 0/1 Knapsack variant — transform into "subset sum" via algebra (`P - N = target`, `P + N = total` ⟹ solve for subset summing to `(total + target) / 2`) |
| "last stone weight II" (minimize difference between two groupings) | 0/1 Knapsack — find achievable sums closest to `total / 2` |

## Worked Pattern: Partition Equal Subset Sum
```python
def canPartition(nums):
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True                     # sum of 0 is always achievable (pick nothing)

    for num in nums:
        for w in range(target, num - 1, -1):    # backward — each number used at most once
            dp[w] = dp[w] or dp[w - num]
    return dp[target]
```
**Key idea:** this is 0/1 Knapsack where "value" and "weight" are the same thing (the number itself), and the question becomes a **feasibility** check (`True`/`False`) instead of maximizing a separate value — same backward-iteration mechanic applies.

## Common Pitfalls
- Iterating capacity **forward** in the space-optimized version — silently turns 0/1 Knapsack into Unbounded Knapsack (allows item reuse), producing wrong (usually too-high) answers.
- Forgetting the base case `dp[0] = True` (or `dp[i][0] = 0`) — capacity 0 should always be trivially achievable with 0 items/value.
- Not recognizing "partition into two equal subsets" or "target sum" as 0/1 Knapsack in disguise — these look like their own problems but reduce directly to the subset-sum recurrence.

## Interview Talking Points
- If using the space-optimized 1D array, explicitly state *why* you're iterating backward — this single detail is one of the most common "do you actually understand it or did you memorize it" checks in knapsack problems.
- Be ready to reduce "partition equal subset sum" / "target sum" to the knapsack recurrence algebraically, out loud, rather than treating them as unrelated problems.

---

# 3. Unbounded Knapsack

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Problem shape | Same as 0/1 Knapsack, but each item can be used **unlimited times** |
| State definition | `dp[w]` = best value/count achievable with capacity `w` |
| Recurrence | `dp[w] = max(dp[w], dp[w - weight[i]] + value[i])` — note: references `dp[w - weight[i]]` which **may already include this same item** |
| Space optimization | 1D array `dp[w]`, iterate `w` **forward** (low to high) — the opposite of 0/1 Knapsack |

## Core Intuition
Since items can be reused, when computing `dp[w]`, it's perfectly valid for `dp[w - weight[i]]` to **already reflect having used item `i`** — that's exactly what "unlimited reuse" means. This is why the space-optimized loop goes **forward**: each update is allowed to build on an already-updated value from the same item's pass, naturally allowing reuse.

```
Coin Change: coins = [1, 2, 5], amount = 11
dp[w] = minimum coins to make amount w

dp[0] = 0
dp[1] = dp[0] + 1 (using coin 1) = 1
dp[2] = min(dp[1]+1, dp[0]+1) = 1   (one coin of value 2)
...
dp[11] = 3   (5 + 5 + 1)
```

## Worked Pattern: Coin Change (Minimum Coins)
```python
def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for w in range(coin, amount + 1):        # forward! allows reuse of the same coin
            dp[w] = min(dp[w], dp[w - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

## Worked Pattern: Coin Change II (Count Number of Ways)
```python
def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1                                     # one way to make amount 0: use no coins
    for coin in coins:
        for w in range(coin, amount + 1):         # forward — unbounded reuse
            dp[w] += dp[w - coin]
    return dp[amount]
```
**Key difference between Coin Change and Coin Change II:** the first minimizes coin *count* (`min` recurrence); the second counts the number of *distinct combinations* (`+=` accumulation) — same loop structure, different aggregation operation, both unbounded.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "minimum number of coins/items to reach a target, unlimited supply" | Unbounded Knapsack, `min` recurrence, forward iteration |
| "number of ways/combinations to reach a target, unlimited supply" | Unbounded Knapsack, `+=` (sum) recurrence, forward iteration |
| "maximize value with unlimited item reuse within a capacity" | Unbounded Knapsack, `max` recurrence, forward iteration |
| "rod cutting" (maximize value by cutting a rod into pieces, pieces reusable) | Unbounded Knapsack — piece lengths = weights, piece prices = values |

## Common Pitfalls
- Iterating forward when the problem is actually 0/1 (each item used once) — the single forward-vs-backward loop direction is the entire difference between these two knapsack variants, and mixing them up silently produces wrong answers without any error.
- Confusing "count combinations" (`dp[w] += dp[w-coin]`, coins iterated in the **outer** loop) with "count permutations" (order matters — amount iterated in the **outer** loop instead) — these produce different counts for the same input and are easy to mix up.
- Not initializing `dp[0]` correctly for the specific aggregation (`0` for min-cost, `1` for count-of-ways, `True` for feasibility).

## Interview Talking Points
- Explicitly contrast with 0/1 Knapsack: "since items can repeat here, I iterate the capacity loop forward instead of backward, which is what allows an item's own updated value to be reused within the same pass."
- If a "counting" variant is asked, clarify with the interviewer (or state your assumption) about whether **order matters** (permutations) or not (combinations) — this changes which loop goes on the outside.

---

# 4. Longest Common Subsequence (LCS)

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| State definition | `dp[i][j]` = length of the LCS between `text1[:i]` and `text2[:j]` (first `i` chars of text1, first `j` chars of text2) |
| Recurrence | If `text1[i-1] == text2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`. Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` |
| Complexity | O(m × n) time, O(m × n) space (reducible to O(min(m,n)) with rolling rows) |
| Key distinction | **Subsequence** ≠ substring — characters don't need to be contiguous, just in the same relative order |

## Core Intuition
Compare the two strings character by character from the end (or beginning): if the current characters **match**, they must both be part of the LCS — extend the LCS found so far without them by 1 (`dp[i-1][j-1] + 1`). If they **don't match**, the LCS must come from dropping one character from either string — take whichever gives the longer result (`max(dp[i-1][j], dp[i][j-1])`).

```
text1 = "abcde", text2 = "ace"

      ""  a   c   e
  ""   0  0   0   0
  a    0  1   1   1
  b    0  1   1   1
  c    0  1   2   2
  d    0  1   2   2
  e    0  1   2   3   ← LCS length = 3 ("ace")
```

## Worked Pattern: Longest Common Subsequence
```python
def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "longest common subsequence between two strings" | Direct LCS recurrence |
| "longest palindromic subsequence" (ties back to 1-D DP Palindrome notes) | LCS of the string and its **reverse** |
| "minimum insertions/deletions to convert string A into string B" | `len(A) + len(B) - 2 * LCS(A, B)` |
| "edit distance" (insert/delete/replace to transform one string into another) | Very similar DP shape to LCS, but recurrence also accounts for a "replace" operation: `dp[i][j] = dp[i-1][j-1]` if match, else `1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` |
| "shortest common supersequence" | Built on top of LCS — the supersequence includes the LCS once plus the non-matching characters from both strings |
| "longest common substring" (must be contiguous — different from subsequence!) | Different recurrence: `dp[i][j] = dp[i-1][j-1] + 1` only on a match, **reset to 0** on mismatch (no `max` fallback) |

## Worked Pattern: Longest Palindromic Subsequence via LCS
```python
def longestPalindromeSubseq(s):
    return longestCommonSubsequence(s, s[::-1])   # LCS of s and its reverse = longest palindromic subsequence
```
**Why this works:** any subsequence that reads the same forward and backward must appear, in the same relative order, in **both** `s` and its reverse — so the longest such subsequence is exactly the LCS between `s` and `reversed(s)`.

## Common Pitfalls
- Confusing **subsequence** (order preserved, gaps allowed) with **substring** (must be contiguous) — these need genuinely different recurrences (LCS allows the `max(dp[i-1][j], dp[i][j-1])` fallback on mismatch; longest common **substring** resets to 0 on mismatch instead).
- Off-by-one indexing — `dp[i][j]` conventionally represents the first `i`/`j` characters, so string indexing inside the loop uses `text1[i-1]`/`text2[j-1]`, not `text1[i]`/`text2[j]`. Mixing this up is a very common bug.
- Forgetting that LCS is the foundation for several other problems (edit distance, shortest common supersequence, longest palindromic subsequence) — not recognizing the connection means re-deriving from scratch instead of adapting a known recurrence.

## Interview Talking Points
- If asked "longest palindromic subsequence" right after LCS, immediately state the reduction (`LCS(s, reverse(s))`) — this is one of the cleanest "aha" connections in the whole DP topic and signals strong pattern transfer.
- For Edit Distance, explicitly contrast the recurrence with plain LCS: "this adds a replace operation, so the recurrence takes a min over three neighbors plus 1, instead of LCS's max over two neighbors."

---

## 📋 Quick Cross-Section Revision Table

| Question to Ask Yourself | If Yes → |
|---|---|
| Am I navigating a literal 2D grid (paths, min cost)? | 2-D DP Fundamentals |
| Can each item be used at most once, with a capacity constraint? | 0/1 Knapsack — iterate capacity **backward** if space-optimized |
| Can items be reused unlimited times? | Unbounded Knapsack — iterate capacity **forward** if space-optimized |
| Am I comparing two separate sequences for shared order (not necessarily contiguous)? | LCS |
| Does the problem need a **contiguous** common run instead? | Longest Common Substring (reset-to-0 variant, not LCS) |
| Can I frame this as "does some subset sum to X"? | 0/1 Knapsack (feasibility variant — Partition Equal Subset Sum, Target Sum) |

## Suggested Problem Set for This Section
- **2-D DP Fundamentals:** Unique Paths, Unique Paths II, Minimum Path Sum, Maximal Square, Triangle
- **0/1 Knapsack:** Partition Equal Subset Sum, Target Sum, Last Stone Weight II, Ones and Zeroes
- **Unbounded Knapsack:** Coin Change, Coin Change II, Combination Sum IV (permutation-counting variant — outer loop is the amount, not the coins)
- **LCS:** Longest Common Subsequence, Longest Palindromic Subsequence, Edit Distance, Shortest Common Supersequence, Delete Operation for Two Strings

---
*Format matches your Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, Tries, Backtracking, Graphs I, and 1-D DP notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*
