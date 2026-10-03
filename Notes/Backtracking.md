# Backtracking — DSA Interview Notes
*Backtracking Fundamentals & Template · Core Patterns (Subsets/Permutations/Combinations) · Pruning & Constraint Satisfaction*

> **Note:** No sub-topics were given for this one, so it's split into the three groupings that cover what interviews actually test: the general template every backtracking solution follows, the handful of recurring enumeration patterns, and how pruning turns a brute-force search into something that actually finishes in time.

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the diagrams by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each section.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right pattern in <10 seconds.

All code examples in Python.

---

## 🔑 Cheat Sheet — All Three Sections at a Glance
| Section | Core Idea | Time (typical) | Space |
|---|---|---|---|
| Fundamentals & Template | Choose → Explore → Un-choose; build a solution incrementally, abandon paths early | Exponential in the worst case | O(depth) recursion stack |
| Core Patterns | A handful of reusable "shapes": subsets, permutations, combinations, combination sum | 2^n to n! depending on shape | O(n) per path, O(2^n)–O(n!) total output |
| Pruning & Constraints | Cut off invalid branches **before** fully exploring them — the difference between brute force and a solution that finishes | Same exponential worst case, but massively reduced in practice | O(depth) + O(constraint-check state) |

**Core shared idea:** backtracking is DFS over a **decision tree** where each node represents a partial solution. At every node, you try each available choice, recurse, then **undo** that choice before trying the next one — the "undo" step (backtracking) is what lets you reuse the same state/array across all branches instead of copying it.

---

# 1. Backtracking Fundamentals & Template

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| General template | `choose → recurse (explore) → un-choose (backtrack)` |
| Base case | When a complete/valid solution is formed — record it (usually a copy, since the list is reused) |
| Why "undo" matters | Reuses the same mutable state across all branches instead of allocating new copies — critical for both correctness and efficiency |
| Complexity mindset | Backtracking problems are inherently exponential — the real skill is minimizing wasted work via pruning (see §3), not avoiding exponential time entirely |

## Core Intuition
Backtracking explores a tree of decisions **depth-first**: make a choice, dive into the consequences of that choice, and if it doesn't pan out (or once you've explored it fully), **undo the choice** and try the next option at that same level. It's DFS, but on an implicit tree of "what could I choose next" rather than a literal data structure like a linked list or graph.

```
Decision tree for subsets of [1, 2]:

                    []
              /            \
          choose 1      don't choose 1
            [1]                []
           /    \              /    \
      choose 2  skip      choose 2  skip
       [1,2]    [1]         [2]      []
```
Each leaf (or every node, for subsets) represents a complete/partial solution to record.

## The Universal Template (Python)
```python
def backtrack(path, choices, result):
    if is_solution(path):           # base case: valid complete solution
        result.append(path[:])      # append a COPY — path will keep changing
        return                       # (or don't return, if partial paths are also valid answers)

    for choice in get_options(choices, path):
        if not is_valid(choice, path):   # pruning check (see §3)
            continue
        path.append(choice)              # CHOOSE
        backtrack(path, choices, result) # EXPLORE
        path.pop()                       # UN-CHOOSE (backtrack)
```
**Key idea — why `path[:]` (a copy) matters:** `path` is a single mutable list reused across the entire recursion. If you append the reference itself (`result.append(path)`) instead of a copy, every recorded "solution" ends up pointing to the *same* list — which gets mutated by later backtracking steps, silently corrupting all previously recorded answers. This is the single most common backtracking bug.

## Common Pitfalls
- Appending `path` instead of `path[:]` (or `list(path)`) to the result — causes all recorded solutions to alias the same mutable list.
- Forgetting the "un-choose" step (`path.pop()`) — leaves stale state polluting sibling branches.
- Not pruning early (checking validity **before** recursing rather than after) — wastes time fully exploring branches that were doomed from the start (see §3).
- Confusing backtracking with plain DFS on an explicit graph/tree — backtracking specifically involves **mutating and restoring shared state** as you explore a space of choices, not just visiting existing nodes.

## Interview Talking Points
- Always narrate the three-step rhythm explicitly ("I'll choose this element, recurse, then remove it before trying the next option") — this signals you understand the mechanism, not just the code shape.
- If asked for time complexity, be upfront that it's exponential (state the specific bound — 2^n for subsets, n! for permutations) and pivot the conversation toward what pruning does to the *practical* runtime.

---

# 2. Core Patterns — Subsets, Permutations, Combinations

## 🔑 Cheat Sheet
| Pattern | Output Size | Order Matters? | Reuse Elements? |
|---|---|---|---|
| Subsets | 2^n | No | No (each element used 0 or 1 times) |
| Permutations | n! | Yes | No (each element used exactly once, all orders count) |
| Combinations (choose k) | C(n, k) | No | No |
| Combination Sum (reuse allowed) | Varies | No | **Yes** — same element can be reused |

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "return all subsets/power set" | Subsets pattern — at each element, branch into include/exclude |
| "return all permutations" (order matters, e.g. [1,2] ≠ [2,1]) | Permutations pattern — track used elements, try every remaining one at each position |
| "return all combinations of size k" (order doesn't matter) | Combinations pattern — use a start index to avoid revisiting earlier elements |
| "combination sum" (numbers can repeat, order doesn't matter) | Combination Sum pattern — recurse without advancing past the current index when reuse is allowed |
| "letter combinations of a phone number" | Cartesian-product-style backtracking, one choice set per position |
| "partition a string into valid substrings" (e.g., palindrome partitioning) | Backtracking with a start index, trying every possible "next cut" |

## Worked Pattern: Subsets (include/exclude at each element)
```python
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])                 # every path is a valid subset — record at every node
        for i in range(start, len(nums)):
            path.append(nums[i])                # CHOOSE nums[i]
            backtrack(i + 1, path)               # EXPLORE — move past i, no reuse
            path.pop()                           # UN-CHOOSE
    backtrack(0, [])
    return result
```
**Complexity:** O(2^n) subsets, O(n) to copy each → O(n · 2^n) total.

## Worked Pattern: Permutations (track used elements, no start index)
```python
def permute(nums):
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue                          # pruning: skip already-used elements
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result
```
**Key difference from Subsets:** permutations don't use a `start` index — every unused element is a valid next choice regardless of position, since order matters and all `n` elements must eventually appear in every full path.
**Complexity:** O(n!) permutations, O(n) to build each → O(n · n!) total.

## Worked Pattern: Combination Sum (element reuse allowed)
```python
def combinationSum(candidates, target):
    result = []
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return                                # pruning: overshoot, no point continuing
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])   # note: i, NOT i+1 — allows reuse
            path.pop()
    backtrack(0, [], target)
    return result
```
**Key idea — `i` vs `i + 1`:** passing `i` (not `i + 1`) to the recursive call is what allows the **same element to be reused** in combination sum, while still using `start` to prevent revisiting *earlier* elements (which would produce duplicate combinations in a different order).

## Common Pitfalls
- Using a `start` index for permutations (wrong — permutations need to consider all unused elements at every position, not just "later" ones).
- Forgetting the `used[]` array (or equivalent) for permutations — without it, elements can be reused within a single permutation, producing invalid results.
- Off-by-one between `i` and `i + 1` when recursing — this single choice is the entire difference between "combinations without reuse" and "combinations with reuse" (Combination Sum).
- Not sorting the input first when duplicates need to be skipped (e.g., Subsets II, Combination Sum II, Permutations II) — duplicate skipping logic typically relies on adjacent equal elements being next to each other after sorting.

## Interview Talking Points
- When asked to solve a new backtracking problem, explicitly identify which "shape" it matches (subsets/permutations/combinations/combination-sum) before coding — this framing shows pattern recognition rather than deriving each solution from scratch.
- For "avoid duplicates in output" variants, mention the standard trick: sort first, then skip an element if it equals the previous element **at the same recursion depth** (not just anywhere in `path`).

---

# 3. Pruning & Constraint Satisfaction

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Pruning | Checking a partial solution's validity **before** fully building it out, so invalid branches are abandoned early instead of explored to completion |
| Constraint satisfaction problems (CSPs) | Problems with explicit placement rules (N-Queens, Sudoku) where pruning is essential — without it, the search space is far too large to finish in reasonable time |
| Effect of pruning | Doesn't change the worst-case big-O, but drastically reduces the *actual* number of nodes explored in practice |

## Core Intuition
Backtracking without pruning still eventually finds the right answer, but it wastes enormous amounts of time fully building out branches that were doomed from the very first invalid placement. Pruning means checking constraints **as early as possible** — ideally right when a choice is made, not after the entire path is built.

```
N-Queens (place queens so none attack each other):

Without pruning: try every possible placement of all n queens (n^n possibilities),
                  then check validity only at the end.

With pruning: check row/column/diagonal conflicts BEFORE placing each queen —
              an invalid placement is rejected immediately, cutting off
              an entire subtree of further-doomed placements.
```

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "place N queens on a board so none attack each other" | Backtracking + pruning on row/column/diagonal conflicts, placed one row at a time |
| "solve a Sudoku puzzle" | Backtracking + pruning on row/column/3×3-box constraints before placing each digit |
| "word search on a grid" | Backtracking + pruning via "already visited" marking and letter mismatch (ties back to Tries §2 when searching multiple words) |
| "generate valid parentheses" | Backtracking + pruning: only add `)` if it wouldn't exceed the number of `(` placed so far |
| "partition equal subset sum / target sum with constraints" | Backtracking + pruning on running sum exceeding target, often combined with memoization to avoid recomputation |

## Worked Pattern: N-Queens (pruning via conflict tracking)
```python
def solveNQueens(n):
    result = []
    cols = set()
    diagonals = set()      # r - c is constant along a "\" diagonal
    anti_diagonals = set()  # r + c is constant along a "/" diagonal
    board = [["."] * n for _ in range(n)]

    def backtrack(row):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diagonals or (row + col) in anti_diagonals:
                continue                              # PRUNE: conflict detected, skip immediately

            cols.add(col)
            diagonals.add(row - col)
            anti_diagonals.add(row + col)
            board[row][col] = "Q"

            backtrack(row + 1)

            cols.remove(col)                          # UN-CHOOSE
            diagonals.remove(row - col)
            anti_diagonals.remove(row + col)
            board[row][col] = "."

    backtrack(0)
    return result
```
**Key idea:** tracking conflicts with **sets** (`cols`, `diagonals`, `anti_diagonals`) gives O(1) conflict checks instead of re-scanning the whole board for every candidate placement — this is the pruning that makes N-Queens tractable for reasonably sized `n`.

## Worked Pattern: Generate Parentheses (pruning invalid states early)
```python
def generateParenthesis(n):
    result = []
    def backtrack(path, open_count, close_count):
        if len(path) == 2 * n:
            result.append("".join(path))
            return
        if open_count < n:
            path.append("(")
            backtrack(path, open_count + 1, close_count)
            path.pop()
        if close_count < open_count:                  # PRUNE: never let close exceed open
            path.append(")")
            backtrack(path, open_count, close_count + 1)
            path.pop()
    backtrack([], 0, 0)
    return result
```
**Key idea:** the condition `close_count < open_count` prunes every invalid path (where parentheses would go negative/unbalanced) **the instant** it would become invalid, rather than generating all 2^(2n) strings and filtering afterward.

## Common Pitfalls
- Checking constraints only at the base case (fully built solution) instead of at each choice — this is technically correct but far slower, since invalid branches are still fully explored before being discarded.
- For N-Queens/Sudoku: re-scanning the whole board on every placement instead of maintaining O(1)-checkable state (sets for columns/diagonals, or row/col/box bitmasks for Sudoku) — a strong candidate optimizes this proactively.
- Forgetting to undo pruning-related state (e.g., removing from `cols`/`diagonals` sets) alongside undoing the path — partial cleanup corrupts sibling branches just like forgetting `path.pop()`.
- Treating pruning as changing the **worst-case** complexity — it doesn't (still exponential in the worst case); it reduces the *practical* number of nodes explored, which is worth stating precisely rather than overclaiming.

## Interview Talking Points
- Whenever you write a backtracking solution, proactively mention where pruning applies — even a brute-force-shaped answer becomes noticeably stronger once you add "and I'd prune here by checking X before recursing further."
- For constraint satisfaction problems (N-Queens, Sudoku), be ready to discuss maintaining O(1)-checkable conflict state (sets/bitmasks) as the key optimization over naive re-validation.

---

## 📋 Quick Cross-Section Revision Table

| Question to Ask Yourself | If Yes → |
|---|---|
| Does order matter in the output (e.g., [1,2] ≠ [2,1])? | Permutations pattern (no start index, track used elements) |
| Does order NOT matter, and each element used at most once? | Combinations/Subsets pattern (use a start index) |
| Can the same element be reused multiple times? | Combination Sum pattern (recurse with `i`, not `i + 1`) |
| Are there explicit placement constraints (rows/cols/diagonals/boxes)? | Constraint satisfaction — track conflict state for O(1) pruning checks |
| Can I check partial validity before the solution is fully built? | Prune there — don't wait until the base case to validate |
| Do I need to avoid duplicate outputs from duplicate input elements? | Sort first, skip equal elements at the same recursion depth |

## Suggested Problem Set for This Section
- **Fundamentals/Subsets/Permutations/Combinations:** Subsets, Subsets II, Permutations, Permutations II, Combinations, Combination Sum, Combination Sum II
- **Pruning/Constraint Satisfaction:** N-Queens, Sudoku Solver, Generate Parentheses, Word Search, Palindrome Partitioning, Letter Combinations of a Phone Number

---
*Format matches your Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, and Tries notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*
