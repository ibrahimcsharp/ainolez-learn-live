---
title: Linear and Binary Search
slug: searching
summary: Find an item by checking every element, or halve a sorted list until you find it.
minutes: 9
---
## Linear search

Check the items one by one until you find the target. It works on any list, sorted or not. Big O: **O(n)**.

```python tryit
def linear_search(items, target):
    for index, item in enumerate(items):
        if item == target:
            return index
    return -1

names = ["Kim", "Ola", "Raj", "Sue", "Ty"]
print(linear_search(names, "Sue"))
print(linear_search(names, "Zed"))
```

Python's `in` and `list.index()` do exactly this.

## Binary search

If the list is **sorted**, you can do much better. Look at the middle item:

- if it is the target, you are done;
- if the target is smaller, search the left half;
- if it is larger, search the right half.

Each step halves the list, so 1,000,000 items need at most about 20 steps. Big O: **O(log n)**.

```python tryit
def binary_search(items, target):
    low, high = 0, len(items) - 1
    steps = 0
    while low <= high:
        steps += 1
        middle = (low + high) // 2
        if items[middle] == target:
            return middle, steps
        if items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1, steps

numbers = list(range(0, 2_000_000, 2))     # one million even numbers
print(binary_search(numbers, 1_337_000))
print(binary_search(numbers, 7))           # not there
```

## Recursive binary search

The same idea, written as a function that calls itself on half of the list.

```python tryit
def search(items, target, low=0, high=None):
    if high is None:
        high = len(items) - 1
    if low > high:
        return -1
    middle = (low + high) // 2
    if items[middle] == target:
        return middle
    if items[middle] < target:
        return search(items, target, middle + 1, high)
    return search(items, target, low, middle - 1)

print(search([3, 8, 15, 21, 34, 55], 21))
```

## The bisect module

Python has binary search built in. `bisect` finds where a value is, or where it would go to keep the list sorted.

```python tryit
import bisect

scores = [40, 55, 62, 78, 91]
print(bisect.bisect_left(scores, 62))   # index of 62
print(bisect.bisect_left(scores, 70))   # 70 would go at index 3
bisect.insort(scores, 70)               # insert in order
print(scores)

def grade(score):
    return "FDCBA"[bisect.bisect([50, 60, 70, 80], score)]
print([grade(s) for s in [45, 65, 85]])
```

## Summary

- Linear search: any list, O(n).
- Binary search: sorted lists only, O(log n) - halve the range each step.
- `bisect` gives you binary search without writing it.

```exercise
{
  "title": "Guess the number",
  "prompt_md": "Use binary search to find `secret` between 1 and 100. Count your guesses and print `found 73 in 6 guesses`. Guess the middle of `low` and `high` with `(low + high) // 2`.",
  "starter_code": "secret = 73\nlow, high = 1, 100\nguesses = 0\n",
  "solution_code": "secret = 73\nlow, high = 1, 100\nguesses = 0\nwhile True:\n    guess = (low + high) // 2\n    guesses += 1\n    if guess == secret:\n        break\n    if guess < secret:\n        low = guess + 1\n    else:\n        high = guess - 1\nprint(f\"found {guess} in {guesses} guesses\")",
  "check_type": "output",
  "expected_value": "found 73 in 6 guesses",
  "hint": "Loop: guess the middle, count it, stop if right, otherwise move low or high past the guess."
}
```

```quiz
[
  {"question": "What does binary search need?", "options": ["A sorted list", "A list of numbers only", "A list with no duplicates"], "answer": 0, "explanation": "It relies on the order to throw away half the list."},
  {"question": "About how many steps does binary search need for 1,000,000 items?", "options": ["20", "1,000", "500,000"], "answer": 0, "explanation": "2 to the power 20 is about a million."},
  {"question": "What is the Big O of linear search?", "options": ["O(1)", "O(log n)", "O(n)"], "answer": 2, "explanation": "It may check every item."}
]
```
