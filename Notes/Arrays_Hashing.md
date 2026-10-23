# Arrays & Hashing — DSA Interview Notes
*NeetCode 150 | Dynamic Arrays · Hash Usage · Prefix Sums*

# 1. Dynamic Arrays

## 🔑 Cheat Sheet
| Operation | Static Array | Dynamic Array (amortized) |
|---|---|---|
| Access by index | O(1) | O(1) |
| Append at end | N/A (fixed size) | **O(1) amortized**, O(n) worst case |
| Insert at front/middle | O(n) | O(n) |
| Delete from end | N/A | O(1) |
| Delete from front/middle | O(n) | O(n) |
| Search (unsorted) | O(n) | O(n) |

## Core Intuition
A **static array** is a fixed-size contiguous memory block — great for O(1) access via `base_address + index * size`, terrible when you don't know the size upfront.

A **dynamic array** (Python `list`, Java `ArrayList`, C++ `vector`) solves this by:
1. Allocating extra capacity beyond current length.
2. When full, allocating a **new array of ~2x size**, copying all elements over.
3. Because doubling happens exponentially less often as size grows, the *amortized* cost of `append` averages out to O(1) even though occasional resizes cost O(n).

```
Capacity: 4        Capacity: 8 (after resize)
[1][2][3][4]   →    [1][2][3][4][5][_][_][_]
   full, append 5         copied + appended
```

### Why amortized O(1), not just O(1)?
If you append n elements starting from capacity 1 and double each time:
```
Total copy cost = 1 + 2 + 4 + 8 + ... + n ≈ 2n
```
Total cost for n appends = O(n) → **average cost per append = O(1)**.
This is the classic "doubling" argument — know it, interviewers sometimes ask you to explain it (esp. at product companies with strong CS fundamentals bar, e.g. Google, Amazon, Uber).

## Deep Dive: What Python/Java Actually Do
- Python's `list` over-allocates (growth pattern roughly ×1.125 for large lists, not a clean 2x, but the amortized argument still holds).
- `list.append(x)` → amortized O(1)
- `list.insert(0, x)` → O(n) — shifts every element right
- `list.pop()` → O(1)
- `list.pop(0)` → O(n) — shifts every element left
- **Interview trap:** using `list.insert(0, x)` or `list.pop(0)` repeatedly in a loop silently turns an O(n) solution into O(n²). If you need frequent front operations, use `collections.deque` instead (O(1) both ends).

## Patterns That Live on Top of Dynamic Arrays
| Pattern | Idea | Example Problems |
|---|---|---|
| **Two Pointers** | Move indices from both ends / same direction to avoid nested loops | Valid Palindrome, Container With Most Water, 3Sum |
| **Sliding Window** | Maintain a window `[left, right]`, expand/shrink based on condition | Best Time to Buy/Sell Stock, Longest Substring Without Repeating Chars |
| **In-place manipulation** | Overwrite array using a slow/fast pointer to avoid O(n) extra space | Remove Duplicates from Sorted Array, Move Zeroes |
| **Prefix/Suffix products or sums** | Precompute left-to-right and right-to-left passes | Product of Array Except Self |
| **Sorting first** | Sort to enable two-pointer or greedy logic | 3Sum, Merge Intervals |

## Common Pitfalls
- Off-by-one errors on `right` boundary — decide up front if your window/range is inclusive or exclusive and stay consistent.
- Mutating a list while iterating over it (skips/misreads elements). Iterate over a copy, or iterate backwards when deleting.
- Forgetting that slicing (`arr[1:]`) in Python creates a new O(n) copy — costly inside a loop.
- Assuming `append` is *always* strictly O(1) — fine for amortized analysis, but matters if asked about worst-case single-call complexity.

## Interview Talking Points
- "Why not just use a static array?" → don't know size in advance / need to grow.
- "What's the worst case for a single append?" → O(n), when resize is triggered.

---

# 2. Hash Usage

## 🔑 Cheat Sheet
| Structure | Stores | Lookup | Use When |
|---|---|---|---|
| `set` (HashSet) | unique keys | O(1) avg | "have I seen this before?", dedup, membership |
| `dict` (HashMap) | key → value | O(1) avg | need to associate data with a key (counts, indices, groups) |
| `Counter` (dict subtype) | key → frequency | O(1) avg | frequency counting, anagrams, majority element |
| `defaultdict(list)` | key → list of values | O(1) avg | grouping items by a computed key |

## Core Intuition
A hash map trades a small amount of memory for **O(1) average-case lookup/insert/delete**, replacing O(n) linear scans. Whenever a problem's brute force is "for each element, search the rest of the array" (O(n²)), ask: *can I remember what I've seen in a hash map instead?*

## Signal → Technique (Pattern Recognition)
| Signal in Problem Statement | Technique | Example |
|---|---|---|
| "find two numbers that sum to target" | Store `value → index` in dict, check `target - num` as you go | Two Sum |
| "group anagrams / group by some property" | Compute a canonical key (sorted string, char-count tuple) → `defaultdict(list)` | Group Anagrams |
| "check for duplicates" | `set` membership check | Contains Duplicate |
| "count frequency of elements/characters" | `Counter` or manual dict | Valid Anagram, Top K Frequent Elements |
| "longest/shortest substring/subarray with X property" | Sliding window + hashmap tracking window state | Longest Substring Without Repeating Characters |
| "subarray sum equals K" | Prefix sum + hashmap of prefix-sum frequencies (see Prefix Sums §4) | Subarray Sum Equals K |
| "first unique / first non-repeating" | Dict for counts + ordered iteration | First Unique Character |
| "is one string a rearrangement/anagram of another" | Char frequency comparison via dict or fixed-size array (26 letters) | Valid Anagram |

## Why Hashing Beats Sorting (Sometimes)
- Sorting to detect duplicates/anagrams: O(n log n).
- Hashing: O(n) average, O(n) extra space.
- **Trade-off to state out loud in interviews:** hashing wins on time, costs extra space; sorting wins on space (in-place), costs time. If asked for O(1) space, sorting (or bit tricks) may be the expected answer instead of hashing.

## Common Pitfalls
- Using a list where a set/dict was called for → turns O(1) lookup into O(n), silently degrading a solution to O(n²).
- Forgetting mutable types (lists) can't be dict keys — use tuples for composite keys (e.g., `(row, col)` in grid problems).
- Not handling hash collisions of *logical* keys — e.g., sorted string as anagram key is safe, but a naive concatenation key might collide unintentionally.
- In frequency-count problems with **fixed alphabet** (e.g., lowercase English letters), a size-26 array is often faster/simpler than a hashmap — mention this as an optimization.

## Interview Talking Points
- Always state time/space complexity **before and after** introducing the hashmap — this is exactly the trade-off interviewers want to hear articulated.
- If interviewer asks "can you do it in O(1) space?", that's your cue hashing isn't the intended final answer (e.g., Product of Array Except Self, or bit manipulation in Single Number).

---

# 3. Prefix Sums

## 🔑 Cheat Sheet
| Task | Formula |
|---|---|
| Build prefix array | `prefix[0] = nums[0]`; `prefix[i] = prefix[i-1] + nums[i]` |
| Range sum `[l, r]` (inclusive) | `prefix[r] - prefix[l-1]` (or `prefix[r+1] - prefix[l]` with 1-indexed/padded prefix) |
| Subarray sum = k (count) | Hashmap of `{prefix_sum: frequency}`, check `prefix_sum - k` seen before |
| 2D range sum | `prefix[r2][c2] - prefix[r1-1][c2] - prefix[r2][c1-1] + prefix[r1-1][c1-1]` |

## Core Intuition
If you'll be asked **multiple range-sum queries** on a **static (unchanging) array**, don't recompute each sum in O(n) — precompute cumulative sums once in O(n), then answer each query in **O(1)**.

```
nums   =  [2, 4, 1, 5, 3]
prefix =  [2, 6, 7, 12, 15]     prefix[i] = sum(nums[0..i])

sum(nums[1..3]) = prefix[3] - prefix[0] = 12 - 2 = 10
                = 4 + 1 + 5 ✓
```

### Padded version (avoids index-out-of-bounds at l=0)
```python
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + nums[i]

# sum of nums[l..r] inclusive:
range_sum = prefix[r + 1] - prefix[l]
```
This padded form is usually cleaner — no special-casing `l == 0`.

## The Big Pattern: Prefix Sum + HashMap (subarray sum problems)
This is the single highest-leverage prefix sum pattern in interviews.

**Problem shape:** "Find number of subarrays that sum to exactly k."

**Key insight:** `sum(i..j) = prefix[j] - prefix[i-1]`. So `sum(i..j) == k` ⟺ `prefix[i-1] == prefix[j] - k`.
As you scan left to right building the running prefix sum, ask: *"have I seen `current_prefix_sum - k` before?"* — store prefix sum frequencies in a hashmap as you go.

```python
def subarraySum(nums, k):
    count = 0
    curr_sum = 0
    seen = {0: 1}   # empty prefix sum occurs once (handles subarray starting at index 0)
    for num in nums:
        curr_sum += num
        count += seen.get(curr_sum - k, 0)
        seen[curr_sum] = seen.get(curr_sum, 0) + 1
    return count
```
This turns an O(n²) brute force (all subarrays) into **O(n)**.

## Signal → Technique
| Signal | Technique |
|---|---|
| "multiple range sum queries on a fixed array" | Plain prefix sum array, O(1) per query |
| "number of subarrays with sum = k" | Prefix sum + hashmap of frequencies |
| "equilibrium index / pivot index" (left sum == right sum) | Prefix sum from both directions |
| "2D submatrix sum queries" | 2D prefix sum (inclusion-exclusion) |
| "product of array except self" | Prefix product (left pass) × suffix product (right pass) — same idea, multiplication instead of addition |
| "running/cumulative XOR of subarray" | Prefix XOR (XOR is its own inverse: `a ^ a = 0`) — same hashmap trick as subarray sum |

## Common Pitfalls
- Off-by-one between 0-indexed and 1-indexed (padded) prefix arrays — pick one convention and stick to it within a solution.
- Forgetting `seen = {0: 1}` initialization in the subarray-sum-k pattern — this accounts for subarrays that start at index 0.
- Using prefix sums when the array is **mutable** (frequent updates) — plain prefix sums require O(n) rebuild per update; that's a signal to reach for a **Fenwick Tree / Binary Indexed Tree** or **Segment Tree** instead (good to *mention* as the next-level structure, even if NeetCode 150 doesn't require implementing one).
- Integer overflow in other languages (not a concern in Python, but mention awareness for Java/C++ interviews).

## Interview Talking Points
- "What if the array can be updated between queries?" → prefix sum breaks down (O(n) rebuild per update); pivot to Fenwick Tree/Segment Tree (O(log n) update + query) as the theoretically correct answer, even if you're not asked to code it.
- Be ready to derive the prefix-sum-plus-hashmap trick live — interviewers often want to see the `prefix[j] - prefix[i-1] = k` algebra reasoned out loud, not just recalled.

---

## 📋 Quick Cross-Topic Revision Table

| Topic | Core Trade-off | O(1) Operation | When It Breaks Down |
|---|---|---|---|
| Dynamic Arrays | Amortized growth vs. fixed size | Append (amortized), index access | Frequent front insert/delete → use deque |
| Hash Usage | Space for time | Lookup/insert/delete (avg) | Need O(1) *extra* space, or ordered data |
| Prefix Sums | Precompute once, query cheap | Range sum query | Array is mutated frequently → need Fenwick/Segment Tree |

## Suggested NeetCode 150 Problem Set for This Section
- **Arrays/Hashing core:** Contains Duplicate, Valid Anagram, Two Sum, Group Anagrams, Top K Frequent Elements, Product of Array Except Self, Valid Sudoku, Encode and Decode Strings, Longest Consecutive Sequence
- **Hash implementation practice:** Design HashMap (LC 706), Design HashSet (LC 705)
- **Prefix sums:** Subarray Sum Equals K, Range Sum Query - Immutable, Product of Array Except Self (prefix/suffix variant)
