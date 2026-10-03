# Stack — DSA Interview Notes
*NeetCode 150 | Core Stack Operations · Monotonic Stack*

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the diagrams by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each method.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right variant in <10 seconds.

---

## 🔑 Cheat Sheet — Both Methods at a Glance
| Method | Core Idea | Typical Use | Time | Space |
|---|---|---|---|---|
| Core Stack | LIFO (last in, first out) — push/pop/peek | Matching, undo, nested structure, DFS iterative | O(1) per op | O(n) |
| Monotonic Stack | Stack kept strictly increasing or decreasing; pop elements that violate order before pushing | "next greater/smaller element", span problems | O(n) total | O(n) |

**Core shared idea:** a stack remembers "what's still relevant/unresolved" in the order you'd need to resolve it — the most recent unresolved thing is always on top, ready to be matched, closed, or compared against next.

---

# 1. Core Stack

## 🔑 Cheat Sheet
| Operation | Complexity |
|---|---|
| Push | O(1) |
| Pop | O(1) |
| Peek/Top | O(1) |
| Search (is X in stack) | O(n) |
| Python implementation | `list` (`append`/`pop` from the end — both O(1) amortized) |

## Core Intuition
A stack is **LIFO**: the last thing pushed is the first thing popped. This maps naturally onto any problem with **nested structure** or where you need to "undo"/"match" the most recent unresolved item — parentheses, function call order, backtracking, browser back-button history.

```
push(1) → [1]
push(2) → [1,2]
push(3) → [1,2,3]
pop()   → returns 3 → [1,2]
pop()   → returns 2 → [1]
```

### Why Stacks Are the Right Tool for Nesting
Nested structures resolve **innermost-first**: in `"([{}])"`, the innermost `{}` must close before the `[]` around it, which must close before the outer `()`. A stack's LIFO order mirrors this exactly — push on "open", pop-and-check on "close".

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "valid parentheses / matching brackets" | Push opening brackets; on closing bracket, pop and check it matches |
| "evaluate expression (RPN, calculator)" | Push operands; on operator, pop two, compute, push result |
| "simplify path / undo operations" | Push valid path segments; pop on `".."` |
| "implement queue using stacks" or "min stack" | Two stacks working together, or auxiliary stack tracking extra state |
| "generate all valid combinations (parentheses, backtracking)" | Stack-based DFS / explicit stack instead of recursion |
| "evaluate nested/recursive structure without recursion" | Explicit stack to simulate the call stack (iterative DFS/tree traversal) |

## Worked Pattern: Valid Parentheses
```python
def isValid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c in pairs:
            if not stack or stack[-1] != pairs[c]:
                return False
            stack.pop()
        else:
            stack.append(c)
    return not stack  # must be fully closed
```
**Complexity:** O(n) time, O(n) space.

## Worked Pattern: Min Stack (auxiliary stack tracks running min)
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # min_stack[i] = min of stack[0..i]

    def push(self, val):
        self.stack.append(val)
        curr_min = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(curr_min)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]  # O(1), no rescanning needed
```
**Key idea:** don't recompute the min on every `getMin()` call (that'd be O(n)) — maintain a parallel stack that tracks the running min at each push, so `getMin()` is O(1).

## Common Pitfalls
- Popping from an empty stack — always check `if not stack` / `if stack` before popping or peeking.
- Forgetting to check the stack is **fully empty** at the end for matching problems (e.g., `"((("` has no closing brackets but never triggers a mismatch — must check leftover unmatched opens).
- For Min Stack: recomputing min from scratch instead of maintaining the auxiliary stack — defeats the O(1) requirement.
- Using recursion where an explicit stack was the point of the question (some interviewers specifically want iterative solutions to demonstrate you understand what recursion does under the hood).

## Interview Talking Points
- "Implement a queue using two stacks" is a classic — know the two-stack amortized O(1) approach (one stack for enqueue, reverse into a second stack for dequeue only when it's empty).
- Be ready to connect stacks to recursion: **the call stack itself is a stack** — any recursive solution can, in principle, be rewritten iteratively with an explicit stack.

---

# 2. Monotonic Stack

## 🔑 Cheat Sheet
| Aspect | Detail |
|---|---|
| Definition | A stack maintained in **strictly increasing** or **strictly decreasing** order (top to bottom or bottom to top, depending on convention) |
| Core operation | Before pushing a new element, **pop** everything that violates the monotonic order — those popped elements just found their "answer" |
| Complexity | O(n) total — despite nested-looking loop, each element is pushed once and popped once |
| Typical use | "next greater/smaller element", "daily temperatures", span/width problems, largest rectangle in histogram |

## Core Intuition
For "next greater element" style problems, brute force checks every element against every element to its right — O(n²). A **monotonic decreasing stack** (values decrease from bottom to top) fixes this: when a new element is larger than the stack's top, that top element has just found its "next greater element" — pop it, record the answer, and repeat until the stack is valid again, then push the new element.

```
nums = [2, 1, 2, 4, 3]     find "next greater element" for each

i=0, val=2: stack empty → push → stack=[2](idx0)
i=1, val=1: 1 < top(2) → push → stack=[2,1](idx0,1)
i=2, val=2: 2 > top(1) → pop idx1, answer[1] = 2 (current val)
            2 == top(2)? not strictly greater than idx0's 2 → push
            stack=[2,2](idx0,2)
i=3, val=4: 4 > top(2) → pop idx2, answer[2] = 4
            4 > top(2) → pop idx0, answer[0] = 4
            stack empty → push → stack=[4](idx3)
i=4, val=3: 3 < top(4) → push → stack=[4,3](idx3,4)

end: anything left in stack has no next greater element → answer = -1
answer = [4, 2, 4, -1, -1]
```

### Why It's O(n), Not O(n²)
The nested `while` loop (popping) looks expensive, but **each element is pushed exactly once and popped at most once** across the entire run. Total pushes + pops ≤ 2n → O(n) overall. This is the same amortized argument as sliding window's "left only moves forward" and dynamic array doubling — a recurring theme across topics, worth stating explicitly in interviews.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "next greater element" (to the right) | Monotonic decreasing stack, scan left to right |
| "next smaller element" | Monotonic increasing stack, scan left to right |
| "previous greater/smaller element" | Same idea, scan right to left, or maintain stack while scanning left to right and check on the way |
| "daily temperatures" (days until warmer temp) | Monotonic decreasing stack of indices; on pop, compute `curr_index - popped_index` |
| "largest rectangle in histogram" | Monotonic increasing stack of indices; on pop, popped bar's height × width (computed from stack boundaries) is a candidate max area |
| "trapping rain water" (stack-based approach) | Monotonic decreasing stack; on pop, compute trapped water bounded by current bar and new stack top |
| "stock span problem" (consecutive days price ≤ today) | Monotonic decreasing stack of (price, span), accumulate span on pop |
| "remove K digits to form smallest number" | Monotonic increasing stack; pop larger digits when a smaller one arrives, greedily |

## Worked Pattern: Daily Temperatures
```python
def dailyTemperatures(temperatures):
    res = [0] * len(temperatures)
    stack = []  # stores indices, temperatures decreasing bottom to top

    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_idx = stack.pop()
            res[prev_idx] = i - prev_idx
        stack.append(i)

    return res
```
**Complexity:** O(n) time, O(n) space — each index pushed once, popped once.

## Common Pitfalls
- Storing **values** instead of **indices** on the stack — most problems need the index to compute distance/span/width once a match is found (e.g., Daily Temperatures, Largest Rectangle in Histogram).
- Using `<` vs `<=` incorrectly — decide up front whether equal elements should trigger a pop (affects strictly increasing vs non-decreasing behavior) and match it to the problem's exact requirement.
- Forgetting elements left in the stack at the end have **no answer found** — typically default to `-1` or `0` depending on the problem.
- Applying monotonic stack when the problem doesn't actually have a "next/previous greater/smaller" shape — it's a specific pattern, not a universal stack upgrade.

## Interview Talking Points
- Immediately flag it as **monotonic stack** when you see "next greater/smaller element" phrasing — this is one of the most recognizable signal-to-pattern mappings in DSA interviews, and naming it early signals pattern fluency.
- Be ready to explain the O(n) amortized argument (each element pushed/popped once) without hand-waving — interviewers often ask "isn't this O(n²) because of the nested loop?"

---

## 📋 Quick Cross-Method Revision Table

| Question to Ask Yourself | If Yes → | If No → |
|---|---|---|
| Does the problem involve matching/nesting (brackets, undo, nested calls)? | Core Stack (LIFO push/pop/match) | — |
| Do I need O(1) access to a running min/max alongside stack operations? | Core Stack + auxiliary stack (Min Stack pattern) | — |
| Does the problem ask for "next/previous greater/smaller element" for every index? | Monotonic Stack | — |
| Am I computing spans, widths, or areas bounded by comparative order (histogram, trapping water)? | Monotonic Stack (store indices) | — |
| Could this be solved recursively but the question wants an iterative approach? | Core Stack simulating the call stack | — |

## Suggested NeetCode 150 Problem Set for This Section
- **Core Stack:** Valid Parentheses, Min Stack, Evaluate Reverse Polish Notation, Generate Parentheses, Daily Temperatures (bridge problem), Car Fleet
- **Monotonic Stack:** Daily Temperatures, Largest Rectangle in Histogram

---
*Format matches your Arrays & Hashing, Two Pointers, and Sliding Window notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*
