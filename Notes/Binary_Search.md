# Binary Search — DSA Interview Notes
*NeetCode 150 | Search Array (Classic) · Search Range (Binary Search on Answer / Boundaries)*

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the diagrams by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each method.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right variant in <10 seconds.

---

## 🔑 Cheat Sheet — Both Methods at a Glance
| Method | Goal | What Narrows the Search | Time | Space |
|---|---|---|---|---|
| Search Array (Classic) | Find exact target's index (or determine absence) in a sorted array | Direct comparison: `arr[mid]` vs `target` | O(log n) | O(1) |
| Search Range (Boundary / On Answer) | Find leftmost/rightmost valid index, or the smallest/largest value satisfying a **condition** | A **predicate/condition function** (`is_valid(mid)`) rather than direct equality | O(log n) × cost of predicate | O(1) |

**Core shared idea:** whenever you can eliminate **half the remaining search space** with one comparison, you get O(log n) instead of O(n). Classic binary search does this on sorted data directly; "search range" generalizes the same halving idea to any **monotonic condition** — even if there's no literal sorted array.

---

# 1. Search Array (Classic Binary Search)

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Setup | `left = 0`, `right = len(arr) - 1` |
| Loop condition | `while left <= right` |
| Midpoint | `mid = left + (right - left) // 2` (avoids overflow in other languages; good habit in Python too) |
| Update | `arr[mid] == target` → return `mid`; `arr[mid] < target` → `left = mid + 1`; `arr[mid] > target` → `right = mid - 1` |
| Precondition | Array must be **sorted** |
| Complexity | O(log n) time, O(1) space |

## Core Intuition
Because the array is sorted, comparing the middle element to the target tells you which **entire half** can be discarded — you never need to look at it again. Each comparison halves the search space, giving O(log n) instead of O(n) linear scan.

```
arr = [1, 3, 5, 7, 9, 11, 13], target = 9

left=0, right=6, mid=3 → arr[3]=7 < 9 → discard left half → left=4
left=4, right=6, mid=5 → arr[5]=11 > 9 → discard right half → right=4
left=4, right=4, mid=4 → arr[4]=9 == 9 → found at index 4
```
3 comparisons instead of scanning up to 7 elements — the gap widens fast as n grows (log₂(1,000,000) ≈ 20).

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "sorted array, find target's index" | Classic binary search |
| "sorted array, search in O(log n)" | Classic binary search — this phrase is a direct giveaway |
| "search in rotated sorted array" | Modified binary search — at each step, determine which half (left or right of `mid`) is properly sorted, then check if target lies within that sorted half |
| "find peak element" | Binary search using local slope comparison (`arr[mid]` vs `arr[mid+1]`) instead of exact match |
| "sqrt(x)" / "find kth smallest via binary search on value space" | Binary search on the **answer's value range**, not array indices (bridges into Search Range, below) |
| "search a 2D matrix (sorted rows and columns)" | Treat as a flattened 1D sorted array, binary search with index math `row = mid // cols`, `col = mid % cols` |

## Worked Pattern: Search in Rotated Sorted Array
```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:          # left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:                                 # right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```
**Key idea:** even though the whole array isn't sorted, **at least one half of any subarray around `mid` always is** — identify which half is sorted first, then decide whether the target could be in that sorted half using normal range comparison.

## Common Pitfalls
- Infinite loop from wrong midpoint update — always move `left`/`right` to `mid ± 1`, never leave `mid` in the range after a comparison (except in boundary-search variants, see §2).
- `left + (right - left) // 2` vs `(left + right) // 2` — functionally same in Python (no integer overflow), but the former is the safer habit to carry into other languages (Java/C++) where it prevents overflow.
- Assuming a "sorted" array with duplicates behaves identically — duplicates can break the "which half is sorted" logic in rotated array search; some variants require O(n) worst case fallback.
- Off-by-one on `while left <= right` vs `while left < right` — classic search uses `<=` because it needs to check the case `left == right` (single element remaining); boundary search often uses `<` (see below).

## Interview Talking Points
- State the invariant clearly before coding: "at every step, if the target exists, it's within `[left, right]`."
- For rotated array search, explicitly say out loud "one half is always sorted" — this is the key insight interviewers are listening for.

---

# 2. Search Range (Binary Search on Boundaries / On Answer)

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Goal | Find the **leftmost** or **rightmost** index satisfying a condition, or the **first/last True** in a monotonic True/False sequence |
| Loop condition | `while left < right` (common form when converging to a single boundary index) |
| Update | Depends on which boundary: for leftmost, when `condition(mid)` is true, don't discard `mid` yet — set `right = mid` (not `mid - 1`) |
| Precondition | The condition must be **monotonic** — i.e., once it flips from False to True (or vice versa) across the search space, it never flips back |
| Complexity | O(log n) × cost of evaluating the condition per step |

## Core Intuition
Not every binary search problem is "find this exact value." Many are: **"find the boundary where a condition changes from False to True."** As long as the condition is monotonic (all False, then all True — or vice versa — never interleaved), you can binary search on that boundary exactly like classic search, just with a different update rule to correctly converge on the edge index.

```
Think of it as a boolean array over the search space:
condition(x): [F, F, F, F, T, T, T, T, T]
                              ^
                    first index where condition becomes True
                    ← binary search finds this boundary in O(log n)
```

### Finding First/Last Occurrence (bisect-style)
```
nums = [5, 7, 7, 7, 8, 10], target = 7

Find leftmost 7:                     Find rightmost 7:
left=0,right=5,mid=2→7==7,           left=0,right=5,mid=2→7==7,
  record, search left: right=mid-1     record, search right: left=mid+1
...converges to index 1              ...converges to index 3

Range of target 7 = [1, 3]
```

### Leftmost Boundary — Canonical Template
```python
def find_leftmost(nums, target):
    left, right = 0, len(nums)  # note: right = len(nums), not len(nums)-1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid           # don't discard mid — it might BE the answer
    return left  # first index where nums[index] >= target
```
This is the exact logic behind Python's `bisect_left`. Swap the comparison to `<=` for `bisect_right` (rightmost insertion point).

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "find first and last position of target in sorted array" | Two boundary searches — leftmost and rightmost occurrence |
| "find minimum in rotated sorted array" | Boundary search on the "is this element ≥ nums[0]" condition (or compare to `nums[right]`) |
| "capacity to ship packages within D days" / "koko eating bananas" / "minimum days to make m bouquets" | **Binary search on the answer** — search over the *value range* of possible answers (e.g., capacity 1..sum(weights)), using a feasibility check as the monotonic condition |
| "split array largest sum" | Binary search on answer — search possible "largest sum" values, check feasibility with greedy partition count |
| "find smallest/largest value satisfying a feasibility check" | Binary search on answer — condition = "is this value feasible?", monotonic by problem design |
| "single element in a sorted array (all others appear twice)" | Boundary search exploiting index parity as the monotonic condition |

## Worked Pattern: Binary Search on Answer (Koko Eating Bananas)
```python
import math

def minEatingSpeed(piles, h):
    def hours_needed(speed):
        return sum(math.ceil(pile / speed) for pile in piles)

    left, right = 1, max(piles)   # search space = possible eating speeds
    while left < right:
        mid = left + (right - left) // 2
        if hours_needed(mid) <= h:   # feasible at this speed
            right = mid               # try to find a smaller feasible speed
        else:
            left = mid + 1            # too slow, need higher speed
    return left
```
**Key idea:** we're not binary-searching an array at all — we're binary-searching the **space of possible answers** (eating speeds 1 to max(piles)), using `hours_needed(speed) <= h` as the monotonic feasibility check. This is the single highest-leverage generalization of binary search for interviews — recognize it whenever a problem asks for "minimum X such that condition holds" or "maximum X such that condition holds."

## Common Pitfalls
- Forgetting the condition must be **monotonic** before applying binary search on answer — verify this explicitly (increasing speed → hours needed only decreases or stays same, never increases).
- Using `right = mid - 1` when you should use `right = mid` (or vice versa) — in boundary search, if `mid` could *be* the answer, don't exclude it from the next range.
- Initializing `right = len(nums) - 1` when the leftmost-boundary template expects `right = len(nums)` — mixing templates from classic search and boundary search causes subtle off-by-one bugs. Keep the two templates mentally separate.
- Infinite loops from using `while left < right` with an update that doesn't shrink the range (e.g., `right = mid` when `mid == left` and range doesn't shrink) — always verify the range strictly shrinks each iteration.

## Interview Talking Points
- "Binary search on answer" is a strong signal-to-pattern connection to name explicitly the moment you see "minimum/maximum value such that some condition holds" — even if there's no array to search at all.
- Be ready to state the monotonicity requirement as the *precondition* for binary search to apply — interviewers often probe "why does binary search work here?"

---

## 📋 Quick Cross-Method Revision Table

| Question to Ask Yourself | If Yes → | If No → |
|---|---|---|
| Am I looking for one exact value's index in a sorted array? | Search Array (Classic) | Consider Search Range |
| Is the array rotated but still "sorted in parts"? | Search Array, modified (identify sorted half each step) | — |
| Do I need the first/last occurrence, or a boundary where a condition flips? | Search Range (boundary template) | — |
| Is there no array at all, just a range of possible answers and a feasibility check? | Search Range — Binary Search on Answer | — |
| Can I verify the condition is monotonic across the search space? | Binary search applies | Binary search does NOT apply — reconsider approach |

## Suggested NeetCode 150 Problem Set for This Section
- **Search Array (Classic):** Binary Search, Search a 2D Matrix, Search in Rotated Sorted Array, Find Minimum in Rotated Sorted Array, Find Peak Element
- **Search Range (Boundary / On Answer):** Find First and Last Position of Element in Sorted Array, Koko Eating Bananas, Time Based Key-Value Store, Median of Two Sorted Arrays (advanced), Capacity To Ship Packages Within D Days

---
*Format matches your Arrays & Hashing, Two Pointers, Sliding Window, and Stack notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*
