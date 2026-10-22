---
title: Python List Methods
slug: list-methods
summary: Add, remove, find, sort, reverse, copy and join lists, and avoid the two-names-one-list surprise.
minutes: 12
---
## Adding items

| Method | What it does |
|---|---|
| `append(x)` | adds `x` at the end |
| `insert(i, x)` | puts `x` at position `i` |
| `extend(other)` | adds every item of another list (or any iterable) |

```python tryit
queue = ["Ana", "Ben"]
queue.append("Cleo")
queue.insert(0, "Dev")       # jumps to the front
queue.extend(["Eli", "Fay"])
print(queue)
```

`append` adds **one** item, even if that item is a list. Compare:

```python tryit
a = [1, 2]
a.append([3, 4])
print(a)        # [1, 2, [3, 4]]

b = [1, 2]
b.extend([3, 4])
print(b)        # [1, 2, 3, 4]
```

## Removing items

| Way | Removes |
|---|---|
| `remove(x)` | the first item equal to `x` (error if missing) |
| `pop()` | the last item, and gives it back |
| `pop(i)` | the item at index `i`, and gives it back |
| `del items[i]` | the item at index `i` (also works with slices) |
| `clear()` | everything |

```python tryit
tools = ["saw", "drill", "hammer", "drill", "tape"]
tools.remove("drill")       # only the first drill
print(tools)

last = tools.pop()
print(last, tools)

first = tools.pop(0)
print(first, tools)

del tools[0]
print(tools)

tools.clear()
print(tools)
```

To remove **every** copy of a value, build a new list: `[t for t in tools if t != "drill"]`.

## Finding items

```python tryit
scores = [70, 85, 70, 92, 70]
print(scores.index(85))   # 1: position of the first 85
print(scores.count(70))   # 3
print(92 in scores)       # True
```

## Sorting

`sort()` sorts the list **in place** and returns `None`. `sorted()` leaves the list alone and returns a **new** sorted list.

```python tryit
ages = [31, 7, 19, 55, 3]
ages.sort()
print(ages)

ages.sort(reverse=True)
print(ages)

names = ["zoe", "Adam", "bea", "Carl"]
print(sorted(names))                 # capitals come first
print(sorted(names, key=str.lower))  # ignore case
print(sorted(names, key=len))        # shortest first
print(names)                         # unchanged
```

`key` is a function that Python calls on each item; the list is sorted by what that function returns.

A common mistake: `ages = ages.sort()` sets `ages` to `None`.

## Reversing

```python tryit
steps = [1, 2, 3, 4]
steps.reverse()       # in place
print(steps)
print(steps[::-1])    # a reversed copy, steps stays as it is
```

## Copying a list

`b = a` does **not** copy. It gives the same list a second name, so a change through one name shows through the other.

```python tryit
original = ["a", "b"]
alias = original
alias.append("c")
print(original)   # ['a', 'b', 'c'] - surprise!

copy1 = original.copy()
copy2 = list(original)
copy3 = original[:]
copy1.append("d")
print(original, copy1)
```

`copy()`, `list()` and `[:]` all make a **shallow** copy: a new outer list, but any lists inside are still shared. For lists of lists, use `copy.deepcopy()` from the `copy` module.

## Joining lists

```python tryit
morning = ["run", "shower"]
evening = ["read", "sleep"]
day = morning + evening
print(day)
print(["-"] * 5)
```

## Summary

- `append` adds one item, `extend` adds many, `insert` adds at a position.
- `remove` deletes by value, `pop` and `del` by position.
- `sort()` changes the list and returns `None`; `sorted()` returns a new list.
- `b = a` shares one list; use `a.copy()` for a separate one.

```exercise
{
  "title": "Tidy the playlist",
  "prompt_md": "Change `playlist` with list methods so that it:\n\n1. loses the song `\"Noise\"`,\n2. gains `\"Calm\"` at the end,\n3. is sorted A to Z.\n\nThen print it. The output must be `['Calm', 'Dawn', 'River', 'Storm']`.",
  "starter_code": "playlist = [\"Storm\", \"Noise\", \"Dawn\", \"River\"]\n",
  "solution_code": "playlist = [\"Storm\", \"Noise\", \"Dawn\", \"River\"]\nplaylist.remove(\"Noise\")\nplaylist.append(\"Calm\")\nplaylist.sort()\nprint(playlist)",
  "check_type": "output",
  "expected_value": "['Calm', 'Dawn', 'River', 'Storm']",
  "hint": "remove(\"Noise\"), append(\"Calm\"), then sort(). Do not write playlist = playlist.sort()."
}
```

```exercise
{
  "title": "A real copy",
  "prompt_md": "The code below changes `prices` by mistake. Fix the second line so that `sale` is a **copy**. The output must be:\n\n```\n[10, 20, 30]\n[5.0, 10.0, 15.0]\n```",
  "starter_code": "prices = [10, 20, 30]\nsale = prices\nfor i in range(len(sale)):\n    sale[i] = sale[i] / 2\nprint(prices)\nprint(sale)",
  "solution_code": "prices = [10, 20, 30]\nsale = prices.copy()\nfor i in range(len(sale)):\n    sale[i] = sale[i] / 2\nprint(prices)\nprint(sale)",
  "check_type": "output",
  "expected_value": "[10, 20, 30]\n[5.0, 10.0, 15.0]",
  "hint": "sale = prices.copy() makes a new list."
}
```

```quiz
[
  {"question": "nums = [3, 1, 2]; x = nums.sort(). What is x?", "options": ["[1, 2, 3]", "None", "[3, 1, 2]"], "answer": 1, "explanation": "sort() changes the list in place and returns None."},
  {"question": "What does pop() with no index remove?", "options": ["The first item", "The last item", "A random item"], "answer": 1, "explanation": "pop() removes and returns the last item."},
  {"question": "a = [1]; b = a; b.append(2). What is a?", "options": ["[1]", "[1, 2]", "[2]"], "answer": 1, "explanation": "a and b are two names for the same list."},
  {"question": "Which adds every item of another list?", "options": ["append", "extend", "insert"], "answer": 1, "explanation": "extend adds each item; append would add the whole list as one item."}
]
```
