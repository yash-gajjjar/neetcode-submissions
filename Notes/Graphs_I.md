# Graphs I — DSA Interview Notes
*Intro to Graphs · Adjacency List · Matrix DFS · Matrix BFS*

> **Part I of II.** This covers graph fundamentals, representation, and grid-based (matrix) DFS/BFS. General graph traversal on adjacency lists, Union-Find, topological sort, and shortest-path algorithms (Dijkstra, etc.) are covered separately in Graphs II.

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the diagrams by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each section.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right technique in <10 seconds.

All code examples in Python.

---

## 🔑 Cheat Sheet — All Four Sections at a Glance
| Section | Core Idea | Time | Space |
|---|---|---|---|
| Intro to Graphs | Nodes + edges, with directed/undirected and weighted/unweighted variants | — | — |
| Adjacency List | Map each node to a list of its neighbors — the standard graph representation | O(V + E) to build | O(V + E) |
| Matrix DFS | Treat a 2D grid as an implicit graph; explore deep before wide, using recursion or an explicit stack | O(rows × cols) | O(rows × cols) worst case (recursion stack) |
| Matrix BFS | Treat a 2D grid as an implicit graph; explore level by level using a queue | O(rows × cols) | O(rows × cols) worst case (queue) |

**Core shared idea:** a graph is just "things connected to other things" — a grid is a special case where each cell is implicitly connected to its (usually 4) neighbors, so grid problems are graph problems in disguise. Whether you traverse depth-first or breadth-first depends on what you're trying to find (any connected region vs. shortest distance).

---

# 1. Intro to Graphs

## 🔑 Cheat Sheet
| Term | Meaning |
|---|---|
| Vertex (Node) | A single entity in the graph |
| Edge | A connection between two vertices |
| Directed graph | Edges have a direction (A→B doesn't imply B→A) |
| Undirected graph | Edges go both ways (A–B implies B–A) |
| Weighted graph | Edges carry a cost/weight (distance, time, etc.) |
| Unweighted graph | All edges are treated as equal cost (commonly cost = 1) |
| Cycle | A path that starts and ends at the same vertex |
| Connected component | A maximal set of vertices all reachable from one another |
| Degree (of a vertex) | Number of edges attached to it (in-degree/out-degree for directed graphs) |

## Core Intuition
A graph generalizes the tree structure from the previous topic: trees are graphs with **no cycles and exactly one path between any two nodes**; graphs allow cycles, disconnected pieces, multiple paths, and edges in both directions. Almost every "trees" technique (DFS, BFS) directly extends to graphs — the main new concern is **avoiding revisiting nodes**, since cycles mean naive traversal could loop forever.

```
Undirected graph:          Directed graph:
   A --- B                    A --> B
   |     |                    ^     |
   C --- D                    |     v
                               D <-- C
```

## Why This Matters for Interviews
- **Trees are a special case of graphs** — if you understand tree DFS/BFS, graph DFS/BFS is the same idea plus a **visited set** to prevent infinite loops on cycles.
- Recognizing **directed vs. undirected** early changes your approach — e.g., cycle detection logic differs meaningfully between the two (see Graphs II for full cycle-detection coverage).
- A **grid** is simply a graph where nodes are cells and edges connect adjacent cells — this reframing is the key insight behind Matrix DFS/BFS (§3, §4).

---

# 2. Adjacency List

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Structure | `dict` mapping each node → list of its neighbors |
| Build time | O(V + E) — one entry per vertex, one append per edge |
| Space | O(V + E) — proportional to actual connections, not V² |
| vs. Adjacency Matrix | Adjacency list is better for **sparse** graphs (few edges); a V×V matrix wastes space when most pairs aren't connected, but gives O(1) "are u and v connected?" checks |

## Core Intuition
An adjacency list stores, for each node, only the nodes it's **actually connected to** — avoiding the O(V²) space of a full matrix when most pairs of nodes have no edge between them (the common case in most interview problems: course prerequisites, social networks, city road maps, etc.).

```
Edges: A-B, A-C, B-D

Adjacency List:
{
  "A": ["B", "C"],
  "B": ["A", "D"],
  "C": ["A"],
  "D": ["B"]
}
```

## Building an Adjacency List (Python)
```python
from collections import defaultdict

def build_adjacency_list(n, edges, directed=False):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)     # undirected: add both directions
    return graph
```
**Key idea:** for an **undirected** graph, every edge must be added in both directions; for a **directed** graph, only add it in the direction given.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "list of edges / list of (course, prerequisite) pairs given" | Build an adjacency list first — almost always the first step before any traversal |
| "given `n` nodes and a list of edges" | `defaultdict(list)`, populate from the edge list |
| "weighted edges" (e.g., `(u, v, weight)`) | Adjacency list of `(neighbor, weight)` tuples instead of plain neighbor lists |
| "is there an edge between u and v?" asked frequently | Consider an adjacency **set** (`defaultdict(set)`) instead of a list for O(1) membership checks |

## Common Pitfalls
- Forgetting to add both directions for an **undirected** graph — a very common source of "why didn't my BFS/DFS visit this node" bugs.
- Using a list where repeated `"is v in graph[u]"` checks are needed — that's O(degree) per check; a set gives O(1) if membership checks are frequent.
- Not initializing entries for **isolated nodes** (nodes with no edges) if the problem needs to account for them — `defaultdict(list)` handles this gracefully since accessing a missing key just returns an empty list, but explicit node counts (e.g., `n` given separately from edges) should still be checked when counting connected components.

## Interview Talking Points
- State explicitly why you're choosing adjacency list over matrix: "the graph is sparse, so adjacency list is O(V+E) space instead of O(V²)" — this is a fast, clean way to signal you understand the trade-off rather than defaulting to one representation out of habit.

---

# 3. Matrix DFS

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Core idea | Treat each grid cell as a graph node; edges connect it to (typically) its 4 orthogonal neighbors (sometimes 8, if diagonals count) |
| Traversal | Recursive DFS (or explicit stack), exploring one direction fully before backtracking |
| Visited tracking | Mark cells visited **in place** (mutate the grid, e.g., `'1'` → `'0'`) or use a separate `visited` set/2D array |
| Complexity | O(rows × cols) — each cell visited once |

## Core Intuition
A 2D grid is an **implicit graph**: instead of an explicit adjacency list, neighbors are computed on the fly using offset directions. DFS on a grid explores as far as possible in one direction (e.g., through a connected region of land, or through a maze path) before backtracking — exactly the same DFS mechanism as trees/graphs, just with neighbors computed via `(row ± 1, col)` / `(row, col ± 1)` instead of `.left`/`.right` or an adjacency list lookup.

```
Grid (1 = land, 0 = water):
1 1 0
0 1 0
0 0 1

DFS from (0,0): visits (0,0) → (0,1) → (1,1)  → all connected 1's found
Then a separate DFS from (2,2) finds the isolated island there.
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "count number of islands / connected regions in a grid" | Matrix DFS from each unvisited land cell, marking the whole connected region visited per DFS call |
| "flood fill" | Matrix DFS from the starting cell, changing/marking connected cells matching the original color |
| "max area of an island" | Matrix DFS, accumulate a count of cells visited per connected region, track the max |
| "surrounded regions" (mark regions not touching the border) | Matrix DFS from all border cells first (these are "safe"), then whatever's left unmarked and not on the border gets flipped |
| "number of enclaves / paths that can't escape" | Matrix DFS from border cells to identify "escapable" cells, similar to Surrounded Regions |

## Worked Pattern: Number of Islands (Matrix DFS)
```python
def numIslands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return                                  # out of bounds or not land — stop
        grid[r][c] = '0'                             # mark visited (in place)
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)                             # sink the entire connected island
    return count
```
**Key idea:** every time the outer loop finds an unvisited `'1'`, it's the **start of a brand-new island** — the DFS call that follows visits (and marks) every cell connected to it, so the outer loop will never re-count any cell belonging to that same island.

## Common Pitfalls
- Forgetting the **bounds check** (`r < 0 or r >= rows or c < 0 or c >= cols`) before accessing `grid[r][c]` — causes an index error.
- Marking a cell visited **after** recursing instead of **before** — this can cause infinite recursion/re-visits, since a neighbor's DFS call might revisit the same cell before it's marked.
- Using recursion on very large grids — Python's recursion limit (~1000 by default) can be exceeded; mention iterative DFS (explicit stack) as a fallback for large inputs.
- Mutating the input grid when the problem expects it unchanged — if so, use a separate `visited` set/2D boolean array instead of overwriting grid values.

## Interview Talking Points
- Explicitly connect this back to tree DFS: "this is the same DFS pattern as tree traversal, except neighbors are computed via grid offsets instead of `.left`/`.right` pointers, and I need a visited check to avoid infinite loops since grids have cycles (trees don't)."
- If the grid is large, proactively mention the recursion-depth risk and offer the iterative stack-based alternative.

---

# 4. Matrix BFS

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Core idea | Same implicit-graph grid model as Matrix DFS, but explore level by level using a queue |
| When to prefer over DFS | Whenever you need the **shortest path / minimum steps** in an unweighted grid — BFS guarantees the first time you reach a cell is via the shortest path |
| Complexity | O(rows × cols) time, O(rows × cols) space (queue can hold up to a full "ring" of the grid) |

## Core Intuition
Just like BFS on trees finds the minimum depth by exploring the nearest nodes first, BFS on a grid finds the **shortest number of steps** to reach a target cell, because it expands outward one "ring" of distance at a time — nothing farther away is explored until everything closer has been fully processed.

```
Grid, find shortest path from S to E (0 = open, X = wall):
S 0 0
X X 0
0 0 E

BFS explores in rings of increasing distance from S,
guaranteeing E is reached via the shortest possible path
the first time it's dequeued.
```

## Worked Pattern: Shortest Path in Binary Matrix (Matrix BFS)
```python
from collections import deque

def shortestPathBinaryMatrix(grid):
    n = len(grid)
    if grid[0][0] != 0 or grid[n-1][n-1] != 0:
        return -1

    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]  # 8-directional
    queue = deque([(0, 0, 1)])   # (row, col, path_length)
    visited = {(0, 0)}

    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == (n - 1, n - 1):
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited and grid[nr][nc] == 0:
                visited.add((nr, nc))              # mark visited WHEN ENQUEUED, not when dequeued
                queue.append((nr, nc, dist + 1))

    return -1
```
**Key idea — mark visited at enqueue time, not dequeue time:** if you wait until a cell is dequeued to mark it visited, the same cell can be added to the queue multiple times (via different neighbors) before being processed, wasting work and potentially causing incorrect distance tracking. Marking at **enqueue time** guarantees each cell enters the queue exactly once.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "minimum number of steps to reach a target in a grid" | Matrix BFS — guarantees shortest path in an unweighted grid |
| "rotting oranges" (multi-source spread over time) | Multi-source BFS — start with **all** initially "infected"/"rotten" cells in the queue simultaneously, track levels as time steps |
| "walls and gates" (distance from each cell to nearest gate) | Multi-source BFS, starting from all gates at once |
| "shortest bridge" (connect two islands with minimum steps) | DFS to find one island's boundary, then multi-source BFS from that boundary to reach the other island |
| "01 matrix" (distance from each cell to nearest 0) | Multi-source BFS from all 0-cells simultaneously |

## Worked Pattern: Rotting Oranges (Multi-Source BFS)
```python
from collections import deque

def orangesRotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))            # all initially-rotten oranges start together
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while queue:
        r, c, minute = queue.popleft()
        minutes = max(minutes, minute)
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, minute + 1))

    return minutes if fresh == 0 else -1
```
**Key idea — multi-source BFS:** instead of starting from a single source, **all** rotten oranges are pushed into the queue at the start (all at "minute 0"). This makes BFS naturally compute "distance from the nearest rotten orange" for every fresh orange in a single pass, rather than running a separate BFS per source and taking the minimum.

## Common Pitfalls
- Marking visited at **dequeue** time instead of **enqueue** time — allows duplicate entries in the queue for the same cell, wasting time and occasionally causing incorrect results.
- Using DFS instead of BFS for "shortest path/minimum steps" problems — DFS finds *a* path but has no guarantee it's the shortest without extra bookkeeping (see Trees notes, §5, for the same distinction in tree context).
- Forgetting **multi-source BFS** when multiple starting points exist simultaneously (Rotting Oranges, Walls and Gates, 01 Matrix) — running BFS separately from each source and combining results is far less efficient than starting all sources in the queue together.
- Off-by-one in distance tracking — decide whether `dist` starts at 0 or 1 for the source cell(s) and be consistent with what the problem is actually asking for (steps vs. cells visited).

## Interview Talking Points
- Immediately name "multi-source BFS" when a problem has multiple simultaneous starting points — this is a strong, specific signal of pattern recognition beyond just "I'll use BFS."
- When comparing to Matrix DFS, be explicit: "I'm choosing BFS here specifically because the problem asks for the *minimum* number of steps — DFS would find a valid path but not necessarily the shortest one."

---

## 📋 Quick Cross-Section Revision Table

| Question to Ask Yourself | If Yes → |
|---|---|
| Am I given a list of edges / pairs rather than a grid? | Build an Adjacency List first |
| Is the graph sparse (most pairs of nodes NOT connected)? | Adjacency List over Adjacency Matrix |
| Do I need to find connected regions / flood-fill / area of a region in a grid? | Matrix DFS |
| Do I need the shortest path / minimum steps in an unweighted grid? | Matrix BFS |
| Are there multiple simultaneous starting points (rot spreading, multiple gates)? | Multi-Source BFS |
| Is this really just tree DFS/BFS with cycles possible? | Same technique, but add a **visited** check to avoid infinite loops |

## Suggested Problem Set for This Section
- **Fundamentals/Adjacency List:** (conceptual — used as setup for most graph problems below and in Graphs II)
- **Matrix DFS:** Number of Islands, Max Area of Island, Flood Fill, Surrounded Regions, Number of Enclaves
- **Matrix BFS:** Shortest Path in Binary Matrix, Rotting Oranges, Walls and Gates, 01 Matrix, Shortest Bridge (DFS + BFS combined)

---
*Format matches your Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, Tries, and Backtracking notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*

*Graphs II (general adjacency-list traversal, Union-Find, topological sort, Dijkstra, and related algorithms) to follow separately.*
