# Graphs II — DSA Interview Notes
*Dijkstra's Algorithm · Prim's Algorithm · Kruskal's Algorithm (+ Union-Find) · Topological Sort*

> **Part II of II.** Builds on Graphs I (Intro to Graphs, Adjacency List, Matrix DFS/BFS). This covers weighted shortest paths, minimum spanning trees, and dependency ordering — the classic "named algorithms" tier of graph interview questions.

---

All code examples in Python.

---

## 🔑 Cheat Sheet — All Four Algorithms at a Glance
| Algorithm | Solves | Core Data Structure | Time | Space |
|---|---|---|---|---|
| Dijkstra's | Shortest path from one source to all nodes (non-negative weights) | Min-heap (priority queue) | O((V + E) log V) | O(V + E) |
| Prim's | Minimum Spanning Tree (MST) — grows one connected tree | Min-heap (priority queue) | O((V + E) log V) | O(V + E) |
| Kruskal's | Minimum Spanning Tree (MST) — builds from globally cheapest edges | Sorted edge list + Union-Find | O(E log E) | O(V + E) |
| Topological Sort | Valid linear ordering of nodes in a DAG respecting dependencies | Queue (Kahn's/BFS) or stack (DFS) | O(V + E) | O(V + E) |

**Core shared idea:** all four are **greedy algorithms built on top of graph traversal** — at each step, they make the locally-cheapest or locally-most-available choice (nearest unvisited node, cheapest remaining edge, a node with no remaining dependencies) and prove that this greedy choice never needs to be undone. Recognizing the *shape* of the problem (shortest path? spanning tree? dependency order?) is what tells you which of the four to reach for.

---

# 1. Dijkstra's Algorithm

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Problem it solves | Shortest path from a single source to every other node, in a **weighted graph with non-negative edge weights** |
| Core data structure | Min-heap, storing `(distance, node)` — always process the closest unvisited node next |
| Precondition | All edge weights must be **≥ 0** — negative weights break the greedy guarantee (use Bellman-Ford instead, not covered here) |
| Complexity | O((V + E) log V) — each edge relaxation may push onto the heap, heap ops are O(log V) |

## Core Intuition
Dijkstra's is BFS's weighted cousin: instead of processing nodes in the order they're *discovered* (BFS's queue), it processes nodes in order of their **current known shortest distance** from the source (a min-heap). Once a node is popped from the heap with its final shortest distance confirmed, that distance can never improve — because every unexplored path only gets *longer* (weights are non-negative), so nothing still in the heap could possibly offer a shorter route to that node than the one just confirmed.

```
Source A, edges: A-B(4), A-C(1), C-B(2), B-D(1), C-D(5)

heap: [(0,A)]
pop A (dist 0): relax B→4, C→1        heap: [(1,C),(4,B)]
pop C (dist 1): relax B→min(4,1+2)=3, D→1+5=6   heap: [(3,B),(6,D),(4,B) stale]
pop B (dist 3): relax D→min(6,3+1)=4             heap: [(4,D),(6,D) stale]
pop D (dist 4): done

shortest distances: A=0, B=3, C=1, D=4
```

## Worked Pattern: Dijkstra's Algorithm
```python
import heapq
from collections import defaultdict

def dijkstra(n, edges, source):
    graph = defaultdict(list)
    for u, v, weight in edges:
        graph[u].append((v, weight))
        graph[v].append((u, weight))     # omit this line if the graph is directed

    dist = {i: float('inf') for i in range(n)}
    dist[source] = 0
    heap = [(0, source)]                  # (distance, node)

    while heap:
        curr_dist, node = heapq.heappop(heap)
        if curr_dist > dist[node]:
            continue                       # stale entry — a shorter path was already found
        for neighbor, weight in graph[node]:
            new_dist = curr_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist
```
**Key idea — the stale-entry check (`if curr_dist > dist[node]: continue`):** since a node's distance can be updated (and re-pushed) multiple times before it's finalized, the heap may contain multiple entries for the same node. When popped, an entry might reflect an already-outdated (larger) distance — checking against the current best-known `dist[node]` and skipping stale entries avoids doing wasted/incorrect relaxation work.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "shortest path in a weighted graph, non-negative weights" | Dijkstra's |
| "cheapest flight with at most K stops" | Modified Dijkstra's (or BFS with a stops-bound) — track `(cost, node, stops)` |
| "network delay time" (time for a signal to reach all nodes from a source) | Dijkstra's — answer is the max shortest distance across all nodes |
| "path with minimum effort / minimize the maximum edge on a path" | Modified Dijkstra's — relax based on `max(current_path_max, edge_weight)` instead of summing |
| "all weights equal to 1" | Plain BFS is sufficient and simpler — Dijkstra's is unnecessary overhead when weights are uniform |

## Common Pitfalls
- Using Dijkstra's with **negative edge weights** — the greedy "once popped, distance is final" guarantee breaks; a graph with negative weights needs Bellman-Ford instead.
- Forgetting the stale-entry check — without it, outdated heap entries can cause incorrect or wasted relaxations.
- Reaching for Dijkstra's when all edges have equal weight — plain BFS already finds the shortest path in that case, with less overhead (no heap needed).
- Not marking distances as `float('inf')` upfront for unreached nodes — needed so the `new_dist < dist[neighbor]` comparison works correctly on the first relaxation.

## Interview Talking Points
- Be ready to explain **why** the greedy approach is correct: once a node is popped with the smallest current distance in the heap, no future relaxation (which can only add non-negative weight) could ever produce a shorter path to it.
- If negative weights come up, immediately flag that Dijkstra's assumption is violated and name Bellman-Ford as the correct algorithm for that case (even if not asked to implement it) — shows awareness of the boundary of applicability.

---

# 2. Prim's Algorithm

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Problem it solves | Minimum Spanning Tree (MST) — connect all nodes with the minimum total edge weight, no cycles |
| Core data structure | Min-heap, storing `(weight, node)` — same structural shape as Dijkstra's |
| Strategy | Start from any node, repeatedly add the **cheapest edge that connects the growing tree to a new (unvisited) node** |
| Complexity | O((V + E) log V) |

## Core Intuition
Prim's is almost identical in *mechanics* to Dijkstra's — both use a min-heap to greedily pick the next node — but the **quantity being minimized is different**. Dijkstra's tracks *total distance from the source*; Prim's tracks the *weight of the single cheapest edge* connecting the current tree to each unvisited node. This is a subtle but important distinction: Prim's doesn't care about the path length to reach a node, only the cost of the **one edge** that would connect it to the tree right now.

```
Prim's grows ONE tree outward, always adding the cheapest
available edge to an unvisited node:

  A --4-- B          Start at A.
  |       |          Cheapest edge from tree {A}: A-C (1) → add C
  1       2          Cheapest edge from tree {A,C}: C-B (2) → add B
  |       |          Cheapest edge from tree {A,C,B}: B-D (1) → add D
  C       D
       5
  (A-C-B-D forms the MST, total weight 1+2+1=4;
   edge A-B (4) and C-D (5) are never used)
```

## Worked Pattern: Prim's Algorithm (MST total weight)
```python
import heapq
from collections import defaultdict

def prims_mst(n, edges):
    graph = defaultdict(list)
    for u, v, weight in edges:
        graph[u].append((weight, v))
        graph[v].append((weight, u))

    visited = set()
    min_heap = [(0, 0)]     # start from node 0, cost 0 to "add" it
    total_weight = 0

    while min_heap and len(visited) < n:
        weight, node = heapq.heappop(min_heap)
        if node in visited:
            continue                       # already part of the tree — skip
        visited.add(node)
        total_weight += weight
        for edge_weight, neighbor in graph[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, neighbor))

    return total_weight if len(visited) == n else -1   # -1 if graph is disconnected
```
**Key idea — comparing to Dijkstra's code:** the structure is nearly identical, but notice `heapq.heappush(min_heap, (edge_weight, neighbor))` pushes the **raw edge weight**, not an accumulated distance (`curr_dist + weight` as in Dijkstra's). That single difference is what turns "shortest path" into "minimum spanning tree."

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "connect all nodes/cities with minimum total cable/road cost" | Prim's (or Kruskal's — see §3 for when to prefer one over the other) |
| "minimum cost to connect all points" (often given as coordinates, requiring you to compute edge weights first, e.g. Manhattan distance) | Build a complete graph of pairwise distances, then Prim's (often more efficient here since the graph is dense) |
| "dense graph" (many edges relative to nodes) | Prim's tends to be preferred — heap operations scale with nodes touched, and a dense graph favors Prim's node-centric growth |

## Common Pitfalls
- Confusing Prim's "cheapest edge to extend the tree" with Dijkstra's "cheapest cumulative path from source" — pushing `curr_dist + weight` (Dijkstra's logic) into Prim's code by mistake produces a shortest-path tree, not a minimum spanning tree — these are **not the same thing** in general.
- Forgetting to check `if len(visited) == n` at the end to detect a disconnected graph — an MST only exists if the graph is fully connected.
- Not skipping already-visited nodes when popped from the heap — necessary since a node may have multiple stale heap entries.

## Interview Talking Points
- If asked "what's the difference between Prim's and Dijkstra's," lead with: "same greedy/heap mechanism, but Prim's minimizes the edge connecting the tree to a new node, while Dijkstra's minimizes the total path from the source — swapping one line of the relaxation logic changes which problem you're solving."
- Mention Prim's vs. Kruskal's trade-off proactively if MST comes up (see §3's comparison table) — this is a very common immediate follow-up question.

---

# 3. Kruskal's Algorithm (+ Union-Find)

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Problem it solves | Minimum Spanning Tree (MST) — same goal as Prim's, different strategy |
| Strategy | Sort **all edges** by weight; greedily add each edge if it doesn't form a cycle (checked via Union-Find) |
| Core data structure | Union-Find (Disjoint Set Union) — tracks which nodes are already connected |
| Complexity | O(E log E) — dominated by sorting edges; Union-Find operations are nearly O(1) amortized (with path compression + union by rank) |

## Core Intuition
While Prim's grows **one tree** outward node by node, Kruskal's considers **all edges globally**, sorted from cheapest to most expensive, and greedily accepts an edge as long as it **doesn't create a cycle** (i.e., the two endpoints aren't already connected). Union-Find is the tool that answers "are these two nodes already connected?" efficiently.

```
Edges sorted by weight: (A,C,1), (B,D,1), (B,C,2), (A,B,4), (C,D,5)

Add (A,C,1): A and C are in different components → add, union them
Add (B,D,1): B and D are in different components → add, union them
Add (B,C,2): B (in {B,D}) and C (in {A,C}) different → add, union them → all 4 connected
Add (A,B,4): A and B are now in the SAME component (cycle!) → skip
Add (C,D,5): also same component now → skip

MST edges: (A,C,1), (B,D,1), (B,C,2) — total weight 4
```

## Union-Find (Disjoint Set Union) Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False                                   # already connected — would form a cycle
        if self.rank[root_x] < self.rank[root_y]:           # union by rank
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        return True
```
**Key ideas:**
- **Path compression** (`self.parent[x] = self.find(self.parent[x])`) flattens the tree during lookups, so future `find` calls on the same nodes are faster.
- **Union by rank** attaches the smaller/shallower tree under the larger/deeper one, preventing the structure from becoming a long chain.
- Together, these give Union-Find a near-constant (technically O(α(n)), the inverse Ackermann function — effectively O(1) for all practical input sizes) amortized time per operation.

## Worked Pattern: Kruskal's Algorithm
```python
def kruskals_mst(n, edges):
    edges.sort(key=lambda e: e[2])       # sort by weight
    uf = UnionFind(n)
    total_weight = 0
    edges_used = 0

    for u, v, weight in edges:
        if uf.union(u, v):                # returns True if they were NOT already connected
            total_weight += weight
            edges_used += 1

    return total_weight if edges_used == n - 1 else -1   # -1 if graph is disconnected
```
**Key idea:** an MST on `n` nodes always has exactly `n - 1` edges — if fewer edges were successfully added, the graph is disconnected and no spanning tree exists.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "minimum spanning tree, sparse graph (relatively few edges)" | Kruskal's tends to be preferred — sorting cost dominates, and fewer edges means less to sort |
| "detect a cycle in an undirected graph" | Union-Find — if `union(u, v)` returns False, an edge closing a cycle was found |
| "number of connected components in a graph" | Union-Find — count the number of distinct roots after processing all edges |
| "redundant connection" (find the edge that creates a cycle) | Union-Find — process edges in given order, return the first edge where `union` returns False |
| "accounts merge / group items by shared relationships" | Union-Find — union all pairwise relationships, then group by root |

## Prim's vs. Kruskal's — When to Prefer Which
| Factor | Prefer Prim's | Prefer Kruskal's |
|---|---|---|
| Graph density | Dense (many edges) | Sparse (few edges) |
| Natural representation | Adjacency list, grow outward from a node | Edge list, sort globally |
| Conceptually simpler when... | You already have an adjacency-list + heap pattern from Dijkstra's | You need cycle detection as a side effect (Union-Find is broadly reusable) |

## Common Pitfalls
- Forgetting **path compression** or **union by rank** in the Union-Find implementation — without them, `find` can degrade toward O(n) per call in adversarial cases, hurting overall performance.
- Not checking `edges_used == n - 1` (or equivalently, all nodes connected) to detect a disconnected graph — Kruskal's will just silently return a "forest" (multiple disconnected trees) otherwise.
- Confusing Union-Find's usefulness **beyond MST** — it's a general "are these two things connected/grouped" tool, showing up in cycle detection, connected components, and grouping problems independent of Kruskal's specifically.

## Interview Talking Points
- Union-Find is one of the highest-leverage "small tool, many uses" structures in graph interviews — explicitly call it out as reusable for cycle detection and connected-components problems, not just MST.
- Be ready to state the Prim's vs. Kruskal's trade-off in one sentence (density of the graph) — this is a near-guaranteed follow-up once you've implemented either one.

---

# 4. Topological Sort

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Problem it solves | A linear ordering of nodes in a **Directed Acyclic Graph (DAG)** such that every edge `u → v` has `u` appearing before `v` |
| Precondition | Graph must have **no cycles** — a cycle means no valid topological order exists |
| Two approaches | **Kahn's Algorithm** (BFS-based, using in-degree counts) or **DFS-based** (post-order, then reverse) |
| Complexity | O(V + E) for either approach |

## Core Intuition
A topological sort answers: "if some tasks must happen before others, what's a valid order to do them all?" A node can only be placed in the ordering once **all of its prerequisites (incoming edges) have already been placed**. Kahn's algorithm formalizes this directly: repeatedly pick nodes with **zero remaining prerequisites** (in-degree 0), "complete" them, and decrement the in-degree of their dependents.

```
Courses: 0 depends on 1, 1 depends on 2  (edges: 2→1, 1→0)

in-degree: node 0 = 1, node 1 = 1, node 2 = 0

Kahn's: start with node 2 (in-degree 0) → process it → decrement node 1's in-degree to 0
        → process node 1 → decrement node 0's in-degree to 0 → process node 0

Valid order: [2, 1, 0]
```

## Worked Pattern: Kahn's Algorithm (BFS-based)
```python
from collections import deque, defaultdict

def topologicalSort(n, edges):
    graph = defaultdict(list)
    in_degree = [0] * n
    for u, v in edges:            # edge u -> v means u must come before v
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([node for node in range(n) if in_degree[node] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == n else []   # empty list = cycle detected, no valid ordering
```
**Key idea — cycle detection is a side effect:** if the graph has a cycle, at least one node's in-degree will **never** reach 0 (since it's waiting on a prerequisite that's waiting on it), so it never enters the queue. Checking `len(order) == n` at the end tells you whether every node was successfully ordered — if not, a cycle exists.

## Worked Pattern: DFS-based Topological Sort
```python
def topologicalSort_dfs(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    visited = set()
    result = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        result.append(node)          # add AFTER exploring all descendants (post-order)

    for node in range(n):
        if node not in visited:
            dfs(node)

    return result[::-1]              # reverse the post-order to get topological order
```
**Key idea — why reverse post-order works:** a node is only appended to `result` **after** all of its dependents (things it points to) have been fully explored — meaning it's always added *after* everything that must come after it. Reversing this post-order puts prerequisites before their dependents, producing a valid topological order.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "course schedule / prerequisites — can all courses be finished?" | Kahn's algorithm — if `len(order) < n`, a cycle exists, so it's impossible |
| "find a valid order to complete all courses/tasks" | Either Kahn's or DFS-based topological sort |
| "detect a cycle in a directed graph" | Topological sort as a cycle-detection tool (Kahn's: not all nodes get ordered; DFS: track an "in current recursion path" set to catch back-edges) |
| "alien dictionary" (derive character ordering from sorted word list) | Build edges from adjacent word comparisons, then topological sort the resulting character graph |
| "build order / task scheduling with dependencies" | Direct topological sort application |

## Common Pitfalls
- Forgetting that topological sort **only applies to DAGs** — running it on a graph with a cycle won't crash, but it will silently produce an incomplete ordering (Kahn's) or an incorrect one (naive DFS without cycle tracking) unless you explicitly check for it.
- In the DFS-based approach, forgetting to **reverse** the final result — the raw post-order list is the *reverse* of a valid topological order, not the order itself.
- In Kahn's algorithm, forgetting to check `len(order) == n` — this check is the only signal that a cycle was present and not all nodes could be ordered.
- For "detect a cycle" variants using plain DFS (not the post-order-and-reverse version above), forgetting to track nodes in the **current recursion path** separately from all-time visited nodes — a node visited via a different branch isn't necessarily part of a cycle; only a node revisited **within the same active DFS path** indicates one.

## Interview Talking Points
- If asked "how do you know a valid ordering exists at all," connect it directly to cycle detection: "a topological order exists if and only if the graph has no cycles — I can detect this as a side effect of running Kahn's algorithm."
- Be ready to justify why reversing DFS post-order produces a valid topological order — a common "explain it, don't just recite it" follow-up.

---

## 📋 Quick Cross-Algorithm Revision Table

| Question to Ask Yourself | If Yes → |
|---|---|
| Need shortest path from one source, weighted, non-negative edges? | Dijkstra's |
| Need to connect all nodes with minimum total edge cost (MST)? | Prim's (dense graph) or Kruskal's (sparse graph) |
| Need to check if two nodes are already connected, or detect a cycle, repeatedly as edges are added? | Union-Find (standalone, or as part of Kruskal's) |
| Need a valid ordering respecting "X before Y" dependencies? | Topological Sort (Kahn's or DFS-based) |
| All edge weights equal (or no weights at all)? | Plain BFS is enough — none of Dijkstra's/Prim's/Kruskal's overhead needed |
| Graph might contain a cycle, but the problem assumes a DAG? | Verify via topological sort — incomplete/invalid result signals a cycle |

## Suggested Problem Set for This Section
- **Dijkstra's:** Network Delay Time, Path with Minimum Effort, Cheapest Flights Within K Stops
- **Prim's / Kruskal's / Union-Find:** Min Cost to Connect All Points, Connecting Cities With Minimum Cost, Number of Connected Components in an Undirected Graph, Redundant Connection, Accounts Merge, Graph Valid Tree
- **Topological Sort:** Course Schedule, Course Schedule II, Alien Dictionary
