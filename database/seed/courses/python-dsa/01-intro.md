---
title: Data Structures, Algorithms and Big O
slug: intro
summary: What data structures and algorithms are, and how Big O notation describes speed.
minutes: 9
---
## Two key ideas

- A **data structure** is a way to organise data so it is easy to use: a list, a dictionary, a tree.
- An **algorithm** is a precise list of steps that solves a problem: find the biggest number, sort a list, find the shortest route.

The right choice can make a program thousands of times faster.

## The same problem, two algorithms

Is there a duplicate in the list? Here are two ways to find out.

```python tryit
def has_duplicate_slow(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):   # compare every pair
            if items[i] == items[j]:
                return True
    return False

def has_duplicate_fast(items):
    seen = set()
    for item in items:                       # look at each item once
        if item in seen:
            return True
        seen.add(item)
    return False

data = [4, 8, 15, 16, 23, 42, 8]
print(has_duplicate_slow(data), has_duplicate_fast(data))
```

Both are correct. But for 10,000 items the slow one makes about 50 million comparisons, the fast one about 10,000 steps.

## Counting steps

We describe speed by how the number of steps **grows** as the input size `n` grows. That is **Big O** notation.

```python tryit
import time

def count_pairs(n):
    steps = 0
    for i in range(n):
        for j in range(n):
            steps += 1
    return steps

for n in [10, 100, 1000]:
    start = time.perf_counter()
    steps = count_pairs(n)
    print(f"n={n:<5} steps={steps:<8} time={time.perf_counter() - start:.4f}s")
```

Ten times more input gives a hundred times more steps: that is **O(n²)**.

## Common Big O classes

| Big O | Name | Example | 1,000 items |
|---|---|---|---|
| O(1) | constant | read `items[5]`, look up a dict key | 1 step |
| O(log n) | logarithmic | binary search | ~10 steps |
| O(n) | linear | loop once over a list | 1,000 steps |
| O(n log n) | linearithmic | merge sort, Python's `sorted()` | ~10,000 steps |
| O(n²) | quadratic | compare every pair | 1,000,000 steps |

Big O ignores small details and constant factors; it tells you what happens when the data gets big.

## Time and memory

Algorithms also use memory (space). The fast duplicate check above uses O(n) extra memory for the `set`; the slow one uses O(1). Often you trade memory for speed.

## Summary

- Data structures organise data; algorithms are step-by-step solutions.
- Big O describes how the work grows with the input size.
- O(1) < O(log n) < O(n) < O(n log n) < O(n²).

```exercise
{
  "title": "Count the steps",
  "prompt_md": "Count how many times the inner line runs for `n = 6` and print the count. The output must be `15` (every pair `i < j`).",
  "starter_code": "n = 6\nsteps = 0\nfor i in range(n):\n    for j in range(i + 1, n):\n        pass  # count this step\n",
  "solution_code": "n = 6\nsteps = 0\nfor i in range(n):\n    for j in range(i + 1, n):\n        steps += 1\nprint(steps)",
  "check_type": "output",
  "expected_value": "15",
  "hint": "Replace pass with steps += 1 and print steps after the loops."
}
```

```quiz
[
  {"question": "What is the Big O of looking up a key in a dict?", "options": ["O(1)", "O(n)", "O(n²)"], "answer": 0, "explanation": "Dicts use hashing, so lookups take about one step."},
  {"question": "Two nested loops over the same list are usually...", "options": ["O(n)", "O(log n)", "O(n²)"], "answer": 2, "explanation": "n times n steps."},
  {"question": "Which grows slowest?", "options": ["O(n)", "O(log n)", "O(n log n)"], "answer": 1, "explanation": "log n grows very slowly: about 20 for a million items."}
]
```
