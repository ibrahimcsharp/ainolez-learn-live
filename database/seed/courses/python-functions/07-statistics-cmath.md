---
title: Python statistics and cmath Modules
slug: statistics-cmath
summary: Describe data with mean, median, mode and spread using the statistics module, and calculate with complex numbers using cmath.
minutes: 11
---
## The statistics module

For quick facts about a list of numbers you do not need pandas. The built-in `statistics` module has the common measures.

```python tryit
import statistics as st

sleep_hours = [7, 6.5, 8, 5, 7, 9, 7]

print("mean:  ", round(st.mean(sleep_hours), 2))
print("median:", st.median(sleep_hours))
print("mode:  ", st.mode(sleep_hours))
```

- **mean**: the average - add everything up and divide by how many there are.
- **median**: the middle value once the numbers are sorted. With an even count it is the average of the two middle values.
- **mode**: the value that appears most often.

## Mean or median?

One extreme value pulls the mean a long way but barely moves the median. That is why reports on income or house prices usually give the median.

```python tryit
import statistics as st

salaries = [31_000, 34_000, 35_000, 38_000, 41_000]
print(st.mean(salaries), st.median(salaries))

salaries.append(900_000)      # one very high earner joins
print(round(st.mean(salaries)), st.median(salaries))
```

## More than one mode

`mode()` returns the first most common value it meets. `multimode()` returns all of them.

```python tryit
import statistics as st

shoe_sizes = [40, 42, 38, 42, 40, 44]
print(st.mode(shoe_sizes))
print(st.multimode(shoe_sizes))
```

## How spread out is the data?

Two classes can have the same average but very different results. The **standard deviation** measures how far values typically sit from the mean; the **variance** is its square.

```python tryit
import statistics as st

class_a = [68, 70, 71, 69, 72]
class_b = [40, 95, 60, 88, 67]

for name, marks in [("A", class_a), ("B", class_b)]:
    print(name, "mean", st.mean(marks), "stdev", round(st.stdev(marks), 1))
```

`stdev` and `variance` treat the numbers as a **sample** of a bigger group; `pstdev` and `pvariance` treat them as the **whole** population. With small lists the sample versions give slightly larger values.

## Other helpers

```python tryit
import statistics as st

data = [3, 9, 4, 12, 7, 5, 10, 8]
print(st.median_low(data), st.median_high(data))
print(st.quantiles(data, n=4))   # the three cut points between quarters
print(st.fmean([1.5, 2.5, 3.5])) # fast mean, always a float
```

## Complex numbers

A **complex number** has a real part and an imaginary part. Python writes the imaginary unit as `j`, as engineers do. They appear in electronics, signal processing and some maths problems.

```python tryit
z = 3 + 4j
print(type(z))
print(z.real, z.imag)
print(abs(z))           # its length: 5.0
print(z * (1 - 2j))
print(z.conjugate())
```

Complex numbers are built in; you only need a module for maths functions on them.

## The cmath module

`math.sqrt(-4)` raises an error, because the answer is not a real number. `cmath` has the same functions as `math`, but works with complex numbers.

```python tryit
import cmath
import math

try:
    math.sqrt(-4)
except ValueError as error:
    print("math:", error)

print("cmath:", cmath.sqrt(-4))

z = 1 + 1j
print(cmath.phase(z))           # angle in radians
print(math.degrees(cmath.phase(z)))
print(cmath.polar(z))           # (length, angle)
print(cmath.rect(2, math.pi / 2))
```

## Solving any quadratic equation

With `cmath`, the quadratic formula works even when the answers are complex.

```python tryit
import cmath

def solve(a, b, c):
    root = cmath.sqrt(b * b - 4 * a * c)
    return (-b + root) / (2 * a), (-b - root) / (2 * a)

print(solve(1, -3, 2))   # real answers: 2 and 1
print(solve(1, 2, 5))    # complex answers
```

## Summary

- `statistics`: `mean`, `median`, `mode`, `multimode`, `stdev`, `variance`, `quantiles`.
- The median resists outliers better than the mean.
- Complex numbers use `j`: `3 + 4j`; `.real`, `.imag` and `abs()` work on them.
- `cmath` is `math` for complex numbers: `cmath.sqrt(-1)` is `1j`.

```exercise
{
  "title": "Describe the delivery times",
  "prompt_md": "Use the `statistics` module to print the mean, the median and the mode of `minutes`, each on its own line. The output must be:\n\n```\n31\n30.0\n28\n```",
  "starter_code": "minutes = [28, 35, 28, 41, 32, 22]\n",
  "solution_code": "import statistics\n\nminutes = [28, 35, 28, 41, 32, 22]\nprint(statistics.mean(minutes))\nprint(statistics.median(minutes))\nprint(statistics.mode(minutes))",
  "check_type": "output",
  "expected_value": "31\n30.0\n28",
  "hint": "import statistics, then statistics.mean(...), statistics.median(...) and statistics.mode(...)."
}
```

```exercise
{
  "title": "Square root of a negative",
  "prompt_md": "Use `cmath` to print the square root of `-9`, then the length (`abs`) of the complex number `6 + 8j`. The output must be:\n\n```\n3j\n10.0\n```",
  "starter_code": "import cmath\n",
  "solution_code": "import cmath\n\nprint(cmath.sqrt(-9))\nprint(abs(6 + 8j))",
  "check_type": "output",
  "expected_value": "3j\n10.0",
  "hint": "cmath.sqrt(-9) gives 3j; abs() of a complex number is its length."
}
```

```quiz
[
  {"question": "What is the median of [1, 3, 100]?", "options": ["34.67", "3", "100"], "answer": 1, "explanation": "The median is the middle value of the sorted list."},
  {"question": "Which measure is least affected by one huge value?", "options": ["mean", "median"], "answer": 1, "explanation": "The median only looks at the middle, so outliers barely move it."},
  {"question": "How does Python write the imaginary unit?", "options": ["i", "j", "im"], "answer": 1, "explanation": "Python uses j, for example 2 + 3j."},
  {"question": "Which call works for a negative number?", "options": ["math.sqrt(-1)", "cmath.sqrt(-1)"], "answer": 1, "explanation": "cmath returns 1j; math raises ValueError."}
]
```
