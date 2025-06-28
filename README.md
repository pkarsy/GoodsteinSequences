# GoodsteinSequences
A learning tool to help comprehending the enormous Goodstein Sequences

Anyone how tried to study the Goodstein theorum/sequences knows that the sequence G(3) is very small but on the other hand G(4) in incomprehensibly long. And yet theese huge numbers will start at some point to decrease and inevitably(this is proved) the sequence terminates at zero.

The simplification cosists of:
- skip trivial repeated steps making it more manageable.
- showing explanations on what it is doing
- allows to start with bases other than 2. For example

Goodstein(10,3) ends at base 159
Goodstein(11,3) ends at base 383
Goodstein(12,3) ends at base 2047

we can easily see that althoug the bases can grow  seemingly "uncontrollably", the critical point is that the exponents never grow and occassionally shrink for example 5^2 -> 6^2-1 = 5*6^1+5

When the number has the form 1*base+const  the numbers cannot grow anymore, and after many steps the base becomes larger than the number itself. From now on the number shrings one by one until reaches 0.

Here is the output of
> python goodstein.py 10 3

```
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

