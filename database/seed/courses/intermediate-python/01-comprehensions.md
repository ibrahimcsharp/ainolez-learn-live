---
title: List and Dict Comprehensions
slug: comprehensions
summary: Build lists, sets and dictionaries in one readable line with comprehensions.
minutes: 8
---
## From loop to comprehension

A very common job is making a new list from an old one. With a loop:

```python
squares = []
for n in range(1, 6):
    squares.append(n * n)
```

A **list comprehension** does the same in one line:

```python tryit
squares = [n * n for n in range(1, 6)]
print(squares)
```

Read it as: "`n * n` for every `n` in `range(1, 6)`".

## Filtering with if

Add an `if` at the end to keep only some items.

```python tryit
numbers = [4, 11, 8, 15, 23, 42]
even = [n for n in numbers if n % 2 == 0]
print(even)

words = ["Python", "is", "fun", "and", "powerful"]
long_words = [w.upper() for w in words if len(w) > 3]
print(long_words)
```

## Dictionary and set comprehensions

Use `{ }` for sets and `{key: value ...}` for dictionaries.

```python tryit
names = ["ana", "ben", "cleo"]
lengths = {name: len(name) for name in names}
print(lengths)

prices = {"tea": 2.5, "cake": 4.0, "water": 1.0}
cheap = {item: p for item, p in prices.items() if p < 3}
print(cheap)

letters = {c for c in "mississippi"}
print(sorted(letters))
```

## When not to use them

Comprehensions are great for short transformations. If you need several steps, nested conditions or side effects such as printing, a normal loop is easier to read.

!!! tip
    If a comprehension no longer fits on one line comfortably, turn it into a loop.

## Summary

- `[expression for item in iterable if condition]` builds a list.
- `{k: v for ...}` builds a dict and `{x for ...}` a set.
- Prefer loops when the logic gets long.

```exercise
{
  "title": "Prices with tax",
  "prompt_md": "Use a **list comprehension** to add 10% tax to every price and round each result to 2 decimals. Print the new list; the output must be exactly `[11.0, 5.5, 2.75]`",
  "starter_code": "prices = [10, 5, 2.5]\n",
  "solution_code": "prices = [10, 5, 2.5]\nprint([round(p * 1.1, 2) for p in prices])",
  "check_type": "output",
  "expected_value": "[11.0, 5.5, 2.75]",
  "hint": "[round(p * 1.1, 2) for p in prices]"
}
```

```quiz
[
  {"question": "What is [x * 2 for x in [1, 2, 3]]?", "options": ["[1, 2, 3, 1, 2, 3]", "[2, 4, 6]", "[2, 3, 4]"], "answer": 1, "explanation": "Each item is multiplied by 2."},
  {"question": "Where does the filter go in a comprehension?", "options": ["At the start", "After the for part", "In a separate line"], "answer": 1, "explanation": "The if comes after for ... in ...."},
  {"question": "Which brackets build a dictionary comprehension?", "options": ["[ ]", "( )", "{ } with key: value"], "answer": 2, "explanation": "{key: value for ...} creates a dict."}
]
```
