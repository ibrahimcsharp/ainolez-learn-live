---
title: Python range()
slug: range
summary: Count with range(start, stop, step), count backwards, and loop with positions.
minutes: 7
---
## Counting from 0

`range(n)` gives the numbers `0, 1, ..., n-1`. It is the usual way to repeat something `n` times.

```python tryit
for i in range(5):
    print(i)
```

`range(5)` has 5 numbers but stops **before** 5.

## Start and stop

`range(start, stop)` starts at `start` and stops before `stop`.

```python tryit
for year in range(2020, 2025):
    print(year)
```

## Step

A third number sets the step. A negative step counts backwards.

```python tryit
print(list(range(0, 21, 5)))    # [0, 5, 10, 15, 20]
print(list(range(10, 0, -2)))   # [10, 8, 6, 4, 2]
for n in range(3, 0, -1):
    print(n, "...")
print("Lift off!")
```

`list(range(...))` shows all the numbers at once.

## range is lazy

A range does not store all its numbers; it works them out when asked. `range(1_000_000_000)` uses almost no memory. You can still ask for its length, index it or test membership.

```python tryit
big = range(0, 1_000_000_000, 3)
print(len(big))
print(big[10])
print(999 in big)
```

## Positions with enumerate()

To get the position and the value of each item, use `enumerate()` instead of `range(len(...))`.

```python tryit
names = ["Ada", "Linus", "Grace"]
for position, name in enumerate(names, start=1):
    print(position, name)
```

## Summary

- `range(stop)`, `range(start, stop)` and `range(start, stop, step)` count up to, but not including, `stop`.
- A negative step counts down.
- Use `enumerate()` when you need positions and values together.

```exercise
{
  "title": "Times table",
  "prompt_md": "Use `range()` to print the 7 times table from 1 to 5, one line each, like `7 x 1 = 7`. The output must be:\n\n```\n7 x 1 = 7\n7 x 2 = 14\n7 x 3 = 21\n7 x 4 = 28\n7 x 5 = 35\n```",
  "starter_code": "n = 7\n",
  "solution_code": "n = 7\nfor i in range(1, 6):\n    print(f\"{n} x {i} = {n * i}\")",
  "check_type": "output",
  "expected_value": "7 x 1 = 7\n7 x 2 = 14\n7 x 3 = 21\n7 x 4 = 28\n7 x 5 = 35",
  "hint": "range(1, 6) gives 1 to 5."
}
```

```quiz
[
  {"question": "What is the last number of range(2, 8)?", "options": ["8", "7", "6"], "answer": 1, "explanation": "range stops before the stop value."},
  {"question": "What does list(range(10, 0, -3)) give?", "options": ["[10, 7, 4, 1]", "[10, 7, 4]", "[]"], "answer": 0, "explanation": "It counts down by 3 and stops before 0."},
  {"question": "What does enumerate([\"a\", \"b\"]) give in a loop?", "options": ["only positions", "pairs of position and item", "only items"], "answer": 1, "explanation": "Each step gives (position, item)."}
]
```
