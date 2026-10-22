---
title: How to Check Numbers - Even, Prime, Leap Year
slug: number-checks
summary: Small yes-or-no checks on numbers - even or odd, divisible, prime, leap year and perfect square - written as reusable functions.
minutes: 9
---
## Even or odd

The remainder after dividing by 2 tells you: `0` means even, `1` means odd.

```python tryit
for n in [4, 7, 0, -3]:
    print(n, "even" if n % 2 == 0 else "odd")
```

The same idea checks any divisor: `n % 5 == 0` means `n` is a multiple of 5.

## Check functions return a bool

Write each check as a function that **returns** `True` or `False`. Then it reads naturally inside `if` and works with `filter`, `any` and `all`.

```python tryit
def is_even(n):
    return n % 2 == 0

numbers = [3, 8, 15, 22, 41]
print([n for n in numbers if is_even(n)])
print(any(is_even(n) for n in numbers))
```

Write `return n % 2 == 0`, not `if n % 2 == 0: return True else: return False`. The comparison already is a bool.

## Prime numbers

A **prime** is a whole number above 1 that can only be divided evenly by 1 and itself. To check `n`, try the divisors from 2 upwards. You can stop at the square root of `n`: if `n` had a bigger divisor, it would also have a smaller partner below the square root.

```python tryit
import math

def is_prime(n):
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            return False
    return True

print([n for n in range(30) if is_prime(n)])
print(is_prime(7919))
```

`math.isqrt(n)` is the whole-number square root, so `range` gets an `int`.

## Leap years

A year is a leap year when it divides by 4, except century years, which must also divide by 400. So 2024 and 2000 are leap years, but 1900 is not.

```python tryit
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

for year in [2024, 2023, 1900, 2000]:
    print(year, is_leap(year))

import calendar
print(calendar.isleap(1900))   # the standard library agrees
```

## Perfect squares

```python tryit
import math

def is_square(n):
    return n >= 0 and math.isqrt(n) ** 2 == n

print([n for n in range(50) if is_square(n)])
```

Using `math.isqrt` avoids float rounding errors that `n ** 0.5` can have with very big numbers.

## Factors of a number

```python tryit
def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

print(factors(36))
print(len(factors(13)) == 2)   # a prime has exactly two factors
```

```exercise
{
  "title": "Primes in a range",
  "prompt_md": "Write `is_prime(n)` and use it to print the prime numbers from 40 to 60 as a list. The output must be `[41, 43, 47, 53, 59]`.",
  "starter_code": "def is_prime(n):\n    pass\n\n",
  "solution_code": "import math\n\ndef is_prime(n):\n    if n < 2:\n        return False\n    for d in range(2, math.isqrt(n) + 1):\n        if n % d == 0:\n            return False\n    return True\n\nprint([n for n in range(40, 61) if is_prime(n)])",
  "check_type": "output",
  "expected_value": "[41, 43, 47, 53, 59]",
  "hint": "Return False as soon as a divisor from 2 up to the square root divides n evenly; return True after the loop."
}
```

```exercise
{
  "title": "Count the leap years",
  "prompt_md": "Write `is_leap(year)` with the rule from this lesson and print how many leap years there are from 1890 to 2030, both included. The output must be `34`.",
  "starter_code": "def is_leap(year):\n    pass\n\n",
  "solution_code": "def is_leap(year):\n    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n\nprint(sum(1 for year in range(1890, 2031) if is_leap(year)))",
  "check_type": "output",
  "expected_value": "34",
  "hint": "Divisible by 4, and either not by 100 or by 400. Count with sum(1 for year in range(1890, 2031) if is_leap(year))."
}
```

```quiz
[
  {"question": "Which expression is True when n is odd?", "options": ["n % 2 == 0", "n % 2 == 1", "n / 2 == 1"], "answer": 1, "explanation": "An odd number leaves a remainder of 1 when divided by 2 (for positive n)."},
  {"question": "Is 1900 a leap year?", "options": ["Yes", "No"], "answer": 1, "explanation": "It is a century year that does not divide by 400."},
  {"question": "To test if n is prime, you only need to try divisors up to...", "options": ["n / 2", "the square root of n", "10"], "answer": 1, "explanation": "Any divisor above the square root has a partner below it."}
]
```
