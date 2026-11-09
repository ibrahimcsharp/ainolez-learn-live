---
title: Python Tuples and Unpacking
slug: tuples-unpacking
summary: Pack values into tuples, unpack them into names, swap variables, catch the rest with a star and return several values from a function.
minutes: 10
---
## A quick reminder

A **tuple** is an ordered collection that cannot be changed after it is made. You write it with commas, usually inside round brackets.

```python tryit
point = (4, -2)
rgb = 255, 128, 0          # brackets are optional
single = ("only",)         # one item needs a trailing comma
not_a_tuple = ("only")     # this is just a string
print(type(point), type(rgb), type(single), type(not_a_tuple))
```

Tuples use the same indexing and slicing as lists: `rgb[0]`, `rgb[-1]`, `rgb[1:]`.

## Unpacking

**Unpacking** puts each item of a tuple (or list) into its own variable in one line. The number of names must match the number of items.

```python tryit
point = (4, -2)
x, y = point
print("x is", x, "and y is", y)

name, year, rating = ("Spirited Away", 2001, 8.6)
print(f"{name} ({year}) scores {rating}")
```

Too many or too few names gives a `ValueError`.

## Swapping two variables

Packing and unpacking together make swapping a one-liner, with no extra variable.

```python tryit
left = "cat"
right = "dog"
left, right = right, left
print(left, right)
```

## Catching the rest with a star

Put `*` before one name to collect every item that is left over into a **list**.

```python tryit
first, *middle, last = [10, 20, 30, 40, 50]
print(first)
print(middle)
print(last)

head, *tail = "abc"
print(head, tail)
```

Use `_` for values you do not need: `name, _, age = ("Kim", "unused", 30)`.

## Unpacking in a for loop

When a list holds tuples, unpack each one right in the `for` line. This is the same thing that happens with `enumerate()` and `dict.items()`.

```python tryit
results = [("Mo", 12.4), ("Lu", 11.9), ("Jo", 13.1)]
for runner, seconds in results:
    print(f"{runner:>3}: {seconds} s")

for place, (runner, seconds) in enumerate(results, start=1):
    print(place, runner)
```

## Returning several values

A function returns one object, but that object can be a tuple. The caller unpacks it.

```python tryit
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([7, 3, 9, 1, 5])
print("lowest", low, "highest", high)
```

## Tuple methods

Tuples have only two methods, because they cannot change: `count()` and `index()`.

```python tryit
dice = (6, 2, 6, 4, 6)
print(dice.count(6))   # 3
print(dice.index(4))   # 3
```

## Why use a tuple?

- It protects data that should not change, like coordinates or a date.
- It can be a **dictionary key** or go into a set; a list cannot.
- To "change" one, make a new tuple: `point = (point[0] + 1, point[1])`.

```python tryit
distances = {("Paris", "Rome"): 1105, ("Oslo", "Bergen"): 463}
print(distances[("Oslo", "Bergen")])
```

## Summary

- `a, b = pair` unpacks; `a, b = b, a` swaps.
- `first, *rest = items` collects the leftovers into a list.
- Unpack tuples straight in a `for` loop.
- Return a tuple to give back several values.

```exercise
{
  "title": "Split the record",
  "prompt_md": "Each record is `(name, *scores)`. Unpack `record` with a star so that `name` gets the first item and `scores` gets the rest, then print the name and the average score. The output must be `Rina 85.0`.",
  "starter_code": "record = (\"Rina\", 80, 92, 83)\n",
  "solution_code": "record = (\"Rina\", 80, 92, 83)\nname, *scores = record\nprint(name, sum(scores) / len(scores))",
  "check_type": "output",
  "expected_value": "Rina 85.0",
  "hint": "name, *scores = record puts the three numbers in a list called scores."
}
```

```exercise
{
  "title": "Rotate three values",
  "prompt_md": "Move the values one place to the left in a **single** assignment: `a` gets `b`'s value, `b` gets `c`'s and `c` gets `a`'s. Then print `a b c`. The output must be `2 3 1`.",
  "starter_code": "a, b, c = 1, 2, 3\n\nprint(a, b, c)",
  "solution_code": "a, b, c = 1, 2, 3\na, b, c = b, c, a\nprint(a, b, c)",
  "check_type": "output",
  "expected_value": "2 3 1",
  "hint": "The right side is built first: a, b, c = b, c, a"
}
```

```quiz
[
  {"question": "Which of these is a tuple with one item?", "options": ["(5)", "(5,)", "[5]"], "answer": 1, "explanation": "The trailing comma makes the tuple; (5) is just the number 5."},
  {"question": "first, *rest = [1, 2, 3]. What is rest?", "options": ["(2, 3)", "[2, 3]", "3"], "answer": 1, "explanation": "The starred name always collects into a list."},
  {"question": "Why can a tuple be a dictionary key but a list cannot?", "options": ["Tuples are faster", "Tuples cannot change", "Lists are too long"], "answer": 1, "explanation": "Keys must not change, and tuples are immutable."}
]
```
