---
title: Lists and Arrays
slug: lists-arrays
summary: How Python lists work underneath, which operations are fast or slow, and when to use array.
minutes: 8
---
## A list is a dynamic array

Most languages have **arrays**: a row of memory slots, one after another, each found by its index. A Python list is a *dynamic array*: it grows automatically when you add items.

Because the slots are in a row, Python can jump straight to any index.

```python tryit
temps = [18, 21, 19, 25, 23]
print(temps[3])       # O(1): jump straight to slot 3
temps[3] = 24         # O(1): overwrite it
print(temps)
```

## Fast and slow operations

| Operation | Big O | Why |
|---|---|---|
| `lst[i]`, `lst[i] = x` | O(1) | jump to the slot |
| `lst.append(x)`, `lst.pop()` | O(1) | work at the end |
| `lst.insert(0, x)`, `lst.pop(0)` | O(n) | every item moves one slot |
| `x in lst`, `lst.index(x)` | O(n) | check items one by one |
| `lst.sort()` | O(n log n) | Timsort |

```python tryit
import time

for n in [10_000, 20_000]:
    items = []
    start = time.perf_counter()
    for i in range(n):
        items.insert(0, i)     # slow: shifts everything
    front = time.perf_counter() - start

    items = []
    start = time.perf_counter()
    for i in range(n):
        items.append(i)        # fast
    back = time.perf_counter() - start
    print(f"n={n}: insert at front {front:.3f}s, append {back:.4f}s")
```

## Common array algorithms

Many problems are solved with one pass over an array.

```python tryit
def find_max(numbers):
    biggest = numbers[0]
    for n in numbers[1:]:
        if n > biggest:
            biggest = n
    return biggest

def reverse_in_place(items):
    left, right = 0, len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1

data = [7, 3, 9, 1, 8]
print(find_max(data))
reverse_in_place(data)
print(data)
```

The second function uses **two pointers** moving towards each other - a technique you will see often.

## The array module

When every item is the same kind of number, `array.array` stores them more compactly than a list.

```python tryit
from array import array

readings = array("i", [12, 15, 11, 19])   # "i" = signed integers
readings.append(14)
print(readings, sum(readings))
```

For maths on large arrays, the NumPy library is far faster - see the *Python for Data Analysis* course.

## Summary

- A list is a dynamic array: index access and appending are O(1).
- Inserting or removing at the front, and searching, are O(n).
- Two pointers is a common pattern for working through an array.

```exercise
{
  "title": "Running total",
  "prompt_md": "Build a new list where each item is the sum of all numbers up to that position, in one pass. Print it. The output must be `[3, 4, 8, 9, 14]`.",
  "starter_code": "numbers = [3, 1, 4, 1, 5]\n",
  "solution_code": "numbers = [3, 1, 4, 1, 5]\ntotals = []\nrunning = 0\nfor n in numbers:\n    running += n\n    totals.append(running)\nprint(totals)",
  "check_type": "output",
  "expected_value": "[3, 4, 8, 9, 14]",
  "hint": "Keep a running sum; after adding each number, append the sum to a new list."
}
```

```quiz
[
  {"question": "What is the Big O of lst[1000]?", "options": ["O(1)", "O(n)", "O(log n)"], "answer": 0, "explanation": "Index access jumps straight to the slot."},
  {"question": "Why is lst.insert(0, x) slow for big lists?", "options": ["It sorts the list", "Every item must move one slot", "It copies the list twice"], "answer": 1, "explanation": "Inserting at the front shifts all items."},
  {"question": "What is the Big O of x in lst?", "options": ["O(1)", "O(n)", "O(n²)"], "answer": 1, "explanation": "Python checks the items one by one."}
]
```
