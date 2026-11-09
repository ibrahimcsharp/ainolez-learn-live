---
title: How to Add Numbers
slug: add-numbers
summary: Add two numbers typed as text, add up a whole list, avoid the 0.1 + 0.2 surprise, and pull numbers out of a sentence.
minutes: 8
---
## Two numbers from the user

`input()` always gives back **text**. Adding two pieces of text joins them, so convert them to numbers first.

```python
first = input("First number: ")    # the user types 5
second = input("Second number: ")  # the user types 7
print(first + second)              # 57 - text joined together!
print(int(first) + int(second))    # 12
```

Here we pretend the user typed the values, so the example runs without asking:

```python tryit
first = "5"
second = "7"
print(first + second)
print(int(first) + int(second))
print(float("2.5") + float("1.25"))
```

Use `int()` for whole numbers and `float()` when decimals are allowed.

## Handling bad input

If the text is not a number, `int()` raises a `ValueError`. Catch it and explain.

```python tryit
def add_text_numbers(a, b):
    try:
        return float(a) + float(b)
    except ValueError:
        return f"cannot add {a!r} and {b!r}"

print(add_text_numbers("3", "4.5"))
print(add_text_numbers("3", "four"))
```

## Adding up a list

`sum()` adds every number in a list. You can give it a starting value too.

```python tryit
expenses = [12.50, 7.25, 30, 4.75]
print(sum(expenses))
print(sum(expenses, 100))       # start from 100
print(sum(range(1, 101)))       # 1 + 2 + ... + 100
```

## Why 0.1 + 0.2 is not 0.3

Computers store decimals in binary, so some values, like 0.1, are a tiny bit off. Usually this does not matter, but it shows up in comparisons and printed results.

```python tryit
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)

import math
print(round(0.1 + 0.2, 2))
print(math.isclose(0.1 + 0.2, 0.3))   # compare with a tolerance
```

For money, where every cent must be exact, use the `decimal` module and create values from **strings**.

```python tryit
from decimal import Decimal

prices = ["0.10", "0.20", "19.99"]
total = sum(Decimal(p) for p in prices)
print(total)
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
```

`math.fsum()` is another option: it adds a list of floats more accurately than `sum()`.

## Adding the numbers inside a sentence

```python tryit
import re

note = "Bought 3 apples, 12 eggs and 2 loaves for 7.40 in total"
numbers = re.findall(r"\d+(?:\.\d+)?", note)
print(numbers)
print(sum(float(n) for n in numbers))
```

## Adding the digits of a number

```python tryit
number = 90417
print(sum(int(digit) for digit in str(number)))
```

```exercise
{
  "title": "Add numbers from a line of text",
  "prompt_md": "`line` holds numbers separated by spaces, as a user might type them. Split it, convert each part to a `float` and print the total. The output must be `24.5`.",
  "starter_code": "line = \"4 10.5 7 3\"\n",
  "solution_code": "line = \"4 10.5 7 3\"\nprint(sum(float(part) for part in line.split()))",
  "check_type": "output",
  "expected_value": "24.5",
  "hint": "line.split() gives the parts as strings; float(part) converts each one; sum adds them."
}
```

```exercise
{
  "title": "An exact bill",
  "prompt_md": "Add up the prices with `Decimal` so the result is exact, and print it. The output must be `0.60`.",
  "starter_code": "prices = [\"0.10\", \"0.20\", \"0.30\"]\n",
  "solution_code": "from decimal import Decimal\n\nprices = [\"0.10\", \"0.20\", \"0.30\"]\nprint(sum(Decimal(p) for p in prices))",
  "check_type": "output",
  "expected_value": "0.60",
  "hint": "from decimal import Decimal, then sum(Decimal(p) for p in prices)."
}
```

```quiz
[
  {"question": "a = \"2\" and b = \"3\". What is a + b?", "options": ["5", "\"23\"", "an error"], "answer": 1, "explanation": "Both are strings, so + joins them."},
  {"question": "What is the safest way to add up money?", "options": ["float", "int of cents or Decimal from strings", "round() after every step"], "answer": 1, "explanation": "Whole cents or Decimal values made from strings stay exact."}
]
```
