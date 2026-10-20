---
title: Python Iterators
slug: iterators
summary: What a for loop really does - iterables, iter(), next() and writing your own iterator.
minutes: 9
---
## Iterables and iterators

Anything you can loop over is an **iterable**: lists, strings, tuples, dictionaries, ranges, files. To loop, Python asks the iterable for an **iterator** - an object that hands out one item at a time.

```python tryit
colours = ["red", "green", "blue"]
it = iter(colours)     # ask for an iterator
print(next(it))        # red
print(next(it))        # green
print(next(it))        # blue
```

When there are no items left, `next()` raises `StopIteration`.

## What for really does

This loop:

```python
for colour in colours:
    print(colour)
```

works like this:

```python tryit
colours = ["red", "green", "blue"]
it = iter(colours)
while True:
    try:
        colour = next(it)
    except StopIteration:
        break
    print(colour)
```

## An iterator is used up

An iterator remembers where it is. Once it has handed out every item, it is empty.

```python tryit
it = iter([1, 2, 3])
print(list(it))   # [1, 2, 3]
print(list(it))   # []  - already used up
```

A list is not used up: each `for` loop asks it for a fresh iterator.

## Your own iterator

A class becomes an iterator when it has two methods:

- `__iter__()` returns the iterator itself.
- `__next__()` returns the next item, or raises `StopIteration` at the end.

```python tryit
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for n in Countdown(3):
    print(n)
```

!!! tip
    Writing a class is the long way. A generator function with `yield` does the same in a few lines - see the *Intermediate Python* course.

## Handy tools for iterables

```python tryit
names = ["Ana", "Ben", "Cy"]
scores = [90, 75, 82]
for name, score in zip(names, scores):   # walk two lists together
    print(name, score)
print(list(reversed(names)))
print(sorted(scores, reverse=True))
print(any(s > 85 for s in scores), all(s > 70 for s in scores))
```

## Summary

- `iter(x)` gets an iterator; `next(it)` gets the next item.
- `for` calls `next()` until `StopIteration`.
- An iterator is used up after one pass; a list is not.

```exercise
{
  "title": "Take two",
  "prompt_md": "Get an iterator over `queue` with `iter()` and call `next()` twice to print the first two people, one per line. Then print the rest with `list()` on the same iterator. The output must be:\n\n```\nAmy\nBo\n['Cal', 'Dee']\n```",
  "starter_code": "queue = [\"Amy\", \"Bo\", \"Cal\", \"Dee\"]\n",
  "solution_code": "queue = [\"Amy\", \"Bo\", \"Cal\", \"Dee\"]\nit = iter(queue)\nprint(next(it))\nprint(next(it))\nprint(list(it))",
  "check_type": "output",
  "expected_value": "Amy\nBo\n['Cal', 'Dee']",
  "hint": "it = iter(queue), then next(it) twice, then list(it) for what is left."
}
```

```quiz
[
  {"question": "Which error tells a for loop to stop?", "options": ["IndexError", "StopIteration", "EndOfLoop"], "answer": 1, "explanation": "next() raises StopIteration when the iterator is empty."},
  {"question": "Which two methods make a class an iterator?", "options": ["__iter__ and __next__", "__init__ and __next__", "__loop__ and __step__"], "answer": 0, "explanation": "__iter__ returns the iterator, __next__ returns each item."},
  {"question": "it = iter([1, 2]); list(it); what is list(it) the second time?", "options": ["[1, 2]", "[]", "an error"], "answer": 1, "explanation": "The iterator is already used up."}
]
```
