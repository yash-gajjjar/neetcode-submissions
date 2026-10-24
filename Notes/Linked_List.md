# Linked List — DSA Interview Notes
*NeetCode 150 | Singly Linked Lists · Doubly Linked Lists · Fast & Slow Pointers*

---

## 🔑 Cheat Sheet — All Four at a Glance
| Structure/Technique | Core Idea | Typical Use | Time | Space |
|---|---|---|---|---|
| Singly Linked List | Node → next only | Sequential access, insert/delete at known position | O(1) insert/delete at head; O(n) access | O(n) |
| Doubly Linked List | Node ↔ prev/next both directions | Need to traverse/delete backward, O(1) removal given a node reference | O(1) insert/delete given node; O(n) access | O(n) |
| Fast & Slow Pointers | Two pointers moving at different speeds through the list | Cycle detection, find middle, find Nth-from-end | O(n) | O(1) |


**Core shared idea:** unlike arrays, linked lists give up O(1) random access in exchange for O(1) insert/delete *once you're at the right node* — most linked-list interview problems are really about **pointer bookkeeping**: carefully rewiring `next` (and `prev`) references without losing track of nodes.

---

# 1. Singly Linked Lists

## 🔑 Cheat Sheet
| Operation | Complexity |
|---|---|
| Access by index | O(n) — must walk from head |
| Insert/delete at head | O(1) |
| Insert/delete at tail (no tail pointer) | O(n) — must walk to find it |
| Insert/delete at tail (with tail pointer) | O(1) insert, O(n) delete (need node *before* tail) |
| Search | O(n) |

## Core Intuition
Each node stores a value and a single pointer to the **next** node. There's no way to go backward — if you need the previous node, you must have kept a reference to it during traversal, or walked from the head again.

```
head → [1|•] → [2|•] → [3|•] → [4|None]
```

### Node Definition (Python)
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "reverse a linked list" | Iterative pointer reversal (prev/curr/next) or recursive |
| "merge two sorted linked lists" | Dummy head node + two pointers advancing through both lists |
| "remove Nth node from end" | Fast pointer N steps ahead, then move both together (ties to Fast & Slow, §3) |
| "add two numbers represented as linked lists" | Simulate digit-by-digit addition with carry, dummy head to build result |
| "reorder list / interleave halves" | Find middle (fast/slow) + reverse second half + merge alternately |
| "delete node given only that node (no head access)" | Copy next node's value into current node, skip next (classic trick — only works if it's not the tail) |

## Worked Pattern: Reverse Linked List (iterative)
```python
def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next   # save before overwriting
        curr.next = prev        # reverse the pointer
        prev = curr             # advance prev
        curr = next_node        # advance curr
    return prev   # new head
```
**Complexity:** O(n) time, O(1) space.

**Why the save step matters:** once you set `curr.next = prev`, you've destroyed the only reference to the rest of the original list — you must capture `next_node` *before* overwriting `curr.next`. This ordering mistake is the single most common bug in linked-list reversal.

## Worked Pattern: Merge Two Sorted Lists (dummy head trick)
```python
def mergeTwoLists(list1, list2):
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 if list1 else list2   # attach remainder
    return dummy.next
```
**Key idea — the dummy head trick:** creating a placeholder `dummy` node before the real head eliminates special-casing "is this the first node I'm attaching?" You always return `dummy.next` at the end. This trick appears constantly across linked-list problems (merge, remove elements, partition, add two numbers).

## Common Pitfalls
- Losing the rest of the list by overwriting `.next` before saving a reference to it.
- Forgetting a **dummy head** when building a new list — leads to messy `if head is None: head = node else: ...` branching.
- Off-by-one when the list is empty or has exactly one node — always trace edge cases (`head = None`, `head.next = None`) by hand.
- Not updating the **tail** pointer (if maintained separately) after modifying the list.

## Interview Talking Points
- Reversal (iterative and recursive) is foundational — practice both until they're automatic; many "harder" linked-list problems (reorder list, palindrome check) are built by composing reversal with other techniques.
- Always mention the dummy-head trick when building a new list — it signals clean, bug-resistant code style.

---

# 2. Doubly Linked Lists

## 🔑 Cheat Sheet
| Operation | Complexity |
|---|---|
| Access by index | O(n) |
| Insert/delete **given a node reference** | O(1) — no need to find the predecessor |
| Traverse backward | O(1) per step (unlike singly, which can't go backward at all) |
| Extra memory per node | One additional pointer (`prev`) vs singly |

## Core Intuition
Each node stores pointers to **both** the next and previous nodes. The key advantage over singly linked lists: **deleting or inserting at a known node is O(1)** without needing to separately track/find the predecessor (which singly linked lists require, since you can't walk backward).

```
None ← [1|•|•] ⇄ [2|•|•] ⇄ [3|•|•] ⇄ [4|•|None]
head↑                                    ↑tail
```

### Node Definition (Python)
```python
class DListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "design a data structure with O(1) insert/delete/get" (e.g., LRU Cache) | Doubly linked list + hashmap (hashmap gives O(1) node lookup, DLL gives O(1) reordering/removal) |
| "browser history / undo-redo with forward and backward navigation" | Doubly linked list, current pointer moves via `prev`/`next` |
| "flatten a multilevel doubly linked list" | DFS/stack-based traversal, rewiring `prev`/`next` and `child` pointers |
| "design a text editor / cursor-based structure" | Doubly linked list, cursor tracks current node |

## Worked Pattern: LRU Cache (Doubly Linked List + HashMap)
```python
class DListNode:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}  # key -> DListNode
        # dummy head/tail sentinels simplify edge cases (no None checks)
        self.left, self.right = DListNode(), DListNode()
        self.left.next, self.right.prev = self.right, self.left

    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _insert(self, node):
        # insert at the right (most recently used) end
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt

    def get(self, key):
        if key not in self.cache:
            return -1
        self._remove(self.cache[key])
        self._insert(self.cache[key])   # mark as most recently used
        return self.cache[key].val

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        self.cache[key] = DListNode(key, value)
        self._insert(self.cache[key])
        if len(self.cache) > self.cap:
            lru = self.left.next            # least recently used = leftmost real node
            self._remove(lru)
            del self.cache[lru.key]
```
**Complexity:** O(1) for both `get` and `put` — the hashmap gives instant node lookup, the doubly linked list gives instant removal/reinsertion without scanning.
**Key idea — sentinel nodes:** using dummy `left`/`right` sentinel nodes (instead of `None` boundaries) removes almost all edge-case branching for "is this the first/last real node?"

## Common Pitfalls
- Forgetting to update **both** `prev` and `next` pointers on insert/delete — a doubly linked list requires twice the pointer bookkeeping of singly linked lists; missing one direction silently corrupts the structure.
- Not using sentinel head/tail nodes — leads to constant `if node is None` special-casing for boundary operations.
- In LRU-style problems, forgetting to move a node to the "most recently used" end on both `get` *and* `put`.

## Interview Talking Points
- LRU Cache (doubly linked list + hashmap) is one of the most common "design a data structure" interview questions at product companies — practice implementing it cold.
- Be ready to state clearly: singly linked list needs the *predecessor* to delete a node in O(1); doubly linked list doesn't, because `prev` is already stored on the node itself.

---

# 3. Fast and Slow Pointers (on Linked Lists)

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Setup | `slow = head`, `fast = head` |
| Movement | `slow` advances 1 step, `fast` advances 2 steps, each iteration |
| Guard condition | `while fast and fast.next:` (prevents null pointer errors) |
| Complexity | O(n) time, O(1) space — no extra data structure needed |

*(This is the linked-list-specific application of the Fast & Slow pattern covered more generally in the Two Pointers notes — repeated here in the linked-list context since the guard conditions and use cases differ slightly from array versions.)*

## Core Intuition
Because `fast` moves twice as fast as `slow`, by the time `fast` reaches the end, `slow` is exactly at the **middle**. And if the list has a cycle, `fast` will eventually **lap** `slow` from behind and they'll meet — this is impossible on a list without a cycle, since `fast` would just hit `None` first.

```
1 → 2 → 3 → 4 → 5 → None

step 0: slow=1, fast=1
step 1: slow=2, fast=3
step 2: slow=3, fast=5
fast.next is None → stop.  slow=3 is the middle. ✓
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "find the middle of a linked list" | fast (2x) / slow (1x); when `fast` hits end, `slow` is at middle |
| "detect if a linked list has a cycle" | Floyd's — if `slow == fast` at any point, cycle exists |
| "find where the cycle begins" | Floyd's Part 2 (see Deep Dive below) |
| "check if a linked list is a palindrome" | Find middle (fast/slow) → reverse second half → compare from both ends → (optionally restore list) |
| "remove Nth node from end" | `fast` starts N steps ahead of `slow`, then both move together until `fast` hits the end — `slow` lands just before the node to remove |
| "reorder list (L0→Ln→L1→Ln-1→...)" | Find middle (fast/slow) → reverse second half → merge two halves alternately |

## Worked Pattern: Linked List Cycle Detection + Finding Cycle Start (Floyd's, full version)
```python
def detectCycle(head):
    slow = fast = head
    # Phase 1: determine if a cycle exists
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None   # no cycle (loop exited normally, not via break)

    # Phase 2: find the start of the cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    return slow   # start of the cycle
```
**Why Phase 2 works (the math interviewers may ask you to justify):**
Let the distance from head to the cycle start be `a`, and from the cycle start to the meeting point be `b`. When `slow` and `fast` meet, it can be shown that resetting one pointer to `head` and advancing both **one step at a time** causes them to meet again exactly at the cycle's start — because the remaining distance for the head-reset pointer to reach the cycle start (`a`) equals the remaining distance for the in-cycle pointer to loop back around to the start.

## Worked Pattern: Remove Nth Node From End
```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next          # fast gets n steps ahead
    while fast.next:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next    # slow is now just before the node to remove
    return dummy.next
```
**Complexity:** O(n) time, O(1) space, single pass.

## Common Pitfalls
- Forgetting the null-check guard `while fast and fast.next` — without it, `fast.next.next` throws on a list with even length or near the end.
- Off-by-one in the "N steps ahead" setup for Remove Nth From End — verify with a small example (e.g., a 2-node list, remove the 1st from end) before trusting the code.
- Assuming cycle detection alone answers "where does the cycle start" — that requires the full two-phase Floyd's algorithm, not just Phase 1.
- Forgetting to use a **dummy node** before `head` when the operation might remove the head itself (e.g., removing the Nth-from-end when N equals the list length).

## Interview Talking Points
- Be ready to derive (not just recite) why Floyd's Phase 2 correctly finds the cycle start — this is one of the most common "prove it" follow-ups in linked-list interviews.
- State the space trade-off explicitly: fast/slow gives O(1) space vs. an O(n) space hashmap-of-visited-nodes approach to the same cycle-detection problem — a strong candidate mentions both and explains why fast/slow is preferred.

---

## 📋 Quick Cross-Topic Revision Table

| Question to Ask Yourself | If Yes → | If No → |
|---|---|---|
| Do I only ever need to traverse forward? | Singly Linked List | Doubly Linked List |
| Do I need O(1) delete/insert given just a node reference (no predecessor search)? | Doubly Linked List | Singly Linked List (need predecessor tracking) |
| Am I finding a middle, detecting a cycle, or finding Nth-from-end? | Fast & Slow Pointers | — |
| Does the last node intentionally point back into the list (round-robin, buffer)? | Circular Linked List | — |
| Building a new list by appending nodes one at a time? | Use a **dummy head** to avoid special-casing the first node | — |
| Designing a cache/history structure needing O(1) reordering + O(1) lookup? | Doubly Linked List + HashMap (LRU Cache pattern) | — |

## Suggested NeetCode 150 Problem Set for This Section
- **Singly Linked List:** Reverse Linked List, Merge Two Sorted Lists, Reorder List, Remove Nth Node From End of List, Add Two Numbers
- **Doubly Linked List:** LRU Cache, Design Browser History, Flatten a Multilevel Doubly Linked List
- **Fast & Slow Pointers:** Linked List Cycle, Linked List Cycle II, Middle of the Linked List, Palindrome Linked List
