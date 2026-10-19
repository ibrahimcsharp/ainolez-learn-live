---
title: Iterators and Generators
slug: generators
summary: Understand how for loops work and produce values lazily with generators and yield.
minutes: 9
---
## How a for loop really works

A `for` loop asks an object for an **iterator** and calls `next()` on it until it is empty.

```python tryit
colors = ["red", "green", "blue"]
it = iter(colors)
print(next(it))
print(next(it))
print(next(it))
# one more next(it) would raise StopIteration
```

## Generators with yield

A function with `yield` becomes a **generator**. Each `yield` hands out one value and pauses the function until the next value is asked for.

```python tryit
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for number in countdown(3):
    print(number)

print(list(countdown(5)))
```

## Why generators? Memory.

A list holds every value at once. A generator makes values one by one, so it can handle huge or even endless sequences.

```python tryit
def even_numbers():
    n = 0
    while True:           # endless, but only computed on demand
        yield n
        n += 2

gen = even_numbers()
print([next(gen) for _ in range(5)])
```

## Generator expressions

Like a list comprehension, but with round brackets. Nothing is computed until it is used.

```python tryit
total = sum(n * n for n in range(1_000_000))
print(total)
```

This adds up a million squares without ever building a list of a million numbers.

## Chaining steps

Generators fit together like a pipeline:

```python tryit
lines = ["  apple ", "", "banana", "  ", "cherry  "]

cleaned = (line.strip() for line in lines)
non_empty = (line for line in cleaned if line)
print(list(non_empty))
```

## Summary

- `iter()` and `next()` are what `for` uses under the hood.
- `yield` makes a generator that produces values lazily.
- `(x for x in ...)` is a generator expression: memory-friendly.

```exercise
{
  "title": "A squares generator",
  "prompt_md": "Write a generator `squares(n)` that yields `1*1`, `2*2`, ... up to `n*n`. The program prints `list(squares(4))`, which must show exactly `[1, 4, 9, 16]`",
  "starter_code": "def squares(n):\n    pass\n\nprint(list(squares(4)))",
  "solution_code": "def squares(n):\n    for i in range(1, n + 1):\n        yield i * i\n\nprint(list(squares(4)))",
  "check_type": "output",
  "expected_value": "[1, 4, 9, 16]",
  "hint": "Loop i from 1 to n and yield i * i."
}
```

```quiz
[
  {"question": "What turns a function into a generator?", "options": ["return", "yield", "async"], "answer": 1, "explanation": "Any function with yield is a generator function."},
  {"question": "Why use a generator instead of a list?", "options": ["Values are produced one at a time, saving memory", "Generators are always sorted", "Lists cannot hold numbers"], "answer": 0, "explanation": "Generators are lazy: they do not store every value."}
]
```
