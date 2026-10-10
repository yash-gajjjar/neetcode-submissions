# Bit Manipulation — DSA Interview Notes
*Bit Operations · Essential Bit Tricks · Common Bit Patterns (XOR, Counting, Bitmasks)*

> **Note:** One source topic (Bit Operations) was given, so it's organized into the three groupings that matter for interviews: the operators themselves, the small set of reusable tricks built from them, and the problem patterns that signal "use bits."

---

## How to use these notes
- **First pass:** read concept + "why it works" sections, trace the binary examples by hand.
- **Revision pass (pre-interview):** jump straight to the 🔑 Cheat Sheet and Pattern Recognition tables at the top of each section.
- **While solving:** use the "Signal → Technique" tables to map problem phrasing to the right trick in <10 seconds.

All code examples in Python.

---

## 🔑 Cheat Sheet — All Three Sections at a Glance
| Section | Core Idea | Time | Space |
|---|---|---|---|
| Bit Operations | AND, OR, XOR, NOT, left/right shift act directly on the binary representation of integers | O(1) per op | O(1) |
| Essential Bit Tricks | A handful of one-liners: check/set/clear/toggle bit, `n & (n-1)`, `n & -n` | O(1) | O(1) |
| Common Bit Patterns | XOR cancellation, counting set bits, bitmask subsets, bit-by-bit construction | O(n) or O(bits) | O(1) typical |

**Core shared idea:** bit manipulation lets you do work **directly on the binary representation** of numbers, often replacing a hashmap (O(n) space) with a single integer (O(1) space), or replacing a loop with one operation. Most interview problems reduce to a few identities: `x ^ x = 0`, `x ^ 0 = x`, `n & (n-1)` clears the lowest set bit.

---

# 1. Bit Operations

## 🔑 Cheat Sheet
| Operator | Symbol | Rule (per bit) | Example (`5 = 101`, `3 = 011`) |
|---|---|---|---|
| AND | `&` | 1 only if **both** bits are 1 | `5 & 3 = 001 = 1` |
| OR | `\|` | 1 if **either** bit is 1 | `5 \| 3 = 111 = 7` |
| XOR | `^` | 1 if the bits **differ** | `5 ^ 3 = 110 = 6` |
| NOT | `~` | Flips every bit | `~5 = -6` (see two's complement below) |
| Left shift | `<<` | Shift bits left, fill with 0 | `5 << 1 = 1010 = 10` (multiply by 2) |
| Right shift | `>>` | Shift bits right | `5 >> 1 = 10 = 2` (floor-divide by 2) |

## Core Intuition
Every integer is stored as a sequence of bits. Bitwise operators work on **each bit position independently** (except shifts, which move all bits). Because these map directly to CPU instructions, they're extremely fast, and because each bit is an independent yes/no flag, a single integer can pack many boolean values.

```
 5 = 0 1 0 1
 3 = 0 0 1 1
-----------------
 &   0 0 0 1  = 1
 |   0 1 1 1  = 7
 ^   0 1 1 0  = 6
```

### Key Identities to Memorize
| Identity | Meaning / Use |
|---|---|
| `x ^ x = 0` | XOR of a number with itself cancels it — the basis of "find the single non-duplicate" |
| `x ^ 0 = x` | XOR with 0 changes nothing |
| `x & 0 = 0`, `x \| 0 = x` | AND with 0 clears everything; OR with 0 is identity |
| `x << k = x * 2^k` | Left shift multiplies by a power of two |
| `x >> k = x // 2^k` | Right shift floor-divides by a power of two |
| XOR is commutative and associative | Order doesn't matter, so duplicates cancel regardless of position |

## Two's Complement (How Negative Numbers Work)
Most systems represent negative numbers in **two's complement**: to negate `x`, flip all bits and add 1 (`-x = ~x + 1`). In an 8-bit system, `5 = 00000101` and `-5 = 11111011`. This is why `~5 = -6` (flip all bits of 5 gives the representation of -6), and why `n & -n` isolates the lowest set bit.

## Python-Specific Caveat (Important!)
Python integers have **arbitrary precision** — there's no fixed 32-bit width, so negative numbers behave as if they have infinitely many leading 1-bits. This matters in problems that assume 32-bit overflow behavior (e.g., Sum of Two Integers, Reverse Bits):
```python
MASK = 0xFFFFFFFF          # keep only the low 32 bits
MAX_INT = 0x7FFFFFFF       # largest positive 32-bit signed int

def to_signed_32(x):
    x &= MASK
    return x if x <= MAX_INT else ~(x ^ MASK)   # reinterpret as signed
```
**Key idea:** mask with `0xFFFFFFFF` after operations that could grow past 32 bits, then convert back to a signed value if needed. Forgetting this is the most common Python-specific bit manipulation bug.

## Common Pitfalls
- Confusing **logical** vs **bitwise** operators: `and`/`or`/`not` operate on truthiness; `&`/`|`/`~` operate on bits.
- Operator precedence: `==` binds tighter than `&`, so `n & 1 == 0` parses as `n & (1 == 0)`. Always parenthesize: `(n & 1) == 0`.
- Assuming `>>` on a negative number shifts in zeros — in Python it preserves the sign (arithmetic shift), so `-8 >> 1 = -4`, and a `while n:` loop over a negative number never terminates unless you mask first.
- Forgetting that `~x` equals `-x - 1` in Python (not an unsigned flip).

## Interview Talking Points
- State the integer width assumption up front ("I'll assume 32-bit unsigned/signed") — interviewers want to see you've considered overflow and sign behavior.
- Mention the Python arbitrary-precision caveat if coding in Python and the problem involves negatives or overflow.

---

# 2. Essential Bit Tricks

## 🔑 Cheat Sheet
| Goal | Expression | Notes |
|---|---|---|
| Check if bit `i` is set | `(n >> i) & 1` or `n & (1 << i)` | Non-zero/1 means set |
| Set bit `i` | `n \| (1 << i)` | Forces the bit to 1 |
| Clear bit `i` | `n & ~(1 << i)` | Forces the bit to 0 |
| Toggle bit `i` | `n ^ (1 << i)` | Flips the bit |
| Check odd/even | `n & 1` | 1 = odd, 0 = even (last bit) |
| Clear lowest set bit | `n & (n - 1)` | Core of Brian Kernighan's algorithm |
| Isolate lowest set bit | `n & -n` | Gives a number with only that bit set |
| Check power of two | `n > 0 and (n & (n - 1)) == 0` | Powers of two have exactly one set bit |
| Swap without temp | `a ^= b; b ^= a; a ^= b` | Cute, rarely preferred in practice |

## Core Intuition: Why `n & (n - 1)` Clears the Lowest Set Bit
Subtracting 1 from `n` flips the lowest set bit to 0 and turns all the zeros **below** it into 1s. ANDing with the original `n` then wipes out that region.

```
n     = 1 0 1 1 0 0    (44)
n - 1 = 1 0 1 0 1 1    (43)   ← lowest set bit became 0, trailing zeros became 1s
n & (n-1) = 1 0 1 0 0 0  (40)  ← lowest set bit removed
```
Repeating this until `n == 0` counts set bits in exactly **as many iterations as there are set bits** (Brian Kernighan's algorithm), rather than iterating through all 32 positions.

## Worked Pattern: Number of 1 Bits (Brian Kernighan)
```python
def hammingWeight(n):
    count = 0
    while n:
        n &= n - 1       # remove the lowest set bit
        count += 1
    return count
```
**Complexity:** O(k) where k = number of set bits (at most 32), O(1) space.

## Worked Pattern: Power of Two
```python
def isPowerOfTwo(n):
    return n > 0 and (n & (n - 1)) == 0
```
**Key idea:** a power of two has exactly one set bit, so removing it with `n & (n-1)` must leave 0. The `n > 0` guard handles 0 and negatives.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "count the number of 1 bits" | `n & (n - 1)` loop (Kernighan) |
| "is n a power of two (or four)?" | `n & (n - 1) == 0` (power of four: also check the single bit is in an even position, e.g. `n & 0x55555555`) |
| "check/set/clear a specific bit" | Mask with `1 << i` plus `&`, `\|`, `& ~`, `^` |
| "isolate the rightmost set bit" | `n & -n` |
| "multiply/divide by a power of two" | Shifts `<<` / `>>` |

## Common Pitfalls
- Writing `n & n - 1` without thinking about precedence — it works (subtraction binds tighter than `&`), but parenthesize for readability.
- Forgetting the `n > 0` guard in the power-of-two check — `0 & -1 == 0` would wrongly return True.
- Using `n & -n` on Python negatives without understanding it relies on two's complement semantics (works in Python too, but be ready to explain why).

## Interview Talking Points
- Be ready to **derive** `n & (n-1)` (subtracting 1 flips the lowest set bit and everything below it), not just recite it — a very common follow-up.
- Mention Kernighan's runs in O(set bits), not O(32), as the optimization over the naive shift-and-check loop.

---

# 3. Common Bit Patterns

## 🔑 Cheat Sheet
| Pattern | Idea |
|---|---|
| XOR cancellation | XOR all elements; pairs cancel (`x ^ x = 0`), leaving the unique one |
| Counting bits for 0..n | `bits[i] = bits[i >> 1] + (i & 1)` — DP over the right-shifted value |
| Bitmask subsets | Each integer from `0` to `2^n - 1` encodes one subset (bit `j` set = element `j` included) |
| Missing number | XOR indices `0..n` with all values — everything cancels except the missing one |
| Bit-by-bit construction | Build a result by shifting and OR-ing bits (reverse bits, add without `+`) |

## Core Intuition
Most bit manipulation interview problems are variations of **three ideas**: (1) XOR cancels duplicates, (2) `n & (n-1)` and shifts let you walk bits efficiently, (3) an integer can act as a compact **set** (a bitmask) of up to ~32/64 booleans.

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "every element appears twice except one" | XOR all elements |
| "find the missing number in 0..n" | XOR indices and values, or sum formula |
| "two numbers appear once, rest twice" | XOR all (gives `a ^ b`), isolate a differing bit with `& -x`, partition into two groups, XOR each |
| "count bits for every number up to n" | DP: `bits[i] = bits[i >> 1] + (i & 1)` |
| "reverse the bits of a 32-bit integer" | Loop 32 times: shift result left, OR in the lowest bit of `n`, shift `n` right |
| "add two integers without `+`" | XOR gives sum without carry, `(a & b) << 1` gives carry; repeat until carry is 0 |
| "generate all subsets / small-n state" | Bitmask enumeration over `range(1 << n)` |
| "track visited/used flags for small sets (≤ ~20)" | Bitmask as a compact visited set (e.g., bitmask DP, TSP-style) |

## Worked Pattern: Single Number (XOR)
```python
def singleNumber(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```
**Why it works:** XOR is commutative and associative, so the order doesn't matter; every paired number cancels to 0, and `0 ^ unique = unique`. **O(n) time, O(1) space** — beats the hashmap/set approach on space.

## Worked Pattern: Missing Number (XOR)
```python
def missingNumber(nums):
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
```
**Key idea:** XOR every index `0..n` and every value; each present number appears twice (once as index, once as value) and cancels, leaving only the missing one.

## Worked Pattern: Counting Bits (DP with shifts)
```python
def countBits(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)   # bits of i = bits of i//2 + its last bit
    return bits
```
**Complexity:** O(n) total, versus O(n log n) if you counted bits independently per number.

## Worked Pattern: Sum of Two Integers (no `+`, with Python masking)
```python
def getSum(a, b):
    MASK = 0xFFFFFFFF
    MAX_INT = 0x7FFFFFFF
    while b & MASK:
        carry = ((a & b) << 1) & MASK
        a = (a ^ b) & MASK
        b = carry
    return a if b == 0 else ~(a ^ MASK)   # handle negative results (Python-specific)
```
**Key idea:** `a ^ b` adds bits without carrying; `(a & b) << 1` is the carry. Repeat until no carry remains. The masking simulates 32-bit overflow, since Python ints never overflow on their own.

## Worked Pattern: Reverse Bits
```python
def reverseBits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)   # append n's lowest bit to result
        n >>= 1
    return result
```
**Complexity:** O(32) = O(1) time, O(1) space.

## Worked Pattern: Bitmask Subset Enumeration
```python
def subsets_bitmask(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):                 # 2^n subsets
        subset = [nums[j] for j in range(n) if mask & (1 << j)]
        result.append(subset)
    return result
```
**Key idea:** each integer `mask` from `0` to `2^n - 1` is a binary string selecting which elements to include — an iterative alternative to the recursive backtracking version in the Backtracking notes, and the foundation of **bitmask DP**.

## Common Pitfalls
- Forgetting the 32-bit masking in Python for Sum of Two Integers / Reverse Bits — loops can run forever or return wrong negatives.
- Using XOR cancellation when elements appear an odd number of times other than once (e.g., thrice) — the trick relies on **pairs** canceling; "all appear three times except one" needs per-bit counting mod 3 instead.
- Bitmask enumeration with large `n` — `2^n` grows fast; it's only viable for roughly `n ≤ 20`.
- Off-by-one in bit positions: bit `0` is the **least** significant bit, so `1 << i` targets bit `i` counted from the right.

## Interview Talking Points
- For XOR problems, explain the **cancellation argument** (`x ^ x = 0`, commutativity) rather than just coding it — and contrast the O(1) space with the obvious hashset approach.
- For "two unique numbers" variants, narrate the partition trick: the XOR of the two uniques is non-zero, so some bit differs; use it to split the array into two groups, each containing exactly one unique.
- Connect bitmasks back to Backtracking (subsets) and forward to bitmask DP when `n` is small, showing you see the pattern across topics.

---

## 📋 Quick Cross-Section Revision Table

| Question to Ask Yourself | If Yes → |
|---|---|
| Do duplicates need to cancel out, leaving a unique element? | XOR all elements |
| Do I need to count, clear, or isolate set bits? | `n & (n-1)` (clear lowest), `n & -n` (isolate lowest) |
| Is it a power-of-two check? | `n > 0 and n & (n-1) == 0` |
| Do I need to represent a small set of booleans/choices compactly? | Bitmask (`1 << i`) |
| Am I coding in Python with 32-bit semantics (negatives, overflow)? | Mask with `0xFFFFFFFF` and convert back to signed |
| Does a problem forbid `+` / arithmetic operators? | XOR for sum, `(a & b) << 1` for carry |

## Suggested Problem Set for This Section
- **Bit tricks:** Number of 1 Bits, Power of Two, Counting Bits
- **XOR patterns:** Single Number, Missing Number, Single Number III (two uniques)
- **Construction / overflow handling:** Reverse Bits, Sum of Two Integers, Reverse Integer
- **Bitmask:** Subsets (bitmask version), Maximum Product of Word Lengths

---
*Format matches your Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, Tries, Backtracking, Graphs I & II, Heap, 1-D DP, and 2-D DP notes: concept → intuition → deep dive → patterns → pitfalls → interview Q&A, adapted for DSA revision speed.*
