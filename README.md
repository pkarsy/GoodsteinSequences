# GoodsteinSequences
A learning tool to help comprehending the marvellous Goodstein Sequences

Anyone how tried to study the Goodstein theorum/sequences knows that the sequence G(3) is very small but on the other hand G(4) in incomprehensibly long. And yet theese huge numbers will start at some point to decrease and inevitably(this is proved) the sequence tertminates at zero.

This tool tries to generate goodstein sequences, skipping trivial steps and optionally show explanations on what is doing, making it more manageable.

One step further step to manageability is that it allows to start with bases other than 2. For example
Goodstein(10,3) ends at base 159
Goodstein(11,3) ends at base 383
Goodstein(12,3) ends at base 2047

By skipping the trivial steps, we can easily see that althoug the bases can grow  seemingly "uncontrollably", the critical point is that the exponents never grow and occassionally shrink for example 5^2 -> 6^2-1 = 5*6^1+5

When the base has maximum exponent = 1 the numbers cannot grow anymore, and after many steps the base becomes larger than the number. From now on the number shrings one by one until reches 0.

Here is the output of
> goodstein 10 3

