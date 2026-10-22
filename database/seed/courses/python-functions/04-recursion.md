---
title: Python Recursion
slug: recursion
summary: Functions that call themselves - the base case, the recursive step, walking nested data, and the limits of recursion.
minutes: 11
---
## A function that calls itself

A **recursive** function solves a problem by calling itself on a **smaller** version of the same problem. Every recursive function needs two parts:

1. a **base case**: a version so small that the answer is known straight away, so the function stops calling itself;
2. a **recursive step**: make the problem smaller and call the function again.

```python tryit
def countdown(n):
    if n == 0:              # base case
        print("Lift off!")
        return
    print(n)
    countdown(n - 1)        # recursive step: a smaller problem

countdown(3)
```

Without a base case the function would call itself forever.

## Returning values

Most recursive functions combine the answer of the smaller problem with one more step. Here, the sum of the digits of 4721 is the last digit, 1, plus the sum of the digits of 472.

```python tryit
def digit_sum(n):
    if n < 10:                          # one digit: the answer is n
        return n
    return n % 10 + digit_sum(n // 10)  # last digit + the rest

print(digit_sum(4721))   # 4 + 7 + 2 + 1 = 14
```

It helps to trace the calls by hand:

```
digit_sum(4721) = 1 + digit_sum(472)
digit_sum(472)  = 2 + digit_sum(47)
digit_sum(47)   = 7 + digit_sum(4)
digit_sum(4)    = 4                  <- base case
```

Then the answers travel back up: 4, 11, 13, 14.

## Seeing the calls

Printing with indentation shows how calls go down and come back.

```python tryit
def power(base, exp, depth=0):
    pad = "  " * depth
    print(f"{pad}power({base}, {exp})")
    if exp == 0:
        return 1
    result = base * power(base, exp - 1, depth + 1)
    print(f"{pad}-> {result}")
    return result

power(3, 3)
```

## Where recursion fits best: nested data

Recursion is natural when data contains smaller copies of itself, such as lists inside lists or folders inside folders. A loop alone does not know how deep to go.

```python tryit
def count_items(things):
    total = 0
    for thing in things:
        if isinstance(thing, list):
            total += count_items(thing)   # a smaller list: recurse
        else:
            total += 1
    return total

boxes = ["pen", ["cup", ["spoon", "fork"], "plate"], [], "lamp"]
print(count_items(boxes))   # 6
```

```python tryit
folders = {
    "docs": {"cv.pdf": 120, "letters": {"a.txt": 3, "b.txt": 5}},
    "photo.jpg": 2400,
}

def total_size(tree):
    size = 0
    for name, value in tree.items():
        if isinstance(value, dict):
            size += total_size(value)
        else:
            size += value
    return size

print(total_size(folders), "KB")
```

## Limits and loops

Each call waits in memory until the calls below it finish. Python stops very deep recursion with a `RecursionError` (by default after about 1000 levels).

```python tryit
import sys

def depth(n):
    return depth(n + 1)

print("limit:", sys.getrecursionlimit())
try:
    depth(0)
except RecursionError:
    print("RecursionError: too deep")
```

For simple counting, a loop is usually clearer and faster. Some recursive functions also repeat the same work many times; the classic example is Fibonacci numbers, which you can speed up by remembering answers with `functools.cache`.

```python tryit
from functools import cache

@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])
print(fib(80))   # instant thanks to the cache
```

## Summary

- A recursive function calls itself on a smaller problem.
- It always needs a base case that stops the calls.
- Recursion is a good fit for nested data like trees and folders.
- Very deep recursion raises `RecursionError`; use a loop when a loop is simpler.

```exercise
{
  "title": "Reverse with recursion",
  "prompt_md": "Write a **recursive** `reverse(text)`: an empty string reverses to itself, otherwise the answer is the reverse of everything after the first character, followed by the first character. The code below must print `nohtyp`.",
  "starter_code": "def reverse(text):\n    pass\n\nprint(reverse(\"python\"))",
  "solution_code": "def reverse(text):\n    if text == \"\":\n        return \"\"\n    return reverse(text[1:]) + text[0]\n\nprint(reverse(\"python\"))",
  "check_type": "output",
  "expected_value": "nohtyp",
  "hint": "Base case: if text == \"\": return \"\". Recursive step: return reverse(text[1:]) + text[0]."
}
```

```exercise
{
  "title": "Flatten a nested list",
  "prompt_md": "Write a recursive `flatten(items)` that returns one flat list of all the numbers, however deeply they are nested. The code below must print `[1, 2, 3, 4, 5, 6]`.",
  "starter_code": "def flatten(items):\n    pass\n\nprint(flatten([1, [2, [3, 4]], [[5]], 6]))",
  "solution_code": "def flatten(items):\n    flat = []\n    for item in items:\n        if isinstance(item, list):\n            flat.extend(flatten(item))\n        else:\n            flat.append(item)\n    return flat\n\nprint(flatten([1, [2, [3, 4]], [[5]], 6]))",
  "check_type": "output",
  "expected_value": "[1, 2, 3, 4, 5, 6]",
  "hint": "Loop over the items. If an item is a list, extend with flatten(item); otherwise append it."
}
```

```quiz
[
  {"question": "What stops a recursive function from calling itself forever?", "options": ["The return keyword", "The base case", "The for loop"], "answer": 1, "explanation": "The base case answers the smallest problem without another call."},
  {"question": "What happens when recursion goes far too deep?", "options": ["Python slows down but finishes", "A RecursionError is raised", "It switches to a loop"], "answer": 1, "explanation": "Python stops deep recursion with RecursionError."},
  {"question": "Which kind of data suits recursion best?", "options": ["A flat list of numbers", "Nested data, like folders inside folders", "A single string"], "answer": 1, "explanation": "Recursion follows nested structures to any depth."}
]
```
