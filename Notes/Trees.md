# Trees — DSA Interview Notes
*Tree Fundamentals · Building a Binary Tree · DFS Traversals (In/Pre/Post-order) · Iterative DFS · BFS (Level Order) · Binary Search Trees · BST Sets & Maps*

> **Note on sources:** Your list had overlap between the YouTube fundamentals series and NeetCode's course — "Level order traversal" (YouTube) is the same concept as "Breadth-First Search" (NeetCode), and "In/Pre/Post-order traversal" (YouTube) are the three recursive flavors of what NeetCode calls "Depth-First Search." These have been merged below into single sections so you're not studying the same concept twice under different names.

---

All code examples in Python.

---

## 🔑 Cheat Sheet — Everything at a Glance
| Concept | Core Idea | Time | Space |
|---|---|---|---|
| DFS (In/Pre/Post-order) | Recursively go deep before wide; order of visiting root vs. children differs | O(n) | O(h) recursion stack, h = height |
| Iterative DFS | Same traversal orders, using an explicit stack instead of recursion | O(n) | O(h) explicit stack |
| BFS / Level Order | Visit level by level, using a queue | O(n) | O(w), w = max width of tree |
| BST Insert/Remove | Use ordering property to navigate in O(h) instead of scanning all nodes | O(h) avg, O(n) worst (skewed) | O(h) recursion or O(1) iterative |
| BST as Set/Map | Ordering property gives sorted iteration + O(h) lookup "for free" | O(h) | O(n) |

**Core shared idea:** almost every tree problem is either **DFS-shaped** (explore fully before backtracking — good for path/subtree problems) or **BFS-shaped** (explore level by level — good for shortest-path/level-grouping problems). Recognizing which shape a problem needs is the single highest-leverage skill in this topic.

---

# 1. Tree Fundamentals & Terminology

## 🔑 Cheat Sheet
| Term | Meaning |
|---|---|
| Node | A single element containing a value and pointers to children |
| Root | The topmost node (no parent) |
| Leaf | A node with no children |
| Edge | The link between a parent and a child |
| Depth (of a node) | Number of edges from root to that node |
| Height (of a node) | Number of edges on the longest path from that node down to a leaf |
| Height (of a tree) | Height of the root |
| Subtree | A node and all its descendants, treated as a tree itself |
| Binary Tree | Each node has **at most 2 children** (commonly labeled left/right) |

## Types of Binary Trees
| Type | Definition |
|---|---|
| **Full** | Every node has 0 or 2 children (never exactly 1) |
| **Complete** | All levels filled except possibly the last, which fills left to right |
| **Perfect** | All internal nodes have 2 children AND all leaves are at the same depth |
| **Balanced** | Height difference between left and right subtrees of every node is ≤ 1 (or bounded by O(log n) generally) |
| **Degenerate (skewed)** | Each parent has only one child — effectively a linked list; worst case for BST performance |

```
Perfect:              Complete:              Degenerate:
      1                    1                       1
    /   \                /   \                      \
   2     3              2     3                       2
  / \   / \            / \                              \
 4   5 6   7          4   5                               3
```

## Why This Matters for Interviews
- **Height vs. depth** confusion is extremely common — depth is measured *from the root down to* a node; height is measured *from a node down to* the furthest leaf. Root's depth = 0; a leaf's height = 0.
- **Balanced vs. degenerate** matters directly for complexity: a balanced BST gives O(log n) operations, but a degenerate (skewed) tree degrades to O(n) — this is *the* key trade-off discussed in BST sections below.

---

# 2. Creating / Building a Binary Tree

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Node definition | A class/struct with `val`, `left`, `right` |
| Common construction inputs | Level-order array (e.g., LeetCode-style `[3,9,20,null,null,15,7]`), or preorder+inorder traversal pairs |
| Complexity to build from traversal(s) | O(n) with a hashmap for index lookup; O(n²) naive |

## Node Definition (Python)
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## Worked Pattern: Build Tree from Preorder + Inorder Traversal
```python
def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None

    root_val = preorder[0]
    root = TreeNode(root_val)
    mid = inorder.index(root_val)   # split point in inorder

    root.left = buildTree(preorder[1:mid + 1], inorder[:mid])
    root.right = buildTree(preorder[mid + 1:], inorder[mid + 1:])
    return root
```
**Key idea:** preorder always gives you the **root first**; inorder tells you which values are in the **left subtree vs. right subtree** relative to that root (everything before the root's position in inorder is the left subtree, everything after is the right subtree). Recurse on each side.
**Complexity:** O(n²) as written (due to `.index()` and slicing) — optimize to O(n) with a value→index hashmap and index-based recursion instead of slicing, worth mentioning in an interview.

## Common Pitfalls
- Confusing which traversal identifies the root (preorder/root-first) vs. which splits left/right subtrees (inorder).
- Using list slicing repeatedly — clean to write, but adds hidden O(n) cost per call; a strong candidate flags this and offers the index-based O(n) optimization.
- Forgetting the base case (`if not preorder: return None`) — infinite recursion or index errors otherwise.

---

# 3. DFS Traversals — In-order, Pre-order, Post-order

## 🔑 Cheat Sheet
| Traversal | Visit Order | Typical Use |
|---|---|---|
| **In-order** | Left → Root → Right | Produces sorted output **for a BST**; used for validating BST property |
| **Pre-order** | Root → Left → Right | Copying/serializing a tree (root written before children — easy to reconstruct) |
| **Post-order** | Left → Right → Root | Deleting a tree safely (children before parent), computing subtree-dependent values (height, sum) bottom-up |

## Core Intuition
All three are **DFS** — the difference is purely *when* you process the current node relative to recursing into its children. This single-line difference in code produces very different outputs and serves very different purposes.

```
        1
       / \
      2   3
     / \
    4   5

In-order:   4, 2, 5, 1, 3   (left, root, right)
Pre-order:  1, 2, 4, 5, 3   (root, left, right)
Post-order: 4, 5, 2, 3, 1   (left, right, root)
```

## Recursive Implementations (Python)
```python
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]
```
*(List concatenation above is clean for teaching; in interviews, prefer passing a shared `result` list by reference to avoid O(n) concatenation cost at every level.)*

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "validate binary search tree" | In-order traversal — must produce strictly increasing values |
| "serialize/deserialize a tree" | Pre-order (root-first makes reconstruction straightforward) |
| "compute height/depth of tree" | Post-order — need children's heights before computing parent's |
| "diameter of binary tree" | Post-order — need subtree heights bottom-up to compute diameter at each node |
| "delete/free a tree bottom-up" | Post-order — process children before the node itself |
| "sum/aggregate values dependent on subtree results" | Post-order — classic "bottom-up" DFS shape |
| "path from root to leaf / root-to-node path problems" | Pre-order-style DFS, carrying a running path down through recursion |

## Worked Pattern: Diameter of Binary Tree (post-order, bottom-up)
```python
def diameterOfBinaryTree(root):
    diameter = 0

    def height(node):
        nonlocal diameter
        if not node:
            return 0
        left_h = height(node.left)
        right_h = height(node.right)
        diameter = max(diameter, left_h + right_h)   # update using children's results
        return 1 + max(left_h, right_h)               # return height upward

    height(root)
    return diameter
```
**Complexity:** O(n) — each node visited once, height computed bottom-up rather than recomputed per node (which would be O(n²)).

## Common Pitfalls
- Computing height **separately for every node** (calling a height function inside another traversal) — turns O(n) into O(n²). Compute bottom-up in a single post-order pass instead, as shown above.
- Confusing in-order with "the traversal that always outputs sorted order" — that's only true when the tree is a **valid BST**; for a general binary tree, in-order has no such guarantee.
- Forgetting the base case `if not root: return ...` matching the correct type (0 for counts, `[]` for lists, `float('-inf')` for max problems, etc.).

## Interview Talking Points
- State explicitly which traversal shape (top-down "pass info down" vs. bottom-up "combine children's results") a problem needs — this framing alone shows strong tree fluency.
- For validate-BST, mention the common trap: comparing only `node.val` to its immediate children isn't sufficient — you need to track a valid `(low, high)` range through recursion, or use in-order and check strict monotonicity.

---

# 4. Iterative DFS

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Data structure | Explicit stack, simulating the recursion call stack |
| Why use it | Avoids recursion depth limits (Python's default recursion limit ~1000); some interviewers explicitly ask for iterative solutions |
| Order to push children | Push in **reverse** of desired visit order (stack is LIFO — last pushed is processed first) |

## Core Intuition
Recursive DFS implicitly uses the **call stack** to remember "what to do next" after finishing a subtree. Iterative DFS makes that stack **explicit**, giving you full control (useful when recursion depth would exceed limits, or when an interviewer wants to see you understand what recursion does under the hood).

## Worked Pattern: Iterative Pre-order Traversal
```python
def preorderIterative(root):
    if not root:
        return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:            # push right FIRST
            stack.append(node.right)
        if node.left:              # push left SECOND — so it's popped first
            stack.append(node.left)
    return result
```
**Key idea:** since a stack is LIFO, to visit **left before right**, you must push **right first, then left** — the last one pushed comes out first.

## Worked Pattern: Iterative In-order Traversal
```python
def inorderIterative(root):
    stack, result = [], []
    curr = root
    while curr or stack:
        while curr:                 # go as far left as possible, pushing along the way
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()          # backtrack to the most recent unvisited node
        result.append(curr.val)
        curr = curr.right           # then explore its right subtree
    return result
```
**Key idea:** in-order is trickier than pre-order iteratively because you must fully descend left *before* recording a value — the inner `while curr` loop handles this descent, and popping represents "backtracking up" to process a node after its left subtree is exhausted.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "traverse without recursion" / "avoid stack overflow on deep trees" | Iterative DFS with explicit stack |
| "binary tree inorder traversal, follow up: can you do it iteratively?" | Iterative in-order pattern above |
| "flatten binary tree to linked list" | Iterative or recursive pre-order-style rewiring |

## Common Pitfalls
- Pushing left before right in iterative pre-order — reverses the intended visit order (must push right first).
- Forgetting post-order iterative is the trickiest of the three (commonly done via two stacks, or one stack with a "last visited node" tracker) — if asked, be ready to reason through it rather than expecting a one-line trick like pre-order.
- Conflating iterative DFS (stack) with BFS (queue) — same "explicit data structure" idea, but stack vs. queue produces fundamentally different traversal orders.

## Interview Talking Points
- If asked "can you do this without recursion?", immediately connect it to simulating the call stack explicitly — this signals you understand *why* recursion and an explicit stack are equivalent, not just that you memorized the iterative code.

---

# 5. BFS / Level Order Traversal

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Data structure | Queue (FIFO) — `collections.deque` in Python for O(1) pops from the front |
| Core idea | Process all nodes at depth `d` before any node at depth `d+1` |
| Complexity | O(n) time, O(w) space where w = maximum width of the tree |

## Core Intuition
BFS explores **level by level**, using a queue so that nodes are processed in the same order they were discovered (unlike DFS's stack, which processes the most recently discovered node first). This makes BFS the natural fit for anything involving **levels**, **shortest path in an unweighted structure**, or **level-grouped output**.

```
        1
       / \
      2   3
     / \   \
    4   5   6

BFS order: 1, 2, 3, 4, 5, 6   (level by level, left to right within a level)
```

## Worked Pattern: Level Order Traversal (grouped by level)
```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level_size = len(queue)      # snapshot: exactly how many nodes are in this level
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```
**Key idea — the `level_size` snapshot:** taking `len(queue)` *before* the inner loop is what separates "process one level at a time" from "process the whole queue as one blob." New nodes get appended to the queue during the loop, but the snapshot ensures you only process the nodes that existed at the start of this level.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "level order traversal" / "group nodes by level" | BFS with level-size snapshot |
| "right side view of a tree" | BFS, take the last node of each level |
| "minimum depth of binary tree" | BFS — first leaf found is guaranteed to be at minimum depth (unlike DFS, which might explore a longer path first) |
| "zigzag level order traversal" | BFS + alternate reversing each level's order |
| "connect nodes at the same level" (populate next pointers) | BFS, link nodes within the same level snapshot |
| "shortest path in a binary tree / grid (unweighted)" | BFS — guarantees shortest path is found first, unlike DFS |

## Common Pitfalls
- Forgetting the `level_size` snapshot — without it, the inner loop boundary is wrong and levels get mixed together.
- Using a plain `list` with `pop(0)` instead of `collections.deque` — `list.pop(0)` is O(n), silently turning BFS into O(n²) overall.
- Reaching for DFS on a "minimum depth" or "shortest path" problem — DFS can find *a* path but not necessarily the *shortest* one without extra bookkeeping; BFS finds it naturally by exploring closest nodes first.

## Interview Talking Points
- For "minimum depth," explicitly contrast with DFS: DFS might dive down a long branch first and waste work, while BFS guarantees the first leaf encountered is at the true minimum depth — this comparison is a strong signal of understanding *why* to choose BFS over DFS, not just recalling that BFS exists.

---

# 6. Binary Search Trees (BST) — Insert and Remove

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| BST property | For every node: all values in left subtree < node.val < all values in right subtree |
| Search/Insert/Delete | O(h) — h = tree height; O(log n) if balanced, O(n) if degenerate/skewed |
| In-order traversal of a BST | Always produces values in **sorted order** — a defining, testable property |

## Core Intuition
A BST is a binary tree with an ordering invariant that lets you **eliminate half the remaining subtree** at each step during search — the same halving idea as Binary Search on Array, just expressed as a tree instead of a flat array. This is why BST operations are O(h) rather than O(n): each comparison sends you left or right, never both.

## Worked Pattern: BST Search / Insert
```python
def searchBST(root, val):
    if not root or root.val == val:
        return root
    return searchBST(root.left, val) if val < root.val else searchBST(root.right, val)

def insertIntoBST(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insertIntoBST(root.left, val)
    else:
        root.right = insertIntoBST(root.right, val)
    return root
```

## Worked Pattern: BST Delete (the tricky one — 3 cases)
```python
def deleteNode(root, key):
    if not root:
        return None

    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        # found the node to delete — 3 cases:
        if not root.left:                     # case 1: no left child (0 or 1 child)
            return root.right
        if not root.right:                    # case 2: no right child
            return root.left
        # case 3: two children — replace with in-order successor
        successor = root.right
        while successor.left:                  # smallest value in right subtree
            successor = successor.left
        root.val = successor.val               # copy successor's value up
        root.right = deleteNode(root.right, successor.val)  # remove the successor's original node

    return root
```
**Key idea — the two-children case:** you can't just remove the node (it has two subtrees to preserve). Instead, find its **in-order successor** (smallest value in the right subtree — guaranteed to be > everything in left subtree, < everything else in right subtree), copy that value into the node being "deleted," then recursively delete the successor's original (now-duplicate) node, which is guaranteed to have at most one child.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "insert/search/delete in a BST" | Direct use of ordering property, O(h) |
| "validate binary search tree" | In-order traversal check (strictly increasing), or recursive `(low, high)` bound passing |
| "kth smallest element in a BST" | In-order traversal, stop at the kth element (leverages sorted-order property) |
| "lowest common ancestor in a BST" | Use ordering: if both values < node, go left; if both > node, go right; else current node is the LCA |
| "convert sorted array to balanced BST" | Recursively pick the middle element as root (mirrors binary search's midpoint logic) |

## Common Pitfalls
- Only comparing a node to its **immediate** children when validating a BST — must maintain a valid `(low, high)` range through the whole recursion, since a node deep in the left subtree must be less than *every* ancestor above-and-to-the-right, not just its immediate parent.
- Forgetting the 3-case structure of delete — most bugs come from mishandling the two-children case.
- Assuming O(log n) — a BST built from already-sorted input degenerates into a skewed (effectively linked-list) tree with O(n) operations, unless self-balancing (AVL/Red-Black) is used.

## Interview Talking Points
- Always mention the worst-case degenerate scenario when discussing BST complexity — strong candidates say "O(log n) average, O(n) worst case if unbalanced" rather than just "O(log n)."
- Be ready to connect BST search directly back to Binary Search on Array — same halving logic, different underlying structure.

---

# 7. BST Sets and Maps

## 🔑 Cheat Sheet
| Structure | What It Gives You "For Free" | Backing Structure (typical) |
|---|---|---|
| TreeSet / TreeMap (ordered set/map) | Sorted iteration, O(log n) floor/ceiling/range queries, O(log n) insert/search/delete | Self-balancing BST (Red-Black tree in Java's `TreeMap`, etc.) |
| Plain HashSet/HashMap | O(1) average lookup, **no ordering** | Hash table (see Hash Implementation notes) |

## Core Intuition
A hashmap gives you O(1) lookup but **no ordering** — you can't efficiently ask "what's the smallest key ≥ X?" or "give me all keys in sorted order" without extra work. A **BST-backed** map/set trades O(1) for O(log n) lookup in exchange for maintaining sorted order, which unlocks range queries, floor/ceiling lookups, and ordered iteration directly.

**Python note:** Python's standard library doesn't have a built-in balanced BST map/set (unlike Java's `TreeMap`/`TreeSet`). In interviews, this is usually simulated with the `sortedcontainers` library (`SortedList`, `SortedDict`) if allowed, or by explicitly discussing that you'd use a self-balancing BST if implementing from scratch.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "find the closest value ≤/≥ X in a dynamic set" (floor/ceiling) | Ordered set/map (BST-backed) — `sortedcontainers.SortedList` with `bisect` in Python |
| "maintain a running sorted structure with frequent insert/delete" | Ordered set/map — better than resorting an array every time (O(n log n) per resort vs. O(log n) per op) |
| "range query: count/sum of elements between L and R, with updates" | Ordered structure, or ties back to Fenwick/Segment Tree (mentioned in Prefix Sums notes) for even better range-update performance |
| "calendar/interval scheduling with dynamic insert and neighbor lookup" | Ordered map keyed by start time, using floor/ceiling to find overlapping neighbors |

## Worked Pattern: Simulating an Ordered Set in Python (via `sortedcontainers` or `bisect`)
```python
import bisect

class OrderedSetSim:
    def __init__(self):
        self.data = []

    def insert(self, val):
        idx = bisect.bisect_left(self.data, val)
        if idx == len(self.data) or self.data[idx] != val:
            self.data.insert(idx, val)   # O(n) insert on plain list — a real TreeSet would be O(log n)

    def contains(self, val):
        idx = bisect.bisect_left(self.data, val)
        return idx < len(self.data) and self.data[idx] == val   # O(log n) search

    def ceiling(self, val):
        idx = bisect.bisect_left(self.data, val)
        return self.data[idx] if idx < len(self.data) else None
```
**Important caveat to state in interviews:** a plain Python list with `bisect` gives O(log n) **search** but O(n) **insert** (due to shifting elements) — a true BST-backed structure (or `sortedcontainers.SortedList`, which uses an internally chunked list) gets closer to O(log n) for both. Know this trade-off rather than presenting `bisect` as a full substitute for a balanced BST.

## Common Pitfalls
- Assuming Python's `bisect` module alone gives O(log n) insert — it only gives O(log n) *search*; the underlying `list.insert` is still O(n).
- Reaching for a plain hashmap/hashset when the problem explicitly needs **ordering** (closest value, range queries) — this is the clearest signal to reach for a BST-backed structure instead.
- Not mentioning the self-balancing requirement (AVL/Red-Black) when discussing "how would you implement a TreeMap from scratch" — a plain unbalanced BST can degrade to O(n), same caveat as §6.

## Interview Talking Points
- If a problem needs both **fast lookup** and **sorted order/range queries**, that combination is the clearest signal to reach for an ordered (BST-backed) set/map instead of a plain hashmap — name this trade-off explicitly.
- Be ready to mention `sortedcontainers.SortedList`/`SortedDict` as the practical Python answer, while acknowledging the true underlying data structure being approximated is a self-balancing BST.

---

## 📋 Quick Cross-Topic Revision Table

| Question to Ask Yourself | If Yes → | If No → |
|---|---|---|
| Do I need to explore full paths / combine results from subtrees? | DFS (pick in/pre/post-order based on when you need the current node's value) | — |
| Do I need shortest path, level grouping, or "closest to root" guarantees? | BFS | — |
| Recursion might hit a depth limit, or interviewer wants no recursion? | Iterative DFS (explicit stack) | Recursive DFS is fine |
| Does the tree maintain a left < node < right ordering invariant? | BST — leverage it for O(h) search/insert/delete | General binary tree — no shortcut, must visit more broadly |
| Do I need sorted iteration or floor/ceiling queries on a dynamic set? | BST-backed ordered set/map | Plain hashmap/hashset (O(1), no ordering) |
| Am I computing something bottom-up (height, sum, diameter)? | Post-order DFS | — |

## Suggested Problem Set for This Section
- **Traversals (recursive & iterative):** Binary Tree Inorder/Preorder/Postorder Traversal, Binary Tree Level Order Traversal
- **DFS-shaped:** Maximum Depth of Binary Tree, Diameter of Binary Tree, Balanced Binary Tree, Same Tree, Subtree of Another Tree, Invert Binary Tree, Path Sum
- **BFS-shaped:** Binary Tree Right Side View, Minimum Depth of Binary Tree, Zigzag Level Order Traversal
- **BST:** Validate Binary Search Tree, Insert into a BST, Delete Node in a BST, Kth Smallest Element in a BST, Lowest Common Ancestor of a BST, Convert Sorted Array to Balanced BST
