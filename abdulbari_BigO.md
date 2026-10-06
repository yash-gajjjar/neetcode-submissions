# Big-O & Time / Space Complexity — PBC Interview Notes

> **Goal:** Keep only the Big-O knowledge that is useful for PBC / top product-company coding interviews.
>
> **Study strategy:** NeetCode's Big-O cheatsheet is the fast reference. This file is the **reasoning + interview application layer**: how to derive complexity from code, recognize patterns, analyze space, and explain the answer clearly.

---

# 1. What Big-O Analysis Means

Big-O analysis asks:

> **How does the amount of work or memory grow as the input size n grows?**

We do not care about exact seconds for algorithmic interviews. We care about the **growth rate**.

Example:

~~~
2n + 10      → O(n)
5n² + 3n + 7 → O(n²)
~~~

Why?

- Constant factors do not change the growth class.
- Lower-order terms become insignificant for large n.
- The fastest-growing term dominates.

---

# 2. Time vs Space Complexity

## Time Complexity

How the number of operations grows with input size.

~~~
One loop over n elements → O(n)
Two nested loops          → O(n²)
Repeated doubling         → O(log n)
~~~

## Space Complexity

How much memory the algorithm uses as input grows.

Focus on **extra / auxiliary memory** unless the interviewer explicitly asks for total memory including the input.

~~~
Few fixed variables → O(1)
Array of n          → O(n)
n × n matrix        → O(n²)
~~~

### Important interview distinction

If an input array of size n is passed into a function, that input already occupies O(n) space. Usually, when people say **auxiliary space**, they mean the **additional memory created by the algorithm**.

---

# 3. Complexity Classes to Know

Use NeetCode's cheat sheet for quick recall. For interviews, recognize these immediately:

~~~
O(1)        Constant
O(log n)    Logarithmic
O(√n)       Square-root
O(n)        Linear
O(n log n)  Linearithmic
O(n·m)      Bilinear / two independent dimensions
O(n²)       Quadratic
O(n³)       Cubic
O(2ⁿ)       Exponential
O(n!)       Factorial
~~~

Typical growth order:

~~~
O(1)
  < O(log n)
  < O(√n)
  < O(n)
  < O(n log n)
  < O(n²)
  < O(n³)
  < O(2ⁿ)
  < O(n!)
~~~

> Do not spend revision time memorizing many obscure growth classes. The important skill is **recognizing the pattern from code**.

---

# 4. The Four Core Rules

## Rule 1 — Ignore Constant Factors

~~~
O(2n)   → O(n)
O(10n²) → O(n²)
~~~

## Rule 2 — Keep the Dominant Term

~~~
O(n² + n + 10) → O(n²)
~~~

## Rule 3 — Sequential Blocks Add

~~~
Block A → O(n)
Block B → O(n²)

Total = O(n + n²)
      = O(n²)
~~~

## Rule 4 — Nested Work Multiplies

~~~
n iterations × n iterations
→ O(n²)

n iterations × log n iterations
→ O(n log n)
~~~

### Memory trick

~~~
Sequential → ADD
Nested     → MULTIPLY
Then       → KEEP THE DOMINANT TERM
~~~

---

# 5. How to Analyze Any Code in an Interview

Use this exact sequence:

~~~
1. Identify the input size(s)
        ↓
2. Find loops / recursion
        ↓
3. Determine how many times each important operation runs
        ↓
4. Combine sequential or nested work
        ↓
5. Drop constants + lower-order terms
        ↓
6. Analyze auxiliary space separately
        ↓
7. Consider best / average / worst case when relevant
~~~

### Example

~~~python
for i in range(n):
    for j in range(n):
        process(i, j)
~~~

Outer loop → n

Inner loop → n for every outer iteration

Therefore:

~~~
n × n = O(n²)
~~~

---

# 6. Loop Patterns You Must Recognize

## i++, i--, or i += k

~~~python
i = 0
while i < n:
    i += 1
~~~

or:

~~~
i += 2
i += 5
i -= 3
~~~

The loop still performs a constant amount of progress each iteration.

~~~
O(n)
~~~

### Key idea

n/2, n/5, etc. are still O(n).

---

## Multiplication / Division by a Constant

~~~python
i = 1
while i < n:
    i *= 2
~~~

Values:

~~~
1, 2, 4, 8, 16, ...
~~~

After k iterations:

~~~
2^k ≈ n
k ≈ log₂ n
~~~

Therefore:

~~~
O(log n)
~~~

Same idea for:

~~~
i *= 3
i *= k
i /= 2
i /= k
~~~

when k > 1 is a constant.

### Memory trick

> **Multiplying or dividing the loop variable by a constant usually means O(log n).**

---

# 7. Nested Loops

## Same-size nested loops

~~~python
for i in range(n):
    for j in range(n):
        work()
~~~

~~~
n × n = O(n²)
~~~

Three nested loops:

~~~
n × n × n = O(n³)
~~~

---

## Different-size nested loops

~~~python
for i in range(n):
    j = 1
    while j < n:
        j *= 2
~~~

Outer → O(n)

Inner → O(log n)

Total:

~~~
O(n log n)
~~~

---

# 8. Sequential Loops

Two separate loops are usually **added**, not multiplied.

~~~python
for i in range(n):
    work()

for j in range(n):
    work()
~~~

~~~
O(n) + O(n)
= O(2n)
= O(n)
~~~

Even though there are two loops, they are not nested.

---

# 9. Summation Pattern

Consider:

~~~python
for i in range(n):
    for j in range(i):
        work()
~~~

The inner work is:

~~~
0 + 1 + 2 + ... + (n-1)
~~~

Using:

~~~
n(n-1)/2
~~~

we get:

~~~
O(n²)
~~~

### Pattern to remember

~~~
1 + 2 + 3 + ... + n
→ O(n²)
~~~

This pattern appears often in nested-loop interview questions.

---

# 10. Recognizing O(√n)

A common pattern occurs when the loop variable grows through a square relationship.

Example:

~~~text
k = 1
i = 1

while k < n:
    k = k + i
    i += 1
~~~

After m iterations:

~~~
k ≈ 1 + 2 + 3 + ... + m
  ≈ m² / 2
~~~

To reach n:

~~~
m² ≈ n
m ≈ √n
~~~

Therefore:

~~~
O(√n)
~~~

> You do not need to memorize many square-root examples. Learn to identify when the loop variable grows quadratically.

---

# 11. O(log log n) — Optional

O(log log n) exists and can appear in advanced algorithm-analysis questions, but it has **low practical ROI** for your main PBC revision.

Know that it is smaller than O(log n).

Do not spend significant study time memorizing obscure loop constructions just to produce O(log log n).

---

# 12. for vs while Does Not Determine Complexity

The loop keyword itself is irrelevant.

What matters is **how the loop variable changes**.

~~~
for + i++       → O(n)
while + i++     → O(n)

for + i*=2      → O(log n)
while + i*=2    → O(log n)
~~~

> Analyze the growth of the state, not the syntax.

---

# 13. Recursion — Interview-Level Rule

For recursive code, ask two questions:

1. **How many recursive calls are made at each level?**
2. **How many levels of recursion are there?**

Examples:

### One recursive call, input decreases by 1

~~~
T(n) = T(n-1) + O(1)
→ O(n)
~~~

### One recursive call, input halves

~~~
T(n) = T(n/2) + O(1)
→ O(log n)
~~~

### Two recursive calls on roughly half the input

~~~
T(n) = 2T(n/2) + O(n)
→ O(n log n)
~~~

### Branching recursion such as naive Fibonacci

~~~
T(n) = T(n-1) + T(n-2) + O(1)
→ exponential
~~~

For PBC coding interviews, recursion complexity should be understood alongside the recurrence / recursion-tree pattern rather than memorized as isolated formulas.

---

# 14. O, Ω, and Θ

These are **asymptotic bounds**, not best/average/worst-case labels.

## Big-O

Asymptotic upper bound.

~~~
f(n) = O(g(n))
~~~

Think:

> f(n) does not grow faster than the reference growth rate, up to constant factors, for sufficiently large n.

## Big-Omega

Asymptotic lower bound.

~~~
f(n) = Ω(g(n))
~~~

Think:

> f(n) grows at least as fast as the reference rate, up to constant factors.

## Big-Theta

Asymptotically tight bound.

~~~
f(n) = Θ(g(n))
~~~

Think:

> f(n) grows at the same asymptotic rate as g(n).

### Example

~~~
f(n) = 2n² + 3n + 4

O(f) → O(n²)
Ω(f) → Ω(n²)
Θ(f) → Θ(n²)
~~~

### Important correction

> **Θ does NOT mean "average case."**
>
> Best / average / worst case are about different input scenarios.  
> O, Ω, and Θ describe asymptotic bounds.

---

# 15. Best, Average, and Worst Case

An algorithm can perform differently depending on the input.

## Example — Linear Search

Array:

~~~
[8, 12, 5, 9, 7, 4, 3]
~~~

### Best Case

Target is first element.

~~~
O(1)
~~~

### Worst Case

Target is last or absent.

~~~
O(n)
~~~

### Average Case

Roughly half the array is inspected on average for a successful search under the usual uniform-position assumption.

~~~
Θ(n)
~~~

### Cheat sheet

~~~
Linear Search

Best    → O(1)
Average → Θ(n)
Worst   → O(n)
~~~

---

# 16. Binary Search

Binary search repeatedly cuts the search space roughly in half.

~~~
n
n/2
n/4
n/8
...
~~~

Therefore:

~~~
O(log n)
~~~

Typical bounds:

~~~
Best case  → O(1)
Worst case → O(log n)
~~~

Binary search requires a suitable ordered/searchable structure, commonly a sorted array.

---

# 17. BST Search

For a Binary Search Tree, complexity depends on tree height h.

~~~
Search = O(h)
~~~

Therefore:

~~~
Balanced BST → O(log n)
Skewed BST   → O(n)
~~~

If the target is at the root:

~~~
O(1)
~~~

### Important interview framing

> **BST search is O(h), not automatically O(log n).**
>
> It becomes O(log n) when the tree height is logarithmic, such as in a balanced tree.

---

# 18. Matrix / 2D Data

For an n × n matrix:

### Traverse every cell

~~~
O(n²)
~~~

### Store an n × n matrix

~~~
O(n²)
~~~

### Three nested dimensions

~~~
O(n³)
~~~

For rectangular matrices with dimensions n × m, prefer:

~~~
O(nm)
~~~

instead of forcing everything into O(n²).

---

# 19. Space Complexity Patterns

## Fixed number of variables

~~~python
a = 10
b = 20
temp = 0
~~~

~~~
O(1)
~~~

## Array proportional to n

~~~
new_array[n]
~~~

~~~
O(n)
~~~

## Matrix

~~~
new_matrix[n][n]
~~~

~~~
O(n²)
~~~

## Recursion Stack

Recursive calls also consume stack space.

Example:

~~~
Depth n recursion → O(n) stack space
Depth log n recursion → O(log n) stack space
~~~

### Interview reminder

Always separate:

~~~
Input Space
+
Auxiliary Space
~~~

when the interviewer cares about memory usage.

---

# 20. Common Interview Traps

## Trap 1 — Two independent loops are not O(n²)

~~~python
for i in range(n):
    ...

for j in range(n):
    ...
~~~

Answer:

~~~
O(n)
~~~

not O(n²).

---

## Trap 2 — Nested loops do not always mean O(n²)

~~~python
for i in range(n):
    j = 1
    while j < n:
        j *= 2
~~~

Answer:

~~~
O(n log n)
~~~

You must analyze each loop.

---

## Trap 3 — i += 2 is still O(n)

~~~
n/2 iterations → O(n)
~~~

---

## Trap 4 — i *= 2 is O(log n)

~~~
1, 2, 4, 8, ...
~~~

---

## Trap 5 — BST is not always O(log n)

~~~
Balanced → O(log n)
Skewed   → O(n)
~~~

Think in terms of height.

---

## Trap 6 — Best case is not the same thing as Ω

Do not say:

~~~
Best case = Ω(...)
Worst case = O(...)
~~~

as a universal rule.

They describe different ideas:

~~~
Best / Average / Worst → input scenarios

O / Ω / Θ → asymptotic bounds
~~~

---

# 21. Practical Examples

## Example A

~~~python
for i in range(n):
    print(i)
~~~

Answer:

~~~
Time  → O(n)
Space → O(1)
~~~

---

## Example B

~~~python
for i in range(n):
    for j in range(n):
        print(i, j)
~~~

Answer:

~~~
Time  → O(n²)
Space → O(1)
~~~

---

## Example C

~~~python
i = 1
while i < n:
    i *= 2
~~~

Answer:

~~~
Time  → O(log n)
Space → O(1)
~~~

---

## Example D

~~~python
for i in range(n):
    j = 1
    while j < n:
        j *= 2
~~~

Answer:

~~~
Time  → O(n log n)
Space → O(1)
~~~

---

## Example E

~~~python
arr = [0] * n

for i in range(n):
    for j in range(n):
        work()
~~~

Answer:

~~~
Time  → O(n²)
Space → O(n)
~~~

The working loops are quadratic, while the extra array is linear.

---

# 22. Interview-Friendly Explanation Template

When an interviewer asks:

> "What is the time and space complexity?"

Answer in this structure:

~~~
"The outer loop runs n times.
For each outer iteration, the inner loop runs log n times.
Therefore the total time complexity is O(n log n).

The algorithm uses only a constant number of extra variables,
so the auxiliary space complexity is O(1)."
~~~

For a more complex problem:

~~~
"First, I identify the dominant operation.
Then I estimate how many times it executes as a function of n.
For nested work I multiply the costs; for sequential blocks I add them
and keep the dominant term. Finally I analyze the auxiliary memory."
~~~

---

# 23. High-Value Pattern Table

| Code / Pattern | Complexity |
|---|---:|
| Single statement | O(1) |
| i++ until n | O(n) |
| i += k for constant k | O(n) |
| i *= k, k > 1 constant | O(log n) |
| i /= k, k > 1 constant | O(log n) |
| Two sequential O(n) blocks | O(n) |
| Two nested O(n) loops | O(n²) |
| n × log n nested work | O(n log n) |
| 1 + 2 + ... + n | O(n²) |
| n × m matrix traversal | O(nm) |
| n × n matrix traversal | O(n²) |
| Balanced BST search | O(log n) |
| Skewed BST search | O(n) |
| Linear search — best | O(1) |
| Linear search — worst | O(n) |
| Binary search — worst | O(log n) |

---

# 24. Final Complexity Cheat Sheet

## Time

~~~
O(1)        Constant
O(log n)    Logarithmic
O(√n)       Square-root
O(n)        Linear
O(n log n)  Linearithmic
O(nm)       Bilinear
O(n²)       Quadratic
O(n³)       Cubic
O(2ⁿ)       Exponential
O(n!)       Factorial
~~~

## Space

~~~
Fixed extra variables → O(1)
Array of n            → O(n)
Matrix n × n          → O(n²)
Recursion depth n     → O(n)
Recursion depth log n → O(log n)
~~~

## Bounds

~~~
O     → Upper bound
Ω     → Lower bound
Θ     → Tight bound
~~~

## Cases

~~~
Best     → Minimum work for a valid input
Average  → Expected / average work under an input model
Worst    → Maximum work for a valid input
~~~

## Main rules

~~~
Sequential → ADD
Nested     → MULTIPLY
Constants  → IGNORE
Lower terms → DROP
Dominant term → KEEP
~~~

---

# 25. One-Page Mental Model

~~~
                 BIG-O INTERVIEW ANALYSIS
                           |
            +--------------+--------------+
            |                             |
          TIME                           SPACE
            |                             |
      Count operations             Count extra memory
            |                             |
      Analyze loop growth          O(1), O(n), O(n²)
            |
      +-----+------+
      |            |
    SEQUENTIAL    NESTED
      |            |
     ADD        MULTIPLY
      |            |
      +-----+------+
            |
       Simplify
            |
   Remove constants
   Drop lower terms
   Keep dominant term
            |
    Consider cases
            |
   Best / Average / Worst
~~~

---

# 26. What You Should Be Able to Do

Before considering Big-O complete for PBC preparation, you should be able to look at unfamiliar code and quickly answer:

### 1. What is the input size?

~~~
n, m, matrix dimensions, tree height, etc.
~~~

### 2. How many times does the important operation execute?

~~~
n
log n
√n
n²
n log n
...
~~~

### 3. Are operations sequential or nested?

~~~
Sequential → add
Nested     → multiply
~~~

### 4. What memory grows with input size?

~~~
Variables
Arrays
Maps/Sets
Matrices
Recursion stack
~~~

### 5. Does the answer depend on the input arrangement?

~~~
Best / Average / Worst
~~~

### 6. Can you explain the answer in one or two sentences?

That final communication step matters in interviews.

---

# 27. Topics Intentionally Removed from the Main PBC Notes

These topics were removed or heavily compressed because they have low practical ROI for your current interview goal:

- Algorithm-vs-program textbook definitions
- Formal characteristics of an algorithm
- A priori / a posteriori analysis in textbook detail
- N(I/O), power, CPU-register analysis
- Detailed frequency-count arithmetic such as exact 3n + 2 expressions
- Matrix frequency-count derivations
- Formal proofs of reflexive / transitive / symmetric asymptotic properties
- Detailed factorial bounds and log(n!)
- Long mathematical comparisons of exotic functions
- Piecewise asymptotic comparison exercises
- True/false asymptotic worksheets
- Obscure O(log log n) derivations

These are **not necessarily wrong or useless**. They are simply not worth occupying the primary revision document when your goal is PBC coding interviews.

---

# 28. Final Interview Mindset

> **Do not memorize hundreds of complexity formulas. Learn to read the code and derive the growth.**

The core mental process is:

~~~
Code
 ↓
Input size
 ↓
Loop / recursion growth
 ↓
Number of operations
 ↓
Sequential vs nested
 ↓
Simplify
 ↓
Time complexity
 ↓
Extra memory
 ↓
Space complexity
 ↓
Best / Average / Worst when relevant
~~~

### The real goal

You should be able to see:

~~~
i++      → linear
i *= 2   → logarithmic
nested n → quadratic
n + logn → linear
n × logn → linearithmic
sum 1..n → quadratic
balanced tree → logarithmic
~~~

and then explain **why**, not just state the answer.

---

## Final Takeaway

For your PBC preparation:

**NeetCode Big-O cheatsheet = fast memorization/reference**

**This file = reasoning, pattern recognition, interview explanation**

Do not repeatedly study both as full theory documents. Use the NeetCode sheet for quick recall and this file when you want to practice deriving complexity from actual code.
