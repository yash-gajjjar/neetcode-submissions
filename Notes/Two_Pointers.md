# Two Pointers — DSA Interview Notes
*NeetCode 150 | Opposite-Directional (Converging) · Same-Directional (Fast & Slow)*

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the diagrams by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each method.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right variant in <10 seconds.

---

## 🔑 Cheat Sheet — Both Methods at a Glance
| Method | Pointer Movement | Typical Precondition | Time | Space |
|---|---|---|---|---|
| Opposite-Directional (Converging) | Start at both ends, move inward | Usually needs **sorted** array (or symmetry, e.g. palindrome) | O(n) | O(1) |
| Same-Directional (Fast & Slow) | Both start at/near the beginning, move forward at different rates or roles | Works on **unsorted** data; common on linked lists & in-place array ops | O(n) | O(1) |

**Core shared idea:** replace an O(n²) nested-loop brute force with a single O(n) pass by using two indices instead of one, each carrying meaningful state about what's already been seen/processed.

---

# 1. Opposite-Directional (Converging) Pointers

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Setup | `left = 0`, `right = len(arr) - 1` |
| Movement | Move `left` right, or `right` left, based on a comparison — never both blindly |
| Termination | `while left < right` |
| Precondition | Almost always requires a **sorted** array, or an inherent left/right symmetry (palindrome check) |
| Complexity | O(n) time, O(1) space (vs O(n²) or O(n log n) brute force alternatives) |

## Core Intuition
When an array is sorted, the two ends give you *maximum leverage*: increasing `left` only grows the value at that side; decreasing `right` only shrinks the value at that side. This lets you eliminate one candidate pair per step instead of checking all pairs.

```
nums = [1, 3, 4, 6, 8, 12], target = 10

left=0 (1)                          right=5 (12)
sum = 1 + 12 = 13 > 10 → too big → move right left

left=0 (1)                   right=4 (8)
sum = 1 + 8 = 9 < 10 → too small → move left right

left=1 (3)                right=4 (8)
sum = 3 + 8 = 11 > 10 → move right left

left=1 (3)         right=3 (6)
sum = 3 + 6 = 9 < 10 → move left right

left=2 (4)   right=3 (6)
sum = 4 + 6 = 10 ✓ found
```

### Why It's Correct (the part interviewers probe on)
At each step, if `sum > target`, you know **every pair involving the current `right` and any index ≤ `left`** is already covered by comparison logic, and increasing `left` is the only way to reduce the sum — so it's safe to discard `right` (or vice versa). This "safe elimination" argument is the crux of why two pointers work; be ready to justify it out loud rather than just stating the algorithm.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "sorted array, find a pair that sums to target" | Converging pointers, move based on sum vs target |
| "check if string/array is a palindrome" | `left`/`right` compare-and-converge, skip non-alphanumeric if needed |
| "container with most water / max area between two lines" | Converging pointers, always move the shorter side (greedy elimination) |
| "3Sum / 4Sum" | Fix one (or two) elements with a loop, converging two-pointer scan on the rest of a **sorted** array |
| "reverse array/string in place" | `left`/`right` swap-and-converge |
| "merge two sorted arrays from the end" | Converging pointers from the back to avoid overwriting |

## Worked Pattern: 3Sum (fix + converge)
```python
def threeSum(nums):
    nums.sort()
    res = []
    for i in range(len(nums)):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # skip duplicate anchors
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total > 0:
                right -= 1
            elif total < 0:
                left += 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                left += 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1  # skip duplicate left
    return res
```
**Complexity:** O(n²) — O(n log n) sort + O(n) outer loop × O(n) inner converge = O(n²) dominates.

## Common Pitfalls
- Forgetting the array must be **sorted** first for sum-based converging problems — sorting costs O(n log n), which is fine unless the problem explicitly asks for O(n).
- Duplicate handling in 3Sum/4Sum — skip duplicate values at both the anchor and the two-pointer level to avoid duplicate triplets in the result.
- Moving both pointers in the same step without justification — usually wrong; the choice of which pointer to move should follow directly from the comparison.
- Container With Most Water: forgetting that you must **always move the pointer at the shorter line** (moving the taller one can never improve the area, since width shrinks either way and height is capped by the shorter line).

## Interview Talking Points
- Be ready to explain *why* two pointers is O(n) instead of O(n²) — the "safe elimination" argument above.
- If the array isn't sorted and you can't sort it (order matters for output), converging pointers usually isn't applicable directly — flag this trade-off.

---

# 2. Same-Directional (Fast & Slow) Pointers

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Setup | `slow = 0`, `fast = 0` (or `fast` a fixed number of steps ahead) |
| Movement | `fast` advances every iteration (sometimes 2x speed); `slow` advances only under a condition |
| Precondition | Works on **unsorted** arrays, linked lists — no sortedness needed |
| Complexity | O(n) time, O(1) space |

## Core Intuition
`slow` marks the boundary of "processed/valid" data; `fast` explores ahead and decides when `slow` should advance. This is the workhorse for **in-place array modification** and **linked-list structure problems** (cycle detection, finding the middle).

Two flavors show up constantly:

### (a) In-place array compaction (write pointer)
```
nums = [0, 1, 0, 3, 12]     "move all zeroes to the end"

slow (write ptr) = 0
fast scans left to right; whenever nums[fast] != 0, swap into nums[slow], slow += 1

fast=0: nums[0]=0 → skip
fast=1: nums[1]=1 → swap(slow=0, fast=1) → [1,0,0,3,12], slow=1
fast=2: nums[2]=0 → skip
fast=3: nums[3]=3 → swap(slow=1, fast=3) → [1,3,0,0,12], slow=2
fast=4: nums[4]=12 → swap(slow=2, fast=4) → [1,3,12,0,0], slow=3
```
`slow` always points to the next position where a "valid" element should be written; `fast` does the scanning/discovery.

### (b) Cycle detection / middle-of-list (Floyd's Tortoise and Hare)
```
slow moves 1 step, fast moves 2 steps per iteration.
If there's a cycle, fast eventually laps slow → they meet.
If no cycle, fast hits null first.
```
```python
def hasCycle(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```
**Why it works:** in a cycle, the gap between `fast` and `slow` shrinks by 1 each iteration (fast gains 1 step relative to slow every step) — so they're guaranteed to meet within one full lap of the cycle, not run forever.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "remove duplicates from sorted array in place" | slow = write pointer, fast = scan pointer, advance slow only on new distinct value |
| "move zeroes / partition array by condition" | slow = next-write position, fast = scanner |
| "detect cycle in linked list" | Floyd's fast (2x) & slow (1x) — meet ⟹ cycle |
| "find middle of linked list" | fast (2x) & slow (1x) — when fast hits end, slow is at middle |
| "find start of cycle" | Floyd's Part 2: after meeting, reset one pointer to head, move both 1 step at a time — they meet at cycle start |
| "remove Nth node from end of list" | fast pointer starts N steps ahead, then both move together until fast hits end |
| "linked list palindrome check" | fast/slow to find middle, reverse second half, then converge-compare (combines both methods!) |

## Worked Pattern: Remove Duplicates from Sorted Array (in-place, slow/fast)
```python
def removeDuplicates(nums):
    if not nums:
        return 0
    slow = 1
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow - 1]:
            nums[slow] = nums[fast]
            slow += 1
    return slow  # new length; first `slow` elements are the deduped array
```
**Complexity:** O(n) time, O(1) space — no extra array needed.

## Common Pitfalls
- Confusing "fast advances every step" with "fast and slow always move together" — in compaction problems, `slow` only advances *conditionally*, `fast` always advances.
- Off-by-one in the Nth-from-end pattern — decide whether the gap is `n` or `n+1` steps and verify with a small example before coding.
- Null pointer checks in linked-list fast/slow — always guard `fast and fast.next` before `fast.next.next`.
- Forgetting Floyd's algorithm has **two phases** (detect meeting point, then find cycle start) — a common half-answer in interviews.

## Interview Talking Points
- Fast/slow (Floyd's) is a favorite "prove it mathematically" follow-up — be ready to explain the relative-speed/gap-shrinking argument, not just recite the code.
- If asked "can you do this without extra space?" for array problems (dedup, move zeroes, partition), fast/slow in-place is almost always the expected answer.

---

## 📋 Quick Cross-Method Revision Table

| Question to Ask Yourself | If Yes → | If No → |
|---|---|---|
| Is the array sorted (or can I sort it without breaking the problem)? | Consider Opposite-Directional (Converging) | Consider Same-Directional (Fast & Slow) |
| Am I looking for a pair/triplet that satisfies a sum/comparison condition? | Converging pointers | — |
| Am I modifying the array in place / compacting it based on a condition? | Fast & Slow (write pointer + scanner) | — |
| Is this a linked list problem about cycles, middle, or Nth-from-end? | Fast & Slow (Floyd's-style) | — |
| Do I need O(1) space instead of a hashmap/extra array? | Two pointers (either variant) is likely the intended optimization | — |

## Suggested NeetCode 150 Problem Set for This Section
- **Converging pointers:** Valid Palindrome, Two Sum II - Input Array Is Sorted, 3Sum, Container With Most Water, Trapping Rain Water
- **Fast & slow pointers:** Remove Duplicates from Sorted Array, Move Zeroes, Linked List Cycle, Middle of the Linked List, Remove Nth Node From End of List, Palindrome Linked List

---
*Format matches your Arrays & Hashing notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*
