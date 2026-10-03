# Sliding Window — DSA Interview Notes
*NeetCode 150 | Fixed Size Window · Variable Size Window*

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the diagrams by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each method.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right variant in <10 seconds.

---

## 🔑 Cheat Sheet — Both Methods at a Glance
| Method | Window Size | Movement | Typical Use | Time | Space |
|---|---|---|---|---|---|
| Fixed Size | Constant `k`, given upfront | `right` advances, `left = right - k + 1` (both slide together) | "window of size k" problems | O(n) | O(1)–O(k) |
| Variable Size | Grows/shrinks based on a condition | `right` always advances; `left` advances only when condition is violated | "longest/shortest/count of subarrays satisfying X" | O(n) | O(1)–O(k) |

**Core shared idea:** avoid recomputing a window's stats from scratch every time it shifts (which is O(n·k) or O(n²)). Instead, **incrementally update** the window state as `left`/`right` move — add what enters, remove what leaves. This is Two Pointers (previous topic) specialized to *contiguous subarray/substring* problems with running state.

---

# 1. Fixed Size Window

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Setup | `left = 0`, build first window `[0, k-1]`, compute initial stat (sum/count/etc.) |
| Movement | For each step: **add** `nums[right]`, **remove** `nums[left]`, then move both `left` and `right` forward by 1 |
| Precondition | Window size `k` is fixed/known in advance |
| Complexity | O(n) time — each element added and removed from the window exactly once |
| Brute force it replaces | Recomputing every window's sum/stat from scratch → O(n·k) |

## Core Intuition
When you slide a fixed-size window one step to the right, only **two elements change**: the one that just left (leftmost of old window) and the one that just entered (rightmost of new window). Everything in between is unchanged — so update the running stat with O(1) work instead of recomputing the whole window.

```
nums = [2, 1, 5, 1, 3, 2], k = 3

window [2,1,5] → sum = 8
slide: remove 2, add 1 → window [1,5,1] → sum = 8 - 2 + 1 = 7
slide: remove 1, add 3 → window [5,1,3] → sum = 7 - 1 + 3 = 9
slide: remove 5, add 2 → window [1,3,2] → sum = 9 - 5 + 2 = 6

max sum = 9  (found in O(n), not O(n·k))
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "maximum/minimum sum of a subarray of size k" | Fixed window, running sum: add incoming, subtract outgoing |
| "average of all subarrays of size k" | Fixed window running sum, divide by k each step |
| "find if a permutation of s1 exists in s2" (window = len(s1)) | Fixed window + character frequency map comparison |
| "max number of vowels in substring of length k" | Fixed window, running count of vowels |
| "sliding window maximum" (max in every window of size k) | Fixed window + **monotonic deque** to track max in O(1) amortized (see Deep Dive) |

## Deep Dive: Sliding Window Maximum (Monotonic Deque)
A plain fixed window handles running **sums/counts** in O(1) per step easily, but tracking the **max/min** of the window isn't a simple add/subtract (removing an element might have been the max — you'd need to rescan). The fix: a **monotonic deque** storing indices, kept in decreasing order of value.

```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()  # stores indices, values decreasing left to right
    res = []
    for right in range(len(nums)):
        # remove indices whose values are smaller than current — they can never be the max again
        while dq and nums[dq[-1]] < nums[right]:
            dq.pop()
        dq.append(right)
        # remove index if it's fallen out of the window on the left
        if dq[0] <= right - k:
            dq.popleft()
        if right >= k - 1:
            res.append(nums[dq[0]])  # front of deque = max of current window
    return res
```
**Why it works:** any element smaller than a newer element to its right, and to its left in the window, can *never* be the max while that newer element is still in the window — so it's safe to discard permanently. Each element is pushed/popped at most once → O(n) total despite the nested-looking while loop.

## Common Pitfalls
- Recomputing the window sum from scratch every slide (defeats the purpose — makes it O(n·k) again).
- Off-by-one when initializing the first window — make sure it's exactly `k` elements (`[0, k-1]`) before you start sliding.
- For max/min-in-window problems, reaching for a plain running variable instead of a monotonic deque — a single removal of the current max/min breaks that approach.
- Forgetting to only start recording results once `right >= k - 1` (i.e., the first full window has formed).

## Interview Talking Points
- If asked for **window max/min**, immediately signal you know a naive running-variable approach breaks on removal, and pivot to monotonic deque — this is a strong signal of pattern depth.
- State clearly: fixed window turns O(n·k) brute force into O(n) by reusing overlapping work between consecutive windows.

---

# 2. Variable Size Window

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Setup | `left = 0`, `right` scans forward |
| Movement | `right` **always** advances each iteration; `left` advances (possibly multiple times) **only while a condition is violated** |
| Precondition | No fixed size — window size is discovered dynamically based on a constraint |
| Complexity | O(n) — `left` and `right` each traverse the array at most once, total pointer movement ≤ 2n |
| Brute force it replaces | Checking every possible subarray/substring → O(n²) or O(n³) |

## Core Intuition
Grow the window (`right += 1`) to include more elements. Whenever the window state violates a constraint (too many duplicate chars, sum too large, etc.), shrink from the left (`left += 1`) until it's valid again. At each point where the window is valid, update your answer (max length / min length / count).

```
s = "abcabcbb"   →  longest substring without repeating characters

right=0 'a': window {a}          valid, len=1, best=1
right=1 'b': window {a,b}        valid, len=2, best=2
right=2 'c': window {a,b,c}      valid, len=3, best=3
right=3 'a': 'a' already in window → shrink: remove s[left]='a', left=1
             window {b,c,a}      valid, len=3, best=3
right=4 'b': 'b' already in window → shrink: remove s[left]='b', left=2
             window {c,a,b}      valid, len=3, best=3
... continues, best stays 3
```

### Why It's O(n), Not O(n²)
It looks like a nested loop (`for right`, `while left`), which seems like O(n²) at first glance. But `left` **only ever moves forward**, never resets backward — across the entire run, `left` advances at most `n` times total, and `right` advances at most `n` times total. Total work = O(n) + O(n) = **O(n)**, not O(n²). This "amortized" argument is exactly analogous to the amortized array-doubling argument from Dynamic Arrays — be ready to state it explicitly.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "longest substring without repeating characters" | Variable window + set/dict of chars in window; shrink on duplicate |
| "longest substring with at most K distinct characters" | Variable window + frequency map; shrink while `distinct count > K` |
| "minimum window substring containing all characters of T" | Variable window + frequency map of T; grow until valid, then shrink while still valid to minimize |
| "smallest subarray with sum ≥ target" | Variable window + running sum; shrink while `sum >= target` |
| "longest subarray with at most K zeroes flipped" | Variable window + zero-count; shrink while `zero_count > K` |
| "max consecutive ones III" | Same as above — variable window bounded by allowed flips |
| "fruit into baskets" (at most 2 distinct types) | Variable window + frequency map, shrink while `distinct types > 2` |

## Worked Pattern: Minimum Window Substring
```python
from collections import Counter, defaultdict

def minWindow(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    window = defaultdict(int)
    have, required = 0, len(need)
    res, res_len = [-1, -1], float("inf")
    left = 0

    for right in range(len(s)):
        c = s[right]
        window[c] += 1
        if c in need and window[c] == need[c]:
            have += 1

        # shrink while window is valid — trying to minimize
        while have == required:
            if (right - left + 1) < res_len:
                res = [left, right]
                res_len = right - left + 1
            window[s[left]] -= 1
            if s[left] in need and window[s[left]] < need[s[left]]:
                have -= 1
            left += 1

    l, r = res
    return s[l:r + 1] if res_len != float("inf") else ""
```
**Complexity:** O(n + m) where n = len(s), m = len(t) — each character in `s` is visited by `right` once and by `left` at most once.

## Common Pitfalls
- Using `if` instead of `while` when shrinking — a single shrink step may not be enough to restore validity (or, for minimization problems, you want to shrink *as much as possible* while still valid).
- Forgetting to update the "best answer" at the correct point — for **longest** problems, update after the window becomes valid; for **minimum window** problems, update *inside* the shrink loop (while still valid), not after.
- Not resetting/decrementing window state correctly when `left` moves — every element added must have a matching removal when it leaves the window.
- Conflating "shrink until valid" (minimize) with "shrink while valid" (some max-length problems shrink only enough to become valid again, not further) — read the problem's exact constraint carefully.

## Interview Talking Points
- Be ready to explain why this is O(n) and not O(n²) — the "left only moves forward" amortized argument.
- Variable window problems are a favorite because they combine hashmap pattern recognition (previous topic) with two-pointer movement — expect interviewers to ask you to identify *both* pieces explicitly.

---

## 📋 Quick Cross-Method Revision Table

| Question to Ask Yourself | If Yes → | If No → |
|---|---|---|
| Is the window size given/fixed (`k`) upfront? | Fixed Size Window | Variable Size Window |
| Do I need the max/min *value* inside a fixed window (not just sum/count)? | Fixed Size + Monotonic Deque | Plain running sum/count is enough |
| Am I looking for longest/shortest/count of subarrays satisfying a condition? | Variable Size Window | — |
| Does the window need to track composition (char/element frequency), not just sum? | Pair window with a hashmap (ties back to Hash Usage topic) | Running sum/count alone may suffice |

## Suggested NeetCode 150 Problem Set for This Section
- **Fixed size:** Maximum Average Subarray I, Permutation in String, Sliding Window Maximum
- **Variable size:** Best Time to Buy and Sell Stock, Longest Substring Without Repeating Characters, Longest Repeating Character Replacement, Permutation in String (alt. approach), Minimum Window Substring, Minimum Size Subarray Sum

---
*Format matches your Arrays & Hashing and Two Pointers notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*
