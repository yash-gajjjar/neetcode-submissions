# Time & Space Complexity 

---

# 1. Introduction to Algorithms

## Algorithm vs Program

The first important distinction is:

| Algorithm                        | Program                                  |
| -------------------------------- | ---------------------------------------- |
| Design / solution approach       | Implementation of the solution           |
| Domain knowledge is important    | Programming language is important        |
| Language independent             | Language dependent                       |
| Hardware independent             | Hardware dependent                       |
| Analyze time & space             | Actual execution can be tested           |
| Focuses on **what/how to solve** | Focuses on **implementing the solution** |

### Simple understanding

Suppose you want to swap two numbers.

**Algorithm:**

```text
temp = a
a = b
b = temp
```

This describes the solution independently of Python, Java, C++, etc.

**Program:**

```python
temp = a
a = b
b = temp
```

The program is the actual implementation in a particular programming language.

The key idea:

> **Algorithm = design of the solution**
> **Program = implementation of that solution**

---

# 2. Characteristics of an Algorithm

An algorithm should have the following characteristics:

1. **Input**

   * An algorithm can have **0 or more inputs**.

2. **Output**

   * It should produce **at least one output**.

3. **Definiteness**

   * Every step should be clearly and unambiguously defined.

4. **Finiteness**

   * The algorithm must eventually terminate.

5. **Effectiveness**

   * The operations should be basic/practical enough to actually execute.

### Easy way to remember

```text
Input
  ↓
Clearly defined steps
  ↓
Finite execution
  ↓
Output
```

These five characteristics are explicitly listed in the source. 

---

# 3. A Priori vs A Posteriori Analysis

There are two ways to analyze an algorithm/program.

## A Priori Analysis

This is done **before running the program**.

Characteristics:

* Works with the **algorithm**
* Independent of programming language
* Hardware independent
* Analyzes:

  * Time
  * Space
  * Functions used

So:

```text
Algorithm
   ↓
A Priori Analysis
   ↓
Time + Space
```

## A Posteriori Analysis

This is done **after implementing/running the program**.

Characteristics:

* Works with the actual **program**
* Language dependent
* Hardware dependent
* Measures things such as:

  * Actual execution time
  * Bytes/memory used

### Interview shortcut

> **A Priori → Analyze algorithm theoretically**
> **A Posteriori → Run the program and measure it**

This distinction is shown on page 3 of your PDF. 

---

# 4. How to Write an Algorithm

The source demonstrates a simple swapping algorithm.

```text
Algorithm Swap(a, b)

begin
    temp = a
    a = b
    b = temp
end
```

The important point is that an algorithm is written as a sequence of logical steps rather than being tied to a particular programming language.



---

# 5. How to Analyze an Algorithm

The source lists the following aspects:

1. **Time**
2. **Space**
3. **N(I/O)**
4. **Power**
5. **CPU Registers**

For DSA interview preparation, the major focus of these notes is **Time Complexity and Space Complexity**. 

---

# 6. Space Complexity

Space complexity represents the amount of memory required by an algorithm.

For example:

```text
temp = a
a = b
b = temp
```

The algorithm uses variables such as:

```text
a
b
temp
```

So the number of additional variables remains constant regardless of input size.

Therefore:

```text
S(n) = O(1)
```

### Important idea

If the amount of extra memory does **not grow with `n`**, the auxiliary space is:

```text
O(1)
```

The swap example in the source concludes constant space. 

---

# 7. Frequency Count Method

One of the most important techniques in these notes is the **Frequency Count Method**.

The basic idea is:

> Count how many times each important statement executes.

Instead of measuring actual seconds, count the number of operations as a function of input size `n`.

---

## Example 1: Sum of Array Elements

Consider:

```text
Algorithm Sum(A, n)

s = 0

for(i = 0; i < n; i++)
    s = s + A[i]

return s
```

### Frequency count

```text
s = 0                  → 1
loop condition         → n + 1
s = s + A[i]           → n
return s               → 1
```

Therefore:

```text
f(n) = 1 + (n + 1) + n + 1
```

Ignoring constants and lower-order terms:

```text
f(n) = O(n)
```

### Space

Variables:

```text
A → n
n → 1
s → 1
i → 1
```

If the input array itself is included:

```text
S(n) = O(n)
```

The source illustrates this frequency-count approach using the array-sum example. 

---

# 8. Matrix Addition

Consider two `n × n` matrices:

```text
A
B
C
```

The algorithm is conceptually:

```text
for(i = 0; i < n; i++)
{
    for(j = 0; j < n; j++)
    {
        C[i][j] = A[i][j] + B[i][j]
    }
}
```

## Frequency Count

Outer loop:

```text
n + 1
```

Inner loop executes approximately:

```text
n × (n + 1)
```

Main operation:

```text
n × n = n²
```

So:

```text
f(n) = 2n² + 2n + 1
```

Therefore:

```text
Time Complexity = O(n²)
```

## Space

The matrices themselves contain:

```text
A → n²
B → n²
C → n²
```

Therefore:

```text
S(n) = O(n²)
```

The matrix-addition example appears across pages 8–9. 

---

# 9. Matrix Multiplication

For multiplying two `n × n` matrices:

```text
A × B = C
```

The algorithm contains **three nested loops**:

```text
for(i = 0; i < n; i++)
    for(j = 0; j < n; j++)
        for(k = 0; k < n; k++)
            C[i][j] = C[i][j] + A[i][k] * B[k][j]
```

Each loop contributes approximately `n`.

Therefore:

```text
n × n × n = n³
```

Hence:

```text
Time Complexity = O(n³)
```

Space shown in the source is:

```text
S(n) = O(n²)
```

The source explicitly analyzes matrix multiplication as cubic time and quadratic space. 

---

# 10. Basic Rules for Calculating Time Complexity

When analyzing loops, focus on **how many times the body executes**.

---

## Example 1 — Increment by 2

```text
for(i = 1; i < n; i = i + 2)
    stmt
```

Values of `i`:

```text
1, 3, 5, 7, ...
```

Approximately:

```text
n / 2
```

iterations.

Therefore:

```text
O(n)
```

### Key point

Even though the loop runs only `n/2` times:

```text
O(n/2) = O(n)
```

Constants are ignored.



---

# 11. Nested Loops

Consider:

```text
for(i = 0; i < n; i++)
    for(j = 0; j < i; j++)
        stmt
```

The inner loop executes:

```text
0 + 1 + 2 + 3 + ... + (n - 1)
```

Using the sum formula:

```text
n(n - 1) / 2
```

Therefore:

```text
O(n²)
```

### Important pattern

Whenever you see:

```text
0 + 1 + 2 + ... + n
```

think:

```text
O(n²)
```

The source demonstrates this through the nested-loop example. 

---

# 12. Loop Where the Work Depends on `i`

Example:

```text
p = 0

for(i = 1; i <= n; i++)
    p = p + i
```

The source uses the summation:

```text
1 + 2 + 3 + ... + k
```

and determines how many iterations are required.

This leads to a square-root relationship in the analyzed condition, giving:

```text
O(√n)
```

The key lesson is:

> Don't automatically assume every loop that increments by `1` is `O(n)`. Analyze the **condition and the amount of work** carefully.



---

# 13. Multiplication in the Loop

Consider:

```text
for(i = 1; i <= n; i = i * 2)
    stmt
```

Values of `i`:

```text
1
2
4
8
16
...
```

After `k` iterations:

```text
i = 2^k
```

The loop stops when:

```text
2^k >= n
```

Therefore:

```text
k = log₂ n
```

So:

```text
Time Complexity = O(log₂ n)
```

### Memory trick

Whenever you see:

```text
i = i * 2
i = i * 3
i = i * k
```

think:

```text
O(log n)
```

The base of the logarithm usually doesn't matter for Big-O.



---

# 14. Division in the Loop

The same principle works in reverse.

For example:

```text
for(i = n; i > 1; i = i / 2)
    stmt
```

The value repeatedly becomes:

```text
n
n/2
n/4
n/8
...
```

Again, the number of iterations is logarithmic:

```text
O(log₂ n)
```

So:

```text
multiply/divide by constant
        ↓
logarithmic complexity
```

The source discusses these logarithmic loop patterns and explicitly shows different logarithm bases. 

---

# 15. `O(log log n)`

The source gives an example where one logarithmic loop is nested inside another.

Conceptually:

```text
for(i = 1; i < n; i = i * 2)
{
    for(j = 1; j < i; j = j * 2)
        stmt;
}
```

The source concludes:

```text
O(log log n)
```

for its specific analyzed structure.

### Important takeaway

There are multiple levels of logarithmic growth:

```text
log n
log log n
```

and they are significantly smaller than linear growth.



---

# 16. Nested `O(n)` and `O(log n)`

Consider:

```text
for(i = 0; i < n; i++)
{
    for(j = 1; j < n; j = j * 2)
        stmt;
}
```

Outer loop:

```text
O(n)
```

Inner loop:

```text
O(log n)
```

Therefore:

```text
O(n) × O(log n)
```

So:

```text
Time Complexity = O(n log n)
```

The source simplifies the total expression, e.g. `2n log n + n`, to:

```text
O(n log n)
```



---

# 17. Common Loop Patterns

From the examples in the source:

| Loop pattern            |   Complexity |
| ----------------------- | -----------: |
| `i++` until `n`         |       `O(n)` |
| `i += 2` until `n`      |       `O(n)` |
| `i--` from `n`          |       `O(n)` |
| `i *= 2`                |  `O(log₂ n)` |
| `i *= 3`                |  `O(log₃ n)` |
| `i /= 2`                |  `O(log₂ n)` |
| Nested `n × n` loops    |      `O(n²)` |
| Three nested `n` loops  |      `O(n³)` |
| `n` loop × `log n` loop | `O(n log n)` |

This is a useful quick-reference summary of the loop patterns demonstrated in pages 20 and earlier. 

---

# 18. Analysis of `if` and `while`

## `for` Loop

Example:

```text
for(i = 1; i <= n; i++)
    stmt;
```

There are approximately `n` iterations.

Therefore:

```text
O(n)
```

The loop-control operations may give an exact frequency such as:

```text
3n + 2
```

but asymptotically:

```text
O(n)
```

---

# 19. `while` Loop with Multiplication

Consider:

```text
a = 1

while(a < b)
{
    stmt;
    a = a * 2;
}
```

Values:

```text
1
2
4
8
16
...
```

Eventually:

```text
2^k >= b
```

Therefore:

```text
k = log₂ b
```

So:

```text
O(log n)
```



---

# 20. `while` Loop with Increasing `k`

The source also shows a loop where:

```text
i = 1
k = 1

while(k < n)
{
    stmt;
    k = k + i;
    i++;
}
```

The value of `k` grows through a sum:

```text
1 + 2 + 3 + 4 + ... + m
```

Using:

```text
m(m + 1) / 2
```

the source derives:

```text
m² ≈ n
```

Therefore:

```text
m ≈ √n
```

This illustrates why understanding the **mathematical growth of a loop variable** is important rather than simply counting the number of loop statements.



---

# 21. Euclidean/GCD-Style While Loop

The source gives a repeated subtraction approach:

```text
while(m != n)
{
    if(m > n)
        m = m - n;
    else
        n = n - m;
}
```

Example:

```text
m = 16
n = 2
```

The values reduce as:

```text
16 → 14 → 12 → 10 → 8 → 6 → 4 → 2
```

The source concludes:

```text
O(n)
```

for this analysis.



---

# 22. Best, Worst and Average Cases

An algorithm may behave differently depending on the input.

For example:

```text
Test(n)
{
    if(n < 5)
        print(...);
    else
        for(i = 0; i < n; i++)
            print(...);
}
```

Possible cases:

### Best Case

The condition is immediately satisfied:

```text
O(1)
```

### Worst Case

The loop executes:

```text
O(n)
```

The source uses this example to introduce best/worst-case analysis. 

---

# 23. Classes of Time Functions

The source lists common classes of time complexity.

From smaller growth to larger growth:

```text
O(1)
O(log n)
O(n)
O(n²)
O(n³)
O(2ⁿ)
O(3ⁿ)
O(nⁿ)
```

### Meaning

| Complexity | Name                 |
| ---------- | -------------------- |
| `O(1)`     | Constant             |
| `O(log n)` | Logarithmic          |
| `O(n)`     | Linear               |
| `O(n²)`    | Quadratic            |
| `O(n³)`    | Cubic                |
| `O(2ⁿ)`    | Exponential          |
| `O(3ⁿ)`    | Exponential          |
| `O(nⁿ)`    | Very rapidly growing |



---

# 24. How to Think About Growth

The source compares functions using values of `n`.

A simplified growth hierarchy is:

```text
1
<
log n
<
n
<
n log n
<
n²
<
n³
<
...
<
2ⁿ
<
3ⁿ
<
...
<
nⁿ
```

### Why this matters

As `n` becomes large, the difference becomes huge.

For example:

```text
n = 8

n² = 64
2ⁿ = 256
```

For larger `n`, exponential functions grow dramatically faster than polynomial functions.

The source illustrates this with tables and a graph showing the relative growth of `log n`, `n`, `n²`, `n³`, and `2ⁿ`. 

---

# 25. Asymptotic Notations

The source introduces three major asymptotic notations:

```text
O       → Big-O       → Upper Bound
Ω       → Big-Omega   → Lower Bound
Θ       → Big-Theta   → Average/Tight Bound
```



> **Important:** In formal algorithm analysis, `Θ` is normally called a **tight asymptotic bound** rather than simply an "average bound." The source labels it as average bound, so the terminology above follows the source while clarifying the usual interpretation.

---

# 26. Big-O — Upper Bound

Big-O represents an **upper bound**.

The source defines:

```text
f(n) = O(g(n))
```

if there exist positive constants `c` and `n₀` such that:

```text
f(n) ≤ c × g(n)
```

for:

```text
n ≥ n₀
```

### Example

Suppose:

```text
f(n) = 2n + 3
```

We can show that:

```text
f(n) = O(n)
```

because for sufficiently large `n`:

```text
2n + 3 ≤ c × n
```

for some constant `c`.

The source also shows that the same function can have more than one valid Big-O upper bound, such as `O(n)` and a looser `O(n²)`. 

---

# 27. Big-Omega — Lower Bound

Big-Omega represents a **lower bound**.

The source defines:

```text
f(n) = Ω(g(n))
```

if there exist positive constants `c` and `n₀` such that:

```text
f(n) ≥ c × g(n)
```

for:

```text
n ≥ n₀
```

### Example

For:

```text
f(n) = 2n + 3
```

we can establish:

```text
f(n) = Ω(n)
```

because the function grows at least linearly.



---

# 28. Big-Theta — Tight Bound

Theta gives both an upper and lower bound.

The source represents:

```text
f(n) = Θ(g(n))
```

when:

```text
c₁g(n) ≤ f(n) ≤ c₂g(n)
```

for suitable positive constants and sufficiently large `n`.

### Simple meaning

```text
O(g(n))   → f doesn't grow faster than g(n)
Ω(g(n))   → f doesn't grow slower than g(n)
Θ(g(n))   → f grows at the same asymptotic rate as g(n)
```

For example:

```text
f(n) = 2n + 3
```

has:

```text
Θ(n)
```



---

# 29. Example: `2n² + 3n + 4`

The source analyzes:

```text
f(n) = 2n² + 3n + 4
```

### Lower bound

The dominant term is:

```text
n²
```

Therefore:

```text
f(n) = Ω(n²)
```

### Upper bound

Similarly:

```text
f(n) = O(n²)
```

Therefore:

```text
f(n) = Θ(n²)
```

This is one of the key examples used to understand asymptotic notation. 

---

# 30. Example: `n² log n + n`

The source analyzes:

```text
f(n) = n² log n + n
```

The dominant growth is:

```text
n² log n
```

Therefore:

```text
f(n) = O(n² log n)
```

and:

```text
f(n) = Ω(n² log n)
```

Hence:

```text
f(n) = Θ(n² log n)
```



---

# 31. Factorial Function

The source analyzes:

```text
f(n) = n!
```

Recall:

```text
n! = n × (n-1) × (n-2) × ... × 2 × 1
```

Since every factor is at most `n`:

```text
n! ≤ n × n × n × ... × n
```

which gives:

```text
n! ≤ nⁿ
```

So the source derives:

```text
n! = O(nⁿ)
```



---

# 32. Logarithm of Factorial

The source also analyzes:

```text
f(n) = log(n!)
```

Using:

```text
log(a × b) = log a + log b
```

we get:

```text
log(n!)
= log(n × (n-1) × ... × 1)
```

which becomes:

```text
log n + log(n-1) + ... + log 1
```

The source establishes the growth in the range:

```text
Ω(n) and O(n log n)
```

as shown in the notes.



---

# 33. Properties of Asymptotic Notations

The source introduces several useful properties.

---

## 33.1 General Property

If:

```text
f(n) = O(g(n))
```

then multiplying by a constant does not change the asymptotic class:

```text
a × f(n) = O(g(n))
```

for a constant `a`.

### Example

If:

```text
f(n) = 2n + 5
```

then:

```text
7f(n)
```

is still:

```text
O(n)
```



---

# 34. Reflexive Property

If:

```text
f(n) is given
```

then:

```text
f(n) = O(f(n))
```

### Example

```text
f(n) = n²
```

Therefore:

```text
f(n) = O(n²)
```



---

# 35. Transitive Property

If:

```text
f(n) = O(g(n))
```

and:

```text
g(n) = O(h(n))
```

then:

```text
f(n) = O(h(n))
```

### Example

Suppose:

```text
f(n) = n
g(n) = n²
h(n) = n³
```

We know:

```text
n = O(n²)
```

and:

```text
n² = O(n³)
```

Therefore:

```text
n = O(n³)
```



---

# 36. Symmetric Property

If:

```text
f(n) = O(g(n))
```

then the corresponding relationship can be expressed in the opposite direction using Omega:

```text
g(n) = Ω(f(n))
```

This connects upper and lower bounds.

The source demonstrates this with:

```text
f(n) = n²
g(n) = n
```

and the corresponding asymptotic relationships. 

---

# 37. Transpose Symmetry

The source gives:

```text
f(n) = O(g(n))
```

then:

```text
g(n) = Ω(f(n))
```

This is another way of expressing the relationship between Big-O and Big-Omega.

### Easy memory trick

```text
O  ↔  Ω
```

They are opposite-bound relationships.



---

# 38. When Both `O` and `Ω` Are Known

If:

```text
f(n) = O(g(n))
```

and:

```text
f(n) = Ω(g(n))
```

then:

```text
f(n) = Θ(g(n))
```

### Easy way to remember

```text
Upper bound + Lower bound
           ↓
       Tight bound
           ↓
          Θ
```



---

# 39. Addition Property

If:

```text
f(n) = O(g(n))
```

and:

```text
d(n) = O(e(n))
```

then:

```text
f(n) + d(n)
=
O(max(g(n), e(n)))
```

### Example

Suppose:

```text
f(n) = n²
d(n) = n
```

Then:

```text
f(n) + d(n)
= n² + n
```

The dominant term is `n²`, so:

```text
O(n²)
```

The source explicitly shows this principle. 

---

# 40. Multiplication Property

If:

```text
f(n) = O(g(n))
```

and:

```text
d(n) = O(e(n))
```

then:

```text
f(n) × d(n)
=
O(g(n) × e(n))
```

### Example

If:

```text
f(n) = O(n)
d(n) = O(n²)
```

then:

```text
f(n)d(n)
=
O(n × n²)
=
O(n³)
```



---

# 41. Comparing Functions

The source then focuses heavily on comparing the growth rates of functions.

For example:

```text
n² < n³
```

for sufficiently large `n`.

At small values:

```text
n = 2
n² = 4
n³ = 8

n = 3
n² = 9
n³ = 27
```

This demonstrates that the cubic function grows faster than the quadratic function.



---

# 42. Useful Logarithm Rules

The source uses these rules repeatedly when comparing functions.

## Rule 1

```text
log(ab) = log a + log b
```

## Rule 2

```text
log(a/b) = log a - log b
```

## Rule 3

```text
log(a^b) = b log a
```

## Rule 4

Change of base:

```text
log_a b = log_c b / log_c a
```

The key point is that changing the logarithm's base only introduces a constant factor, which does not change the asymptotic complexity class. 

---

# 43. Comparing `n²` and `n³`

To compare:

```text
n² < n³
```

for large `n`, take logarithms:

```text
log(n²) < log(n³)
```

Using:

```text
log(a^b) = b log a
```

we get:

```text
2 log n < 3 log n
```

which is true for positive `n > 1`.

Therefore:

```text
n² = O(n³)
```



---

# 44. Comparing More Complicated Functions

The source gives examples such as:

```text
f(n) = n^(√n)
```

and:

```text
g(n) = 2^(√n log n)
```

The technique is:

1. Take logarithm of both functions.
2. Simplify using logarithm identities.
3. Compare the resulting expressions.
4. Determine which original function grows faster.

This is an important technique for complicated asymptotic comparisons.



---

# 45. Comparing `2^n` and `2^(2n)`

The source also compares:

```text
f(n) = 2^n
```

with:

```text
g(n) = 2^(2n)
```

Take logs:

```text
log(2^n) = n log 2
```

and:

```text
log(2^(2n)) = 2n log 2
```

Therefore the second function grows faster:

```text
2^n < 2^(2n)
```

as `n` grows.



---

# 46. Piecewise Function Comparison

The source gives piecewise functions such as:

```text
g(n) =
    n³   if n < 100
    n²   if n ≥ 100
```

and another function:

```text
O2(n) =
    n²   if n < 10,000
    n³   if n ≥ 10,000
```

The important lesson is:

> When comparing piecewise functions, you must consider the relevant ranges of `n`.

A function may behave differently for small and large input sizes.



---

# 47. True / False Asymptotic Questions

The source ends the function-comparison section with several true/false-style statements.

Examples include comparisons involving:

```text
(n + k)^m
2^(2n)
4^n
√(log n)
n^(log n)
```

The purpose is to test whether you can:

* Ignore constants appropriately
* Compare exponential functions
* Apply logarithms
* Recognize dominant growth
* Determine whether two complexity classes are equivalent

The exact handwritten markings are visible on page 59. 

---

# 48. Best, Worst and Average Case Analysis

The final section of the PDF focuses on:

1. **Linear Search**
2. **Binary Search Tree**

The key idea is that the same algorithm can have different running times depending on the input.

---

# 49. Linear Search

Suppose:

```text
A = [86, 12, 5, 9, 7, 4, 3, 16, 18]
```

and we want to find a particular key.

Linear search checks elements one by one:

```text
A[0]
A[1]
A[2]
...
A[n-1]
```

---

## Best Case

The key is found at the **first position**.

Number of comparisons:

```text
1
```

Therefore:

```text
Best-case time = O(1)
```

and:

```text
B(n) = O(1)
```



---

# 50. Worst Case — Linear Search

The worst case occurs when the key is:

* At the last position, or
* Not present at all.

Then we may inspect all `n` elements.

Therefore:

```text
Worst-case time = O(n)
```

The source represents this as:

```text
W(n) = O(n)
```



---

# 51. Average Case — Linear Search

The source shows the average number of comparisons as approximately:

```text
(n + 1) / 2
```

Therefore:

```text
A(n) = (n + 1) / 2
```

Ignoring constants:

```text
A(n) = O(n)
```

The source also shows:

```text
B(n) = Θ(1)
W(n) = Θ(n)
```

and:

```text
A(n) = Θ(n)
```



---

# 52. Linear Search — Final Cheat Sheet

| Case    | Comparisons | Complexity |
| ------- | ----------: | ---------: |
| Best    |         `1` |     `O(1)` |
| Average |   `(n+1)/2` |     `O(n)` |
| Worst   |         `n` |     `O(n)` |

### Remember

```text
Linear Search

Best    → O(1)
Average → O(n)
Worst   → O(n)
```

---

# 53. Binary Search Tree — Best and Worst Case

The final pages introduce a Binary Search Tree (BST).

Example tree:

```text
          20
        /    \
      10      30
     /  \    /  \
    5   15  25  40
```

The source then considers searching for an element.

---

## Best Case

If the searched key is at the root:

```text
20
```

only one comparison/search step is needed.

Therefore:

```text
Best-case time = O(1)
```

---

# 54. Worst Case — Binary Search Tree

If the tree becomes highly skewed, the search may have to travel through many nodes.

The source shows a skewed tree structure where the height can become approximately:

```text
n
```

Therefore:

```text
Worst-case time = O(n)
```

---

# 55. Balanced BST

For a reasonably balanced binary search tree, the search path reduces the remaining search space substantially at each level.

The source gives the best/worst bounds in terms of the tree height and shows the logarithmic case:

```text
min(W(n)) = log n
```

and:

```text
max(W(n)) = n
```

Therefore, depending on tree shape:

```text
Balanced BST → O(log n)
Skewed BST   → O(n)
```



---

# 56. Most Important Complexity Patterns

Based on the entire PDF, these are the patterns you should recognize immediately.

| Code Pattern                          |   Complexity |
| ------------------------------------- | -----------: |
| Single statement                      |       `O(1)` |
| `i++` until `n`                       |       `O(n)` |
| `i += 2` until `n`                    |       `O(n)` |
| `i--` until `0`                       |       `O(n)` |
| `i *= 2`                              |   `O(log n)` |
| `i /= 2`                              |   `O(log n)` |
| Two independent `O(n)` loops          |       `O(n)` |
| Nested `n × n` loops                  |      `O(n²)` |
| Three nested `n` loops                |      `O(n³)` |
| `n` loop containing `log n` loop      | `O(n log n)` |
| Summation `1+2+...+n`                 |      `O(n²)` |
| Multiplication/division growth        |   `O(log n)` |
| Certain square-growth loop conditions |      `O(√n)` |
| Balanced BST search                   |   `O(log n)` |
| Skewed BST search                     |       `O(n)` |

---

# 57. Complexity Growth Order

For interview purposes, memorize this ordering:

```text
O(1)
    ↓
O(log n)
    ↓
O(n)
    ↓
O(n log n)
    ↓
O(n²)
    ↓
O(n³)
    ↓
O(2ⁿ)
    ↓
O(3ⁿ)
    ↓
O(nⁿ)
```

The further down the list you go, the faster the function grows as `n` becomes large. The source's comparison table/graph illustrates this growth behavior. 

---

# 58. How to Calculate Time Complexity — Practical Method

When you get a DSA problem in an interview, use this process.

## Step 1 — Find the input size

Usually:

```text
n = size of input
```

For matrices:

```text
n = dimension of matrix
```

---

## Step 2 — Identify loops

Ask:

```text
How many times does this loop execute?
```

Examples:

```text
i++       → n
i += 2    → n/2 → O(n)
i *= 2    → log n
i /= 2    → log n
```

---

## Step 3 — Analyze nested loops

If loops are nested:

```text
for n
    for n
```

multiply:

```text
n × n = n²
```

If:

```text
for n
    for log n
```

then:

```text
n × log n
=
O(n log n)
```

---

## Step 4 — Analyze sequential blocks

If code is:

```text
Block 1 → O(n)
Block 2 → O(n²)
Block 3 → O(log n)
```

then:

```text
O(n + n² + log n)
```

The dominant growth determines the final class:

```text
O(n²)
```

This follows the source's asymptotic addition principle. 

---

# 59. How to Calculate Space Complexity

Count the memory that grows with input size.

### Example

```text
a = 10
b = 20
temp = 0
```

Number of variables is fixed:

```text
O(1)
```

But:

```text
A[n]
```

requires memory proportional to `n`:

```text
O(n)
```

And:

```text
A[n][n]
```

requires:

```text
O(n²)
```

### Quick pattern

```text
Single variable      → O(1)
Array of n            → O(n)
Matrix n × n          → O(n²)
Three-dimensional data → O(n³)
```

The matrix examples in the source explicitly demonstrate the difference between `O(n)` and `O(n²)` space. 

---

# 60. Frequency Count — Interview Formula

A useful way to think about frequency counting:

```text
Total operations
=
(number of executions of statement 1)
+
(number of executions of statement 2)
+
...
```

For example:

```text
for(i = 0; i < n; i++)
    statement
```

roughly gives:

```text
n
```

executions of the statement.

For:

```text
for(i = 0; i < n; i++)
    for(j = 0; j < n; j++)
        statement
```

the statement executes:

```text
n × n
=
n²
```

times.

For:

```text
for(i = 1; i < n; i *= 2)
```

the iterations satisfy:

```text
2^k ≈ n
```

so:

```text
k ≈ log₂ n
```

---

# 61. The Most Important Rules to Memorize

## Rule 1 — Ignore Constants

```text
O(2n) = O(n)

O(5n²) = O(n²)
```

---

## Rule 2 — Keep the Dominant Term

```text
O(n² + n + 10)
=
O(n²)
```

---

## Rule 3 — Sequential Code Adds

```text
O(n) + O(n²)
=
O(n²)
```

---

## Rule 4 — Nested Code Multiplies

```text
O(n) × O(n)
=
O(n²)
```

---

## Rule 5 — Multiplication/Division Growth Means Logarithm

```text
i = i × 2
```

or:

```text
i = i / 2
```

usually leads to:

```text
O(log n)
```

---

## Rule 6 — Summation Can Create Quadratic Complexity

```text
1 + 2 + 3 + ... + n
=
n(n+1)/2
=
O(n²)
```

---

## Rule 7 — Both Upper and Lower Bounds Give Theta

```text
O(g(n)) + Ω(g(n))
        ↓
Θ(g(n))
```

---

# 62. Best/Worst/Average — Quick Revision

For **Linear Search**:

```text
Best Case
→ Element at first position
→ O(1)

Average Case
→ Approximately (n+1)/2 comparisons
→ O(n)

Worst Case
→ Element at last position/not found
→ O(n)
```

For the **Binary Search Tree** shown:

```text
Best Case
→ Search key at root
→ O(1)

Balanced tree
→ O(log n)

Worst/skewed tree
→ O(n)
```

These are the final examples presented in the source. 

---

# 63. Final Interview Cheat Sheet

## Complexity Classes

```text
O(1)        Constant
O(log n)    Logarithmic
O(n)        Linear
O(n log n)  Linearithmic
O(n²)       Quadratic
O(n³)       Cubic
O(2ⁿ)       Exponential
O(3ⁿ)       Exponential
O(nⁿ)       Very high growth
```

## Asymptotic Notations

```text
O(g(n))  → Upper Bound
Ω(g(n))  → Lower Bound
Θ(g(n))  → Tight Bound
```

## Loop Recognition

```text
i++          → O(n)
i += k       → O(n)
i *= k       → O(log n)
i /= k       → O(log n)

n nested with n       → O(n²)
n nested with log n   → O(n log n)
three n loops         → O(n³)
```

## Space

```text
Fixed variables       → O(1)
Array of n            → O(n)
Matrix n × n          → O(n²)
```

## Search

```text
Linear Search
Best    → O(1)
Average → O(n)
Worst   → O(n)

BST
Best/root     → O(1)
Balanced      → O(log n)
Skewed        → O(n)
```

---

# 64. One-Page Mental Model

If you want to remember the entire PDF without going through the screenshots again, remember this:

```text
                    ALGORITHM ANALYSIS
                           |
             +-------------+-------------+
             |                           |
           TIME                        SPACE
             |                           |
      Count operations             Count memory
             |                           |
       Frequency Count              O(1), O(n),
             |                     O(n²), ...
             |
      +------+------+
      |             |
    LOOPS         ASYMPTOTIC
      |             |
  n → O(n)       O → Upper
  log → O(log n) Ω → Lower
  n² → O(n²)     Θ → Tight
  n³ → O(n³)
      |
      +-------------------------+
      |                         |
 Best / Average / Worst    Compare Growth
      |                         |
 Linear Search             1 < log n < n
 BST                       < n² < n³ < 2ⁿ
```

---

# 65. What You Should Be Able to Do After These Notes

For DSA interviews, you should now be able to look at code and answer:

### 1. How many times does this loop execute?

```text
i++
→ n times

i *= 2
→ log n times
```

### 2. What happens with nested loops?

```text
n × n
→ n²
```

### 3. What happens with nested different complexities?

```text
n × log n
→ n log n
```

### 4. What happens with sequential blocks?

```text
n + n² + log n
→ n²
```

### 5. What is the difference between O, Ω and Θ?

```text
O  → upper bound
Ω  → lower bound
Θ  → tight bound
```

### 6. What are best/worst cases?

```text
Best    → minimum work
Worst   → maximum work
Average → expected/average work
```

### 7. What happens to BST search?

```text
Balanced → O(log n)
Skewed   → O(n)
```

---

## Final Takeaway

The central theme of the entire PDF is:

> **Don't measure an algorithm by the actual seconds it takes. Analyze how the number of operations and memory requirements grow as the input size `n` increases.**

The workflow to use in interviews is:

```text
Understand the code
       ↓
Identify input size n
       ↓
Count loop iterations / operations
       ↓
Derive f(n)
       ↓
Remove constants + lower-order terms
       ↓
Get O / Ω / Θ
       ↓
Analyze space separately
       ↓
Consider best / average / worst case
```

This turns the handwritten 65-page material into a much more usable **Time & Space Complexity revision document** while retaining the examples and progression of the original screenshots. 
