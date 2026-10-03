# 1-D Dynamic Programming — DSA Interview Notes
*1-Dimensional DP Fundamentals · Palindrome DP*

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the diagrams by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each section.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right technique in <10 seconds.

All code examples in Python.

---

## 🔑 Cheat Sheet — Both Sections at a Glance
| Section | Core Idea | Time | Space |
|---|---|---|---|
| 1-D DP Fundamentals | `dp[i]` = optimal answer using only the first `i` elements/steps; build up from small `i` to large `i` | O(n) typical | O(n), often reducible to O(1) |
| Palindrome DP | `dp[i][j]` = is `s[i..j]` a palindrome; or expand outward from centers | O(n²) typical | O(n²) table, or O(1) with expand-around-center |

**Core shared idea:** DP replaces exponential brute-force recursion (recomputing the same subproblems over and over) with **remembering** each subproblem's answer once, then reusing it — trading memory for a massive time savings. The entire skill of DP is (1) correctly defining what `dp[i]` (or `dp[i][j]`) *means*, and (2) finding the recurrence that builds it from smaller subproblems.

---

# 1. 1-Dimensional DP Fundamentals

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| State definition | `dp[i]` = the answer to the problem considering only the first `i` elements/steps |
| Two implementation styles | **Top-down (memoization):** recursion + cache. **Bottom-up (tabulation):** iterative, fill `dp[]` from base case upward |
| Base case(s) | The smallest subproblem(s) you can answer directly without recursion (e.g., `dp[0]`, `dp[1]`) |
| Recurrence | How `dp[i]` is computed from `dp[i-1]`, `dp[i-2]`, etc. |
| Space optimization | If `dp[i]` only depends on the last 1–2 values, replace the array with a few rolling variables → O(1) space |

## Core Intuition
Many problems can be solved with plain recursion, but the recursion tree **recomputes the same subproblem many times** (e.g., naive Fibonacci recomputes `fib(n-2)` inside both `fib(n-1)` and directly — exponential blowup). DP fixes this by **caching** each subproblem's answer the first time it's computed (top-down), or by **building the answer iteratively** from the smallest subproblem up (bottom-up), so each subproblem is solved exactly once.

```
Naive recursion for fib(5):           With memoization, each fib(k)
                fib(5)                 is computed ONCE and reused:
              /        \
          fib(4)      fib(3)           fib(2) computed once, reused
          /    \        /   \          by both fib(4) and fib(3)
      fib(3)  fib(2) fib(2) fib(1)     → O(n) instead of O(2^n)
       /  \
   fib(2) fib(1)
   (fib(2) and fib(3) each computed multiple times — wasted work)
```

## Top-Down (Memoization) vs. Bottom-Up (Tabulation)
```python
# Top-down: natural recursive thinking, cache with a dict or @lru_cache
def climbStairs_topdown(n, memo={}):
    if n <= 2:
        return n
    if n in memo:
        return memo[n]
    memo[n] = climbStairs_topdown(n - 1, memo) + climbStairs_topdown(n - 2, memo)
    return memo[n]

# Bottom-up: iterative, build dp[] from the base case upward — no recursion overhead
def climbStairs_bottomup(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# Space-optimized bottom-up: only the last 2 values are ever needed
def climbStairs_optimized(n):
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1
```
**When to use which:** top-down is often easier to *derive* (write the brute-force recursion first, add a cache); bottom-up avoids recursion-depth limits and is usually what interviewers want to see as the "optimized" final answer, especially once space optimization is layered on top.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "number of ways to reach step n / climb stairs" | `dp[i] = dp[i-1] + dp[i-2]` (Fibonacci-shaped) |
| "maximum sum without choosing adjacent elements" (House Robber) | `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` |
| "maximum profit with a cooldown / transaction fee constraint" | `dp[i]` tracks multiple states (holding stock vs. not) at each step |
| "longest increasing subsequence" | `dp[i]` = length of the longest increasing subsequence ending at index `i`; `dp[i] = max(dp[j] + 1)` for all `j < i` with `nums[j] < nums[i]` |
| "minimum cost to reach the end, one or two steps at a time" | `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` |
| "count ways to decode / tile / partition a sequence" | `dp[i]` = number of valid ways using the first `i` elements, recurrence depends on valid "last piece" choices |

## Worked Pattern: House Robber
```python
def rob(nums):
    if not nums:
        return 0
    rob1, rob2 = 0, 0   # rob1 = dp[i-2], rob2 = dp[i-1]
    for num in nums:
        new_rob = max(rob2, rob1 + num)   # either skip current, or rob it + best up to i-2
        rob1 = rob2
        rob2 = new_rob
    return rob2
```
**Key idea:** at each house, you either **skip it** (carry forward the best result without it, `dp[i-1]`) or **rob it** (`dp[i-2] + nums[i]`, since you can't rob the adjacent house). Only the last two `dp` values are ever needed — hence the O(1) space rolling-variable version.

## Worked Pattern: Longest Increasing Subsequence (O(n²) DP)
```python
def lengthOfLIS(nums):
    dp = [1] * len(nums)   # every element is at least a subsequence of length 1 (itself)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```
**Complexity:** O(n²) — for every `i`, check all previous `j`. *(An O(n log n) binary-search-based approach exists too — worth mentioning as a follow-up optimization if asked.)*

## Common Pitfalls
- Not clearly defining what `dp[i]` **means** before writing the recurrence — this is the #1 source of DP bugs; if you can't state the meaning in one sentence, the recurrence will be wrong.
- Off-by-one errors in base cases (`dp[0]`, `dp[1]`) — always hand-trace the smallest 2–3 cases before trusting the general recurrence.
- Jumping straight to space-optimized rolling variables before confirming the array-based version is correct — verify correctness first, optimize space second.
- Confusing "subarray" (contiguous) with "subsequence" (not necessarily contiguous) — this distinction changes the recurrence entirely (e.g., Maximum Subarray vs. Longest Increasing Subsequence).

## Interview Talking Points
- Always state the `dp[i]` definition out loud before coding — "dp[i] represents the maximum profit achievable using the first i days" — this is exactly what interviewers want to hear to confirm you're not guessing.
- If you started with recursion, explicitly narrate the transition: "this naive recursion recomputes overlapping subproblems, so I'll add memoization" — demonstrates you understand *why* DP applies, not just that it does.

---

# 2. Palindrome DP

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| DP table definition | `dp[i][j]` = True if `s[i..j]` (inclusive) is a palindrome |
| Recurrence | `dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]` (with base cases for length 1 and 2) |
| Alternative: Expand Around Center | For each possible center (single char or between two chars), expand outward while characters match — O(1) space, same O(n²) time |
| When to use table vs. expand-around-center | Table is needed when you must **query palindrome status of many substrings repeatedly**; expand-around-center is simpler and more space-efficient for single-pass problems like "longest palindromic substring" |

## Core Intuition
A substring `s[i..j]` is a palindrome if its **outer characters match** (`s[i] == s[j]`) **and** the inner substring `s[i+1..j-1]` is also a palindrome. This is a direct recursive/DP relationship — building outward from the smallest palindromes (single characters, always palindromes) to longer ones.

```
s = "babad"

dp[i][i] = True for all i           (single chars are palindromes)
dp[i][i+1] = True if s[i]==s[i+1]   (two-char palindromes)

"bab": dp[0][2] = (s[0]==s[2]) and dp[1][1] = ('b'=='b') and True = True
```

### Expand Around Center (the more commonly used approach in interviews)
Instead of filling a full table, treat every index (and every gap between two indices, for even-length palindromes) as a potential **center**, and expand outward while the characters on both sides match.

```
s = "babad", center at index 2 ('b' in "bab")

expand: left=2, right=2 → 'b' == 'b' → expand
        left=1, right=3 → 'a' == 'a' → expand
        left=0, right=4 → 'b' == 'd' → stop
palindrome found: s[1:4] = "bab"
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "longest palindromic substring" | Expand around center (every index + every gap as a center), O(n²) time, O(1) space |
| "count all palindromic substrings" | Expand around center, count every successful expansion |
| "is this string/substring a palindrome" (asked repeatedly) | Precompute the full `dp[i][j]` table once, O(1) lookup per query afterward |
| "longest palindromic subsequence" (not necessarily contiguous) | This is **not** expand-around-center — it reduces to **LCS of the string and its reverse** (see 2-D DP notes, LCS section) |
| "minimum insertions/deletions to make a string a palindrome" | Related to Longest Palindromic Subsequence — answer = `n - LPS length` |
| "palindrome partitioning" (split string into palindromic pieces) | Backtracking (see Backtracking notes) combined with a precomputed `dp[i][j]` palindrome table for O(1) validity checks during the search |

## Worked Pattern: Longest Palindromic Substring (Expand Around Center)
```python
def longestPalindrome(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]     # the last valid palindrome before mismatch/out-of-bounds

    result = ""
    for i in range(len(s)):
        odd = expand(i, i)          # odd-length palindrome centered AT i
        even = expand(i, i + 1)     # even-length palindrome centered BETWEEN i and i+1
        result = max(result, odd, even, key=len)
    return result
```
**Key idea — two center types:** odd-length palindromes (like "bab") have a single character as the center; even-length palindromes (like "abba") have the center **between** two characters. Both must be checked at every index to cover all possible palindromes.
**Complexity:** O(n²) time (n centers × O(n) expansion each), O(1) extra space.

## Worked Pattern: Count Palindromic Substrings (DP Table version)
```python
def countSubstrings(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    count = 0

    for i in range(n - 1, -1, -1):          # build from shorter substrings to longer (i decreasing, j increasing relative to i)
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                count += 1
    return count
```
**Key idea — fill order matters:** `dp[i][j]` depends on `dp[i+1][j-1]` (a shorter, "more inward" substring), so the table must be filled with `i` decreasing (or equivalently, by increasing substring length) to guarantee the needed values are already computed.

## Common Pitfalls
- Filling the `dp[i][j]` table in the wrong order — since `dp[i][j]` depends on `dp[i+1][j-1]`, iterating `i` from 0 upward (the "natural" direction) accesses **not-yet-computed** cells. Iterate `i` from `n-1` down to `0` (or by increasing substring length) instead.
- Forgetting the two center types (single-character and between-characters) in expand-around-center — missing the "even-length" case silently drops valid palindromes like "abba".
- Confusing **longest palindromic substring** (contiguous, expand-around-center or DP table) with **longest palindromic subsequence** (not contiguous, solved via LCS with the reversed string — a completely different technique).
- Using the full O(n²) DP table when expand-around-center (O(1) space) would suffice — table is only necessary when the same palindrome-membership queries are needed repeatedly (e.g., inside a backtracking search).

## Interview Talking Points
- Be ready to justify why expand-around-center achieves O(n²) despite looking like it might be more: there are O(n) possible centers, each expansion is O(n) worst case, giving O(n²) total — same as the DP table approach, but with O(1) space instead of O(n²).
- If asked about "longest palindromic **subsequence**" right after solving "longest palindromic **substring**," immediately flag that it's a different problem needing LCS-with-reverse, not a small tweak to expand-around-center.

---

## 📋 Quick Cross-Section Revision Table

| Question to Ask Yourself | If Yes → |
|---|---|
| Does `dp[i]` depend only on a fixed small number of previous states (`dp[i-1]`, `dp[i-2]`)? | 1-D DP, likely space-optimizable to O(1) |
| Am I checking palindrome status of substrings, need the longest one, single-pass? | Expand Around Center |
| Do I need repeated palindrome-substring queries, or is this feeding into backtracking? | Precompute the `dp[i][j]` palindrome table once |
| Is the palindrome required to be **contiguous**? | Substring techniques (expand-around-center/table) | 
| Is the palindrome allowed to **skip characters** (not contiguous)? | Longest Palindromic Subsequence → LCS with reversed string (see 2-D DP notes) |
| Can I write brute-force recursion first and see repeated subproblems? | Add memoization (top-down), then consider converting to bottom-up + space optimization |

## Suggested Problem Set for This Section
- **1-D DP Fundamentals:** Climbing Stairs, House Robber, House Robber II, Longest Increasing Subsequence, Maximum Subarray, Decode Ways, Coin Change (also appears in Unbounded Knapsack, 2-D DP notes), Word Break
- **Palindrome DP:** Longest Palindromic Substring, Palindromic Substrings, Longest Palindromic Subsequence, Palindrome Partitioning, Minimum Insertion Steps to Make a String Palindrome

---
*Format matches your Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, Tries, Backtracking, and Graphs I notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*
