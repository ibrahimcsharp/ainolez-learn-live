---
title: Python Lists
slug: lists
summary: Store many values in a list, read and change items, and use common list methods.
minutes: 9
---
## Creating a list

A list keeps several values in order, inside square brackets.

```python tryit
fruits = ["apple", "banana", "cherry"]
print(fruits)
print(len(fruits))
print(fruits[0])
print(fruits[-1])
```

Lists can hold any type, even mixed: `[1, "two", 3.0, True]`.

## Changing items

Unlike strings, lists can change.

```python tryit
fruits = ["apple", "banana", "cherry"]
fruits[1] = "mango"
fruits.append("kiwi")        # add at the end
fruits.insert(0, "lemon")    # add at a position
print(fruits)
fruits.remove("apple")       # remove by value
last = fruits.pop()          # remove and return the last item
print(fruits, last)
```

## Slices and checks

```python tryit
numbers = [10, 20, 30, 40, 50]
print(numbers[1:4])
print(30 in numbers)
print(numbers.index(40))
```

## Sorting and totals

```python tryit
scores = [72, 95, 58, 88]
print(sorted(scores))          # a new sorted list
scores.sort(reverse=True)      # sorts this list itself
print(scores)
print(sum(scores), min(scores), max(scores))
```

## Summary

- Lists are ordered and changeable: `items = [1, 2, 3]`.
- `append()`, `insert()`, `remove()` and `pop()` change a list.
- `sorted()`, `sum()`, `min()` and `max()` work on whole lists.

```exercise
{
  "title": "Average score",
  "prompt_md": "Add the score `90` to the list, then print the average of all scores (the total divided by how many there are). The output must be exactly `80.0`.",
  "starter_code": "scores = [70, 80]\n",
  "solution_code": "scores = [70, 80]\nscores.append(90)\nprint(sum(scores) / len(scores))",
  "check_type": "output",
  "expected_value": "80.0",
  "hint": "Use append(), then sum(scores) / len(scores)."
}
```

```quiz
[
  {"question": "What is [5, 6, 7][1]?", "options": ["5", "6", "7"], "answer": 1, "explanation": "Index 1 is the second item."},
  {"question": "Which method adds an item to the end?", "options": ["add()", "append()", "push()"], "answer": 1, "explanation": "append() adds one item at the end of a list."},
  {"question": "What is the difference between sorted(x) and x.sort()?", "options": ["None", "sorted(x) returns a new list, x.sort() changes x", "x.sort() returns a new list"], "answer": 1, "explanation": "sorted() leaves the original alone; .sort() sorts in place and returns None."}
]
```
