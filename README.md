# GoodsteinSequences

My try to understand the enormous Goodstein Sequences.

> **Disclaimer:** I am not a mathematician — nothing here is authoritative. This is
> a personal exploration project. I am not even familiar with the proofs involved.
> For the real thing see the
> [Wikipedia article on Goodstein's theorem](https://en.wikipedia.org/wiki/Goodstein%27s_theorem).

> **Note:** This is an **educational** tool, not a computational one. The famous
> Goodstein sequence starting from 4 in base 2 — G(4) — terminates, but its full
> length is incomprehensibly large (FAR beyond the number of atoms in the universe).
> No program or computer system can print it. Stick to small initial values (≤ 12) and a reasonable
> starting base (>2) — the joy is watching the structure decompose, not brute-forcing
> huge numbers. When comfortable, you can increase moderatelly the initial value, and the stop base(-b)

## What is a Goodstein sequence?

A Goodstein sequence starts from a number `n` written in **hereditary base-`b`** representation — not only the number but also every exponent is expanded in the same base. Then you repeatedly:

1. **Increase the base** by 1 (2 → 3 → 4 → …)
2. **Subtract 1** from the value

Despite looking like it should grow forever (the base keeps increasing), **Goodstein's theorem** (Reuben Goodstein, 1944) proves the sequence always reaches 0.

**Sidenote:** Remarkably, this theorem is independent of Peano arithmetic — it cannot be proved using ordinary arithmetic alone (the standard Peano Axioms); it requires the tools of set theory. The proof (that it is not provable in PA) was finalized much later (Kirby–Paris 1982), and obviously it is a much harder problem. But it is also what makes the sequence so important.

Indeed, Goodstein's theorem is a concrete example of a true statement that is not provable in Peano arithmetic (PA), but is provable in stronger set theories like ZFC. **This makes it a paradigmatic instance of Gödel incompleteness:** a natural mathematical fact that lies beyond the reach of PA, much like the self-referential sentence constructed in Gödel's proof, but without the artificial flavor.

Perhaps even more interesting is that the theorem seems (by seeing some examples) **visibly true** — and yet it cannot be proved without infinity.

## Examples

### G(4) — a glimpse

The sequence G(4) is far too long to print, but with `-s 0` (landmark-only mode) and `-d` (no decomposing markers) we can watch its structural evolution:

```
$ python goodstein.py 4 2 -s 0 -d -b 10000000000
B=2 : B^B
B=5 : 2*B^2+2*B   No more B^B
B=11 : 2*B^2+B
B=23 : 2*B^2
B=47 : B^2+23*B   No more 2*B^2
B=95 : B^2+22*B
B=191 : B^2+21*B
B=383 : B^2+20*B
B=767 : B^2+19*B
B=1535 : B^2+18*B
B=3071 : B^2+17*B
B=6143 : B^2+16*B
B=12287 : B^2+15*B
B=24575 : B^2+14*B
B=49151 : B^2+13*B
B=98303 : B^2+12*B
B=196607 : B^2+11*B
B=393215 : B^2+10*B
B=786431 : B^2+9*B
B=1572863 : B^2+8*B
B=3145727 : B^2+7*B
B=6291455 : B^2+6*B
B=12582911 : B^2+5*B
B=25165823 : B^2+4*B
B=50331647 : B^2+3*B
B=100663295 : B^2+2*B
B=201326591 : B^2+B
B=402653183 : B^2
B=805306367 : 402653183*B  No more B^2
B=1610612735 : 402653182*B
B=3221225471 : 402653181*B
B=6442450943 : 402653180*B

...
The python script cannot go there but our logic can
For some unfathonably huge value of B
the coefficient of B shrinks until B no longer appears in the sequence
from now on the elements decrease one by one until 0
```

Each line is a **structural landmark** — a point where the constant term has just run down to zero and the form is about to decompose. The bases follow the pattern `Bₙ₊₁ = 2·Bₙ + 1` (2, 5, 11, 23, 47, …)

### A fully printable sequence

For a sequence that actually can printed fully, try a larger starting base:

```
$ python goodstein.py 10 3
B=3 : B^2+1
B=4 : B^2
[Decomposing]
B=5 : 4*B+4  No more B^2
B=6 : 4*B+3
B=7 : 4*B+2
B=8 : 4*B+1
B=9 : 4*B
[Decomposing]
B=10 : 3*B+9
B=11 : 3*B+8
B=12 : 3*B+7
...
B=16 : 3*B+3
B=17 : 3*B+2
B=18 : 3*B+1
B=19 : 3*B
[Decomposing]
B=20 : 2*B+19
B=21 : 2*B+18
B=22 : 2*B+17
...
B=36 : 2*B+3
B=37 : 2*B+2
B=38 : 2*B+1
B=39 : 2*B
[Decomposing]
B=40 : B+39
B=41 : B+38
B=42 : B+37
...
B=76 : B+3
B=77 : B+2
B=78 : B+1
B=79 : B
[Decomposing]
B=80 : 79 No more B. From now on the elements decrease
B=81 : 78
B=82 : 77
...
B=156 : 3
B=157 : 2
B=158 : 1
B=159 : 0
```

The `[Decomposing]` marker appears whenever the constant term vanishes and the next step will structurally decompose the number.

## Key insight

Although the bases can grow very fast, the critical point is that the **non base exponents and coefficients never grow** and occasionally shrink. For example:

When the number has the form `1·base + const` the value cannot grow anymore, and after many steps the base becomes larger than the number itself (`0·base + const`). From then on the number shrinks by one each step until it reaches 0.

Note this is NOT a formal proof, but it gives the intuition. The definition of a Goodstein sequence is straightforward, yet the theorem that every sequence terminates — though expressible in Peano arithmetic — cannot be proved within Peano arithmetic itself, as we have seen.

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

## Running the program

From the shell:

```
python goodstein.py <initial_value> <initial_base> [-b <max_base>] [-B] [-s N] [-d]
```

| Flag | Meaning |
|------|---------|
| `initial_value` | Starting value of the sequence (e.g. 4, 10) |
| `initial_base` | Starting base (e.g. 2, 3) |
| `-b N` | Stop when base exceeds N (default: 1 000 000 000) |
| `-B` | Show base as its numeric value instead of the default `B` |
| `-s N` | Print N steps, then fast-forward to the next landmark (0 = only landmarks) |
| `-d` | Suppress the `[Decomposing]` marker |

Examples:

```
# Default: symbolic base B, all steps:
python goodstein.py 10 3

# Numeric base instead of B:
python goodstein.py 10 3 -B

# Only structural landmarks, no markers:
python goodstein.py 4 2 -s 0 -d

```

Or from the Python interpreter:

```python
import goodstein
g = goodstein.Goodstein(10, 3)
g.run()
```
