---
title: Merge Sort, Quick Sort and Counting Sort
slug: fast-sorts
summary: Divide and conquer with merge and quick sort, sorting without comparisons, and how sorted() works.
minutes: 12
---
## Divide and conquer

The fast sorts split the problem into smaller pieces, solve each piece, and combine the answers. This is called **divide and conquer**, and it gives **O(n log n)**: for a million items, about 20 million steps instead of a trillion.

## Merge sort

1. Split the list in half.
2. Sort each half (recursively).
3. **Merge** the two sorted halves by repeatedly taking the smaller front item.

```python tryit
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]

def merge_sort(items):
    if len(items) <= 1:              # base case
        return items
    middle = len(items) // 2
    return merge(merge_sort(items[:middle]), merge_sort(items[middle:]))

print(merge([1, 4, 9], [2, 3, 10]))
print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
```

Merge sort is always O(n log n) and **stable** (equal items keep their order), but it needs extra memory for the merged lists.

## Quick sort

1. Pick a **pivot** value.
2. Split the list into values smaller than, equal to and larger than the pivot.
3. Sort the smaller and larger parts (recursively) and join them.

```python tryit
def quick_sort(items):
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]
    smaller = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    larger = [x for x in items if x > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)

print(quick_sort([33, 10, 55, 71, 29, 3, 18, 42]))
```

Quick sort is O(n log n) on average and very fast in practice. With an unlucky pivot every time it degrades to O(n²); picking the middle or a random pivot makes that rare. Real implementations split the list in place to save memory.

## Counting sort: no comparisons

When values are small whole numbers, you can count how many times each appears and write them out in order. Big O: **O(n + k)**, where k is the largest value.

```python tryit
def counting_sort(items, max_value):
    counts = [0] * (max_value + 1)
    for x in items:
        counts[x] += 1
    result = []
    for value, count in enumerate(counts):
        result.extend([value] * count)
    return result

dice = [3, 6, 1, 3, 2, 6, 6, 4, 1, 5]
print(counting_sort(dice, 6))
```

**Radix sort** extends this idea to bigger numbers by sorting digit by digit.

## How Python sorts

`sorted()` and `list.sort()` use **Timsort**: merge sort combined with insertion sort for small runs. It is O(n log n), stable, and extra fast on data that is partly sorted. Use the `key` argument to sort by anything.

```python tryit
people = [("Ana", 31), ("Ben", 25), ("Cy", 31), ("Dee", 22)]
print(sorted(people, key=lambda p: p[1]))                 # by age, stable
print(sorted(people, key=lambda p: (-p[1], p[0])))         # oldest first, then name
print(sorted(["banana", "Apple", "cherry"], key=str.lower))
```

## Summary

| Sort | Big O | Notes |
|---|---|---|
| Merge sort | O(n log n) always | stable, extra memory |
| Quick sort | O(n log n) average, O(n²) worst | fast in practice |
| Counting sort | O(n + k) | small whole numbers only |
| Timsort (`sorted`) | O(n log n) | use it in real code |

```exercise
{
  "title": "Merge two lists",
  "prompt_md": "Write `merge(a, b)` that combines two **sorted** lists into one sorted list in a single pass (do not call `sorted()`). Print `merge([1, 5, 8], [2, 3, 9, 10])`. The output must be `[1, 2, 3, 5, 8, 9, 10]`.",
  "starter_code": "def merge(a, b):\n    result = []\n    i = j = 0\n    # take the smaller front item until one list is used up\n    return result\n\nprint(merge([1, 5, 8], [2, 3, 9, 10]))\n",
  "solution_code": "def merge(a, b):\n    result = []\n    i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            result.append(a[i])\n            i += 1\n        else:\n            result.append(b[j])\n            j += 1\n    return result + a[i:] + b[j:]\n\nprint(merge([1, 5, 8], [2, 3, 9, 10]))\n",
  "check_type": "output",
  "expected_value": "[1, 2, 3, 5, 8, 9, 10]",
  "hint": "While both lists have items, append the smaller front item and move that list's index. Then add what is left of both."
}
```

```quiz
{
  "title": "Final quiz: Data Structures and Algorithms",
  "final": true,
  "questions": [
    {"question": "What is the Big O of binary search?", "options": ["O(n)", "O(log n)", "O(1)"], "answer": 1, "explanation": "It halves the range every step."},
    {"question": "Which structure is last in, first out?", "options": ["queue", "stack", "hash table"], "answer": 1, "explanation": "A stack takes from the top."},
    {"question": "Which is the right tool for a fast queue in Python?", "options": ["list with pop(0)", "collections.deque", "set"], "answer": 1, "explanation": "deque.popleft() is O(1)."},
    {"question": "What makes dict lookups O(1) on average?", "options": ["Sorting", "Hashing", "Recursion"], "answer": 1, "explanation": "The hash says which bucket to check."},
    {"question": "In a binary search tree, the left subtree holds...", "options": ["larger values", "smaller values", "the same values"], "answer": 1, "explanation": "Left is smaller, right is larger."},
    {"question": "Which graph search uses a queue?", "options": ["BFS", "DFS"], "answer": 0, "explanation": "Breadth-first search explores level by level with a queue."},
    {"question": "Which sort is O(n log n) in every case?", "options": ["quick sort", "merge sort", "bubble sort"], "answer": 1, "explanation": "Merge sort always splits evenly."},
    {"question": "What does Python's sorted() use?", "options": ["bubble sort", "Timsort", "counting sort"], "answer": 1, "explanation": "Timsort mixes merge sort and insertion sort."}
  ]
}
```
