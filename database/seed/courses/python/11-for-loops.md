---
title: Python For Loops
slug: for-loops
summary: Repeat code for every item in a list, string or range of numbers.
minutes: 8
---
## Looping over a list

A `for` loop runs its block once for every item.

```python tryit
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print("I like", fruit)
```

The variable `fruit` gets the next item each time round.

## range()

`range()` makes a sequence of numbers, which is perfect for counting.

```python tryit
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 11, 2): # start 2, stop before 11, step 2
    print(i, end=" ")
```

## Adding things up

```python tryit
prices = [4.5, 12.0, 3.25]
total = 0
for price in prices:
    total = total + price
print("Total:", total)
```

## enumerate(): the item and its position

```python tryit
players = ["Mia", "Leo", "Zara"]
for position, name in enumerate(players, start=1):
    print(f"{position}. {name}")
```

## break and continue

`break` leaves the loop early; `continue` skips to the next round.

```python tryit
for n in range(1, 10):
    if n == 3:
        continue      # skip 3
    if n == 6:
        break         # stop at 6
    print(n)
```

## Summary

- `for item in collection:` runs once per item.
- `range(start, stop, step)` gives numbers; the stop value is not included.
- `enumerate()` gives positions, `break` stops, `continue` skips.

```exercise
{
  "title": "Times table",
  "prompt_md": "Use a `for` loop with `range()` to print the 3 times table from `3 x 1 = 3` to `3 x 5 = 15`, one line each:\n\n```\n3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15\n```",
  "starter_code": "for i in range(1, 6):\n    pass  # print one line here\n",
  "solution_code": "for i in range(1, 6):\n    print(f\"3 x {i} = {3 * i}\")",
  "check_type": "output",
  "expected_value": "3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15",
  "hint": "Replace pass with print(f\"3 x {i} = {3 * i}\")."
}
```

```quiz
[
  {"question": "Which numbers does range(3) give?", "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3"], "answer": 1, "explanation": "range(3) starts at 0 and stops before 3."},
  {"question": "What does break do?", "options": ["Skips one round", "Stops the loop", "Pauses the program"], "answer": 1, "explanation": "break exits the loop straight away."}
]
```
