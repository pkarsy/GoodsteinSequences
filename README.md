# GoodsteinSequences

My try to understand the enormous Goodstein Sequences.

> **Disclaimer:** I am not a mathematician — nothing here is authoritative. This is
> a personal exploration project. I am not even familiar with the proofs involved.

> **Note:** This is an **educational** tool, not a computational one. The famous
> Goodstein sequence starting from 4 in base 2 — G(4) — terminates, but its full
> length is incomprehensibly large (FAR beyond the number of atoms in the universe).
> No program or computer system can print it. Stick to small initial values (≤ 12) and a reasonable
> starting base (>2) — the joy is watching the structure decompose, not brute-forcing
> huge numbers.

## What is a Goodstein sequence?

A Goodstein sequence starts from a number `n` written in **hereditary base-`b`** representation — not only the number but also every exponent is expanded in the same base. Then you repeatedly:

1. **Increase the base** by 1 (2 → 3 → 4 → …)
2. **Subtract 1** from the value

Despite looking like it should grow forever (the base keeps increasing), **Goodstein's theorem** (proved by Reuben Goodstein in 1944) proves the sequence always reaches 0.


**Sidenote:** Remarkably, this theorem is independent of Peano arithmetic — it cannot be proved using ordinary arithmetic alone (the standard axioms); it requires the tools of set theory. The proof (that it is not provable in PA) finalized much later (Kirby-Paris 1982), and obviously it is a much harder problem.

Anyone who tried to study these sequences knows that G(3) is very small but G(4) is so long there is no way to visualize it or run the full sequence via a program. And yet it will start at some point to decrease one by one, and inevitably the sequence terminates at zero.

## Key insight

Although the bases can grow very fast, the critical point is that the **exponents never grow** and occasionally shrink. For example:

```
5^2 → 6^2 - 1 → 5·6¹ + 5
```

When the number has the form `1·base + const` the value cannot grow anymore, and after many steps the base becomes larger than the number itself (`0·base + const`). From then on the number shrinks by one each step until it reaches 0.

Note this is NOT a formal proof, but it gives the intuition. The definition of a Goodstein sequence is straightforward, yet the theorem that every sequence terminates — though expressible in Peano arithmetic — cannot be proved within Peano arithmetic itself.

## How the code works

The program uses an **efficient symbolic representation** that avoids ever computing the astronomically large integers. It works directly on a recursive tree structure rather than converting to `int`.

### Hereditary representation (internal format)

A number is stored as a nested Python structure:

| Type | Meaning | Example |
|------|---------|---------|
| `int` | A simple constant `< base` | `5` |
| `tuple (coeff, exponent)` | `coeff · base`<sup>exponent</sup> | `(2, (1,1))` → `2·B¹` |
| `list` | A sum of terms | `[(1, 2), 5]` → `B² + 5` |

The exponent itself can be another tuple or list — that's the "hereditary" part.

### Key functions

| Function | Purpose |
|----------|---------|
| `int_to_hereditary(n, b)` | Converts an integer `n` into hereditary base-`b` form |
| `hereditary_to_int(h, b)` | Converts back to integer (for debugging — overflows on large sequences) |
| `hereditary_to_string(h, b)` | Pretty-prints the representation (e.g. `3^2+1`) |
| `constant(h)` | Extracts the constant term (the rightmost integer, if any) |
| `hereditary_sub_one(h, b)` | Subtracts 1 *without* converting to int — works on the symbolic form directly |
| `hereditary_sub(h, b, n)` | Subtracts `n` from a hereditary form (used for the skip-ahead optimization) |
| `hereditary_trivial_steps(h, b)` | Skips the "constant decay" segment at once |

### The `Goodstein` class

```python
from goodstein import Goodstein

g = Goodstein(10, 3)   # start value 10, initial base 3
g.run()                # prints the full sequence
```

**Methods:**
- `run(skip=True, showVal=False, showStep=False, maxBase=1_000_000_000)` — prints the sequence. When `skip` is on (default) it skips ahead in chunks where the constant term is large, marking those jumps with `[Decomposing]`.
- `step(n=1)` — advances by one or more steps (increase base + subtract).
- `base()` / `value()` — current base and hereditary value.
- `constant()` — the constant term (0 if the number is a pure power).
- `reset()` — resets to the initial value and base.
- `is_zero()` — has the sequence terminated?
- `__int__()` — converts back to an integer (beware: can be astronomically large).

## Program shortcuts

The python script does some shortcuts:
- skips trivial repeated steps making it more manageable
- shows explanations on what it is doing
- allows starting with bases other than 2. For example:

```
Goodstein(10,3) ends at base 159
Goodstein(11,3) ends at base 383
Goodstein(12,3) ends at base 2047
```

## Example output

```
> python goodstein.py 10 3

Base=3 : 3^2+1
Base=4 : 4^2
[Decomposing]
Base=5 : 4*5+4
Base=6 : 4*6+3
Base=7 : 4*7+2
Base=8 : 4*8+1
Base=9 : 4*9
[Decomposing]
Base=10 : 3*10+9
Base=11 : 3*11+8
Base=12 : 3*12+7
...
Base=16 : 3*16+3
Base=17 : 3*17+2
Base=18 : 3*18+1
Base=19 : 3*19
[Decomposing]
Base=20 : 2*20+19
Base=21 : 2*21+18
Base=22 : 2*22+17
...
Base=36 : 2*36+3
Base=37 : 2*37+2
Base=38 : 2*38+1
Base=39 : 2*39
[Decomposing]
Base=40 : 40+39
Base=41 : 41+38
Base=42 : 42+37
...
Base=76 : 76+3
Base=77 : 77+2
Base=78 : 78+1
Base=79 : 79
[Decomposing]
Base=80 : 79
Base=81 : 78
Base=82 : 77
...
Base=156 : 3
Base=157 : 2
Base=158 : 1
Base=159 : 0
```

## Running the program

From the shell:

```
python goodstein.py <initial_value> <initial_base> [-b <max_base>]
python goodstein.py 10 3
# The famous G(4), we cannot print it all, for sure
# The code can go beyond 10000 if skips trivial steps
python goodstein.py 4 2 -b 10000
```

Or from the Python interpreter:

```python
import goodstein
g = goodstein.Goodstein(10, 3)
g.run()
```
