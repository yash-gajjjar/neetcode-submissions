# Heap / Priority Queue — DSA Interview Notes
*Heap Properties · Push and Pop · Heapify · Two Heaps*

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the diagrams by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each section.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right technique in <10 seconds.

All code examples in Python (using the built-in `heapq` module, which implements a **min-heap**).

---

## 🔑 Cheat Sheet — All Four Sections at a Glance
| Section | Core Idea | Time | Space |
|---|---|---|---|
| Heap Properties | A complete binary tree where every parent is ≤ (min-heap) or ≥ (max-heap) its children | — | O(n) storage |
| Push and Pop | Insert/remove while restoring heap order via "bubble up" / "bubble down" | O(log n) per operation | O(1) extra |
| Heapify | Convert an unordered array into a valid heap **in place** | O(n) — not O(n log n)! | O(1) extra |
| Two Heaps | Pair a max-heap (for the "lower half") with a min-heap (for the "upper half") to track a median or split data by threshold | O(log n) per insert | O(n) |

**Core shared idea:** a heap gives you fast access to the **min or max element** (O(1) peek) while still supporting O(log n) insert/remove — it deliberately gives up full sorting in exchange for being much cheaper to maintain than a sorted array, because it only enforces order **between parents and children**, not across the whole structure.

---

# 1. Heap Properties

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Shape property | A heap is a **complete binary tree** — every level is fully filled except possibly the last, which fills left to right |
| Order property (min-heap) | Every parent's value ≤ both its children's values (the root is always the minimum) |
| Order property (max-heap) | Every parent's value ≥ both its children's values (the root is always the maximum) |
| Array representation | Stored as a flat array — no explicit pointers needed, since the complete-tree shape makes index math predictable |
| Index math | For a node at index `i`: parent = `(i-1)//2`, left child = `2i+1`, right child = `2i+2` |

## Core Intuition
A heap is **not fully sorted** — it only guarantees that each parent is smaller (min-heap) or larger (max-heap) than its own children. This weaker guarantee is exactly what makes heaps cheap to maintain: you never need to reorder the *entire* structure, only the path from a changed node up or down to restore local parent-child ordering.

```
Min-Heap (as a tree):              Same heap (as an array):
        1
      /   \                        [1, 3, 2, 5, 4, 8]
     3     2                        index: 0  1  2  3  4  5
    / \   /
   5   4 8

Verify with index math: node at index 1 (value 3) →
  parent = (1-1)//2 = 0 (value 1) ✓ 1 ≤ 3
  left child = 2*1+1 = 3 (value 5) ✓ 3 ≤ 5
  right child = 2*1+2 = 4 (value 4) ✓ 3 ≤ 4
```

### Why "Complete Tree + Array" Instead of Linked Nodes
Because a heap is always a **complete** tree (no gaps except possibly at the end of the last level), its shape is fully predictable — you never need explicit `left`/`right` pointers. This lets a heap be stored compactly in a plain array with O(1) parent/child lookups via index arithmetic, unlike a general binary tree which needs actual node objects with pointers.

## Common Pitfalls
- Assuming a heap is **fully sorted** — it's not; only the root is guaranteed to be the min/max. The second-smallest element in a min-heap is *not necessarily* at index 1 or 2 — it's guaranteed to be one of the root's children, but you can't know which without comparing.
- Confusing min-heap and max-heap order direction — Python's `heapq` only implements a **min-heap**; to simulate a max-heap, negate values on push/pop (see §2).
- Forgetting the heap must remain a **complete** tree at all times — this shape property is what every push/pop operation is careful to preserve.

## Interview Talking Points
- If asked "why use a heap instead of just sorting," the answer is the trade-off: sorting gives full order (O(n log n) to build, but then O(1) access to *any* rank), while a heap gives O(n) or O(log n) maintenance with fast access to *only* the min/max — the right tool depends on whether you need the extremes repeatedly (heap) or full ordering (sort).

---

# 2. Push and Pop

## 🔑 Cheat Sheet
| Operation | Complexity | Mechanism |
|---|---|---|
| Push (insert) | O(log n) | Add at the end (preserving complete-tree shape), then **bubble up** (swap with parent while out of order) |
| Pop (remove min/max) | O(log n) | Remove the root, move the **last element** to the root, then **bubble down** (swap with the smaller/larger child while out of order) |
| Peek (view min/max) | O(1) | Just look at index 0 — no restructuring needed |

## Core Intuition
Both operations follow the same idea: make a **minimal, localized change** (add at the end, or move the last element to the root), then walk that one out-of-place element up or down the tree until heap order is restored. Because the tree has height O(log n), this walk touches at most O(log n) nodes.

### Push: Bubble Up
```
Insert 2 into: [1, 3, 4]

Step 1: append at the end → [1, 3, 4, 2]
Step 2: compare 2 with its parent (index (3-1)//2=1, value 3): 2 < 3 → swap
         → [1, 2, 4, 3]
Step 3: compare 2 (now index 1) with its parent (index 0, value 1): 2 > 1 → stop

Final heap: [1, 2, 4, 3]
```

### Pop: Bubble Down
```
Remove min from: [1, 2, 4, 3]

Step 1: save root (1) as the answer
Step 2: move the LAST element (3) to the root → [3, 2, 4]
Step 3: compare 3 with its children (2 and 4): smaller child is 2 → swap
         → [2, 3, 4]
Step 4: 3 has no children left to compare → stop

Answer: 1.  Remaining heap: [2, 3, 4]
```

## Using Python's `heapq` (min-heap only)
```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
print(heap[0])            # peek: 1 (the minimum)
print(heapq.heappop(heap))  # 1 — removes and returns the minimum
```

### Simulating a Max-Heap (negate values)
```python
max_heap = []
for num in [5, 1, 3]:
    heapq.heappush(max_heap, -num)     # negate on push
largest = -heapq.heappop(max_heap)     # negate again on pop to recover the true value
```
**Key idea:** since `heapq` only provides min-heap behavior, negating values flips the comparison — the "smallest negated value" corresponds to the "largest original value."

### Pushing Tuples (Priority + Payload)
```python
heap = []
heapq.heappush(heap, (2, "task_b"))    # (priority, data) — compares by priority first
heapq.heappush(heap, (1, "task_a"))
print(heapq.heappop(heap))             # (1, "task_a") — lowest priority number first
```
**Key idea:** `heapq` compares tuples element by element, so `(priority, data)` naturally orders by priority; if two priorities are equal, it falls back to comparing `data` — which can crash if `data` isn't comparable (e.g., raw objects). A common fix is to add a **tie-breaking counter**: `(priority, counter, data)`.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "kth largest/smallest element" | Min-heap of size k (for kth largest) or max-heap of size k (for kth smallest) — see Heapify §3 for the efficient build |
| "top K frequent elements" | Heap of `(frequency, element)` pairs, size-bounded to k |
| "merge K sorted lists" | Min-heap holding the current head of each list; repeatedly pop the smallest, push its successor |
| "task scheduling by priority" | Heap of `(priority, task)` tuples, possibly with a tie-breaking counter |
| "running median" | Two Heaps (see §4) |

## Common Pitfalls
- Forgetting `heapq` is min-heap only — trying to use it directly for "largest" problems without negation gives wrong results.
- Pushing raw objects without a sortable key, causing a crash on tie-breaking comparisons — always push `(priority, ..., data)` tuples with enough leading comparable fields to avoid ties reaching an incomparable payload.
- Assuming `heap[0]` after arbitrary list mutation is still valid — you cannot safely modify the underlying list directly and expect heap order to hold; always go through `heappush`/`heappop` (or re-`heapify` after direct mutation).

## Interview Talking Points
- If simulating a max-heap, mention the negation trick explicitly — a very standard, expected technique in Python-based interviews.
- For "top K" style problems, be ready to state the complexity precisely: maintaining a heap capped at size k costs O(n log k), better than sorting everything (O(n log n)) when k is much smaller than n.

---

# 3. Heapify

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| What it does | Converts an arbitrary unsorted array into a valid heap **in place** |
| Complexity | **O(n)** — not O(n log n) as a naive analysis might suggest (see Deep Dive below) |
| Python built-in | `heapq.heapify(list)` — transforms the list in place into a valid min-heap |
| Common use | Building a heap from an entire existing array up front, faster than pushing elements one at a time |

## Core Intuition
You could build a heap by pushing every element one at a time (`n` pushes, each O(log n) → O(n log n) total). Heapify does better: it starts from the **last non-leaf node** and bubbles each node **down** into place, working backward toward the root. Because most nodes in a complete tree are near the bottom (where bubbling down is cheap — few levels to travel), the total cost sums to O(n), not O(n log n).

### Why O(n), Not O(n log n) (the part worth understanding, not just memorizing)
```
In a heap of n nodes:
- ~n/2 nodes are leaves (0 levels to bubble down)
- ~n/4 nodes are one level up (at most 1 swap)
- ~n/8 nodes are two levels up (at most 2 swaps)
- ...

Total work ≈ n/2×0 + n/4×1 + n/8×2 + n/16×3 + ...
           = a converging sum that totals O(n), not O(n log n)

(Most nodes are near the bottom, where bubbling down is cheap —
 only a few nodes near the root require the full O(log n) work.)
```

## Implementation (manual, for understanding — Python's `heapq.heapify` does this internally)
```python
def heapify(arr):
    n = len(arr)
    # start from the last non-leaf node, work backward to the root
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, i, n)

def _sift_down(arr, i, n):
    smallest = i
    left, right = 2 * i + 1, 2 * i + 2
    if left < n and arr[left] < arr[smallest]:
        smallest = left
    if right < n and arr[right] < arr[smallest]:
        smallest = right
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        _sift_down(arr, smallest, n)     # continue bubbling down from the new position
```

## Using Python's Built-in
```python
import heapq

arr = [5, 3, 8, 1, 9, 2]
heapq.heapify(arr)          # O(n), transforms arr in place
print(arr[0])                # smallest element, guaranteed at index 0
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "given an unsorted array, repeatedly extract the min/max" | `heapq.heapify(arr)` once (O(n)), then `heappop` repeatedly (O(log n) each) |
| "find the kth largest element" (one-time query, not a stream) | `heapify` the whole array (O(n)), then pop k times (O(k log n)) — or use `heapq.nlargest(k, arr)` |
| "build a heap from a full dataset upfront" | Always prefer `heapify` (O(n)) over pushing one at a time (O(n log n)) when you have all the data in advance |

## Common Pitfalls
- Building a heap by pushing elements one at a time when the entire dataset is already available — this is O(n log n) instead of the O(n) `heapify` achieves; a strong candidate uses `heapify` whenever the full input is known upfront.
- Assuming heapify produces a **fully sorted array** — it doesn't; it only establishes valid heap order (root is min/max, but siblings and cousins have no guaranteed relative order).
- Forgetting `heapify` works **in place** — it doesn't return a new list; the input list itself becomes the heap.

## Interview Talking Points
- If you're about to push n elements into a heap one at a time and you already have all of them in a list, proactively mention `heapify` instead — the O(n) vs. O(n log n) distinction is a specific, checkable signal of algorithmic care.
- Be ready to explain (not just state) why heapify is O(n) — the "most nodes are near the bottom, where sifting down is cheap" argument above.

---

# 4. Two Heaps

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Structure | A **max-heap** holding the smaller half of the data, and a **min-heap** holding the larger half |
| Invariant | Every element in the max-heap ≤ every element in the min-heap; sizes are kept balanced (differ by at most 1) |
| Core use | Efficiently track the **median** of a growing stream of numbers |
| Complexity | O(log n) per insertion, O(1) to retrieve the median |

## Core Intuition
To find a median efficiently as numbers stream in, split the data into two halves: the **lower half** (accessed via its maximum, using a max-heap) and the **upper half** (accessed via its minimum, using a min-heap). The median is then always derivable from the tops of these two heaps in O(1) — either the average of both tops (even total count) or the top of the larger heap (odd total count) — without ever needing to fully sort the stream.

```
Stream: 5, 15, 1, 3

Insert 5:  max_heap=[5]           min_heap=[]
Insert 15: max_heap=[5]           min_heap=[15]     (5 ≤ 15, balanced)
Insert 1:  max_heap=[5,1]→rebal   min_heap=[15]      → max_heap=[1] min_heap=[5,15]
Insert 3:  max_heap=[1,3]         min_heap=[5,15]    (balanced, sizes equal)

Median after 4 elements = avg(top of max_heap, top of min_heap) = avg(3, 5) = 4
```

## Worked Pattern: Find Median from Data Stream
```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []    # max-heap (store negated values) — lower half
        self.large = []    # min-heap — upper half

    def addNum(self, num):
        heapq.heappush(self.small, -num)               # always push to max-heap first

        # ensure every element in small <= every element in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # rebalance sizes: they must differ by at most 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        if len(self.large) > len(self.small):
            return self.large[0]
        return (-self.small[0] + self.large[0]) / 2
```
**Key idea — two separate invariants maintained on every insert:** (1) ordering — every value in `small` must be ≤ every value in `large`, checked by comparing their tops; (2) balance — the two heaps' sizes can differ by at most 1, so the median is always retrievable from just the top(s). Both are restored after every single insertion, keeping `findMedian()` an O(1) operation.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "find the median of a stream of numbers" | Two Heaps (max-heap for lower half, min-heap for upper half) |
| "sliding window median" | Two Heaps + a way to remove arbitrary elements as the window slides (often a "lazy deletion" heap variant) |
| "IPO / maximize capital with a threshold" (pick projects you can afford, then unlock better ones) | Two Heaps — a min-heap of "affordable by capital" and a max-heap of "profit," moving projects between them as capital grows |
| "task scheduling balancing two competing priorities" | Two Heaps, one for each priority dimension |

## Common Pitfalls
- Forgetting to maintain **both** invariants (ordering between heaps, and size balance) on every single insertion — skipping either one breaks the O(1) median retrieval guarantee.
- Mixing up which heap needs negation — only `small` (the max-heap simulation) needs negated values; `large` (min-heap) uses plain `heapq` behavior directly.
- Off-by-one when computing the median for even vs. odd total counts — always check `len(self.small)` vs `len(self.large)` explicitly rather than assuming one is always bigger.

## Interview Talking Points
- Be ready to explain the two invariants explicitly (cross-heap ordering + size balance) as two separate things that must both be restored after every insert — this precision signals you're not just pattern-matching the "two heaps" label but understand what makes it correct.
- If asked to extend to a **sliding window** median, flag that removing arbitrary (non-top) elements from a heap isn't natively supported — this typically requires a "lazy deletion" approach (mark elements as removed, discard them lazily when they surface at the top) rather than a true removal operation.

---

## 📋 Quick Cross-Section Revision Table

| Question to Ask Yourself | If Yes → |
|---|---|
| Do I only need the min or max element repeatedly, not full sorting? | Heap/Priority Queue |
| Do I have the entire dataset upfront before building the heap? | Use `heapify` (O(n)) instead of repeated `heappush` (O(n log n)) |
| Do I need the "largest" using Python's min-heap-only `heapq`? | Negate values on push/pop |
| Do I need to track a running median as data streams in? | Two Heaps |
| Do I need the top K elements, K much smaller than N? | Size-bounded heap, O(n log k) |
| Am I merging multiple already-sorted sources? | Min-heap holding one "current" element per source |

## Suggested Problem Set for This Section
- **Heap Properties / Push & Pop:** Kth Largest Element in a Stream, Last Stone Weight
- **Heapify:** Kth Largest Element in an Array, Top K Frequent Elements
- **Two Heaps:** Find Median from Data Stream, Sliding Window Median, IPO
- **General heap application:** Merge K Sorted Lists, Task Scheduler, K Closest Points to Origin

---
*Format matches your Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, Tries, Backtracking, Graphs I, Graphs II, 1-D DP, and 2-D DP notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*
