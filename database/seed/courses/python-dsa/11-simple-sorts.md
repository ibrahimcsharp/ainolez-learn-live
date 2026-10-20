---
title: Bubble, Selection and Insertion Sort
slug: simple-sorts
summary: Three simple O(n²) sorting algorithms, how they work step by step, and when they are useful.
minutes: 11
---
## Why learn sorting?

Python's `sorted()` is excellent, and you should use it in real code. But writing sorts yourself teaches the core ideas of algorithms: loops inside loops, swapping, invariants and Big O.

All three sorts here are **O(n²)**: fine for small lists, slow for big ones.

## Bubble sort

Walk through the list comparing neighbours; swap them if they are in the wrong order. After each pass the largest remaining value has "bubbled" to the end.

```python tryit
def bubble_sort(items):
    items = items[:]                          # don't change the caller's list
    n = len(items)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        print(items)
        if not swapped:                       # already sorted: stop early
            break
    return items

print(bubble_sort([5, 1, 4, 2, 8]))
```

## Selection sort

Find the smallest value in the unsorted part and swap it to the front. Repeat for the rest.

```python tryit
def selection_sort(items):
    items = items[:]
    for start in range(len(items) - 1):
        smallest = start
        for i in range(start + 1, len(items)):
            if items[i] < items[smallest]:
                smallest = i
        items[start], items[smallest] = items[smallest], items[start]
        print(items)
    return items

print(selection_sort([29, 10, 14, 37, 13]))
```

Selection sort always makes the same number of comparisons, but very few swaps.

## Insertion sort

Take the next value and slide it left into its place among the already-sorted values - like sorting playing cards in your hand.

```python tryit
def insertion_sort(items):
    items = items[:]
    for i in range(1, len(items)):
        value = items[i]
        j = i - 1
        while j >= 0 and items[j] > value:
            items[j + 1] = items[j]          # shift right
            j -= 1
        items[j + 1] = value
        print(items)
    return items

print(insertion_sort([12, 11, 13, 5, 6]))
```

Insertion sort is very fast on lists that are **almost sorted** - close to O(n). That is why Python's own sort uses it for small pieces.

## Comparing them

```python tryit
import random
import time

def bubble(a):
    a = a[:]
    for end in range(len(a) - 1, 0, -1):
        for i in range(end):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
    return a

def insertion(a):
    a = a[:]
    for i in range(1, len(a)):
        v, j = a[i], i - 1
        while j >= 0 and a[j] > v:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = v
    return a

data = [random.randint(0, 10_000) for _ in range(2_000)]
for sort in (bubble, insertion, sorted):
    start = time.perf_counter()
    result = sort(data)
    print(f"{sort.__name__:<10}{time.perf_counter() - start:.3f}s  correct={result == sorted(data)}")
```

## Summary

| Sort | Idea | Best | Worst |
|---|---|---|---|
| Bubble | swap neighbours, largest bubbles to the end | O(n) with early stop | O(n²) |
| Selection | pick the smallest, put it in front | O(n²) | O(n²) |
| Insertion | slide each value into the sorted part | O(n) | O(n²) |

```exercise
{
  "title": "Sort descending",
  "prompt_md": "Change insertion sort so it sorts from **largest to smallest**, and print the result. The output must be `[9, 7, 4, 3, 1]`.",
  "starter_code": "items = [4, 9, 1, 7, 3]\nfor i in range(1, len(items)):\n    value = items[i]\n    j = i - 1\n    while j >= 0 and items[j] > value:\n        items[j + 1] = items[j]\n        j -= 1\n    items[j + 1] = value\nprint(items)\n",
  "solution_code": "items = [4, 9, 1, 7, 3]\nfor i in range(1, len(items)):\n    value = items[i]\n    j = i - 1\n    while j >= 0 and items[j] < value:\n        items[j + 1] = items[j]\n        j -= 1\n    items[j + 1] = value\nprint(items)\n",
  "check_type": "output",
  "expected_value": "[9, 7, 4, 3, 1]",
  "hint": "Only one character changes: the comparison in the while line."
}
```

```quiz
[
  {"question": "After the first pass of bubble sort, where is the largest value?", "options": ["At the start", "At the end", "In the middle"], "answer": 1, "explanation": "It bubbles all the way to the end."},
  {"question": "Which sort is fastest on an almost-sorted list?", "options": ["Selection sort", "Insertion sort"], "answer": 1, "explanation": "Each value only slides a short way."},
  {"question": "What is the worst-case Big O of these three sorts?", "options": ["O(n log n)", "O(n²)", "O(n)"], "answer": 1, "explanation": "They compare values in nested loops."}
]
```
