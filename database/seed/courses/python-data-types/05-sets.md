---
title: Python Set Methods and Set Maths
slug: set-methods
summary: Add and remove set items, then combine sets with union, intersection and difference, and test subsets.
minutes: 10
---
## A set keeps each value once

A **set** is an unordered collection with no duplicates. Making a set from a list is the quickest way to drop repeats.

```python tryit
visits = [3, 1, 3, 2, 1, 3]
unique = set(visits)
print(unique)
print(len(unique), "different values")
print(2 in unique)    # very fast, even for huge sets
```

Sets have **no order and no index**: `unique[0]` is an error. When you need a fixed order to show them, use `sorted(the_set)`, which gives a list.

An empty set is `set()`. Writing `{}` makes an empty **dictionary**.

## Adding and removing

| Method | What it does |
|---|---|
| `add(x)` | adds one value (nothing happens if it is there already) |
| `update(items)` | adds every value from a list, tuple or other set |
| `remove(x)` | removes `x`, raises `KeyError` if it is missing |
| `discard(x)` | removes `x`, says nothing if it is missing |
| `pop()` | removes and returns some value (you cannot choose which) |

```python tryit
skills = {"python", "sql"}
skills.add("git")
skills.add("python")          # already there
skills.update(["html", "css"])
skills.discard("java")        # not there: no error
skills.remove("css")
print(sorted(skills))
```

## Set maths

Think of two overlapping circles in a Venn diagram.

| Operator | Method | Gives the values that are... |
|---|---|---|
| `a | b` | `a.union(b)` | in either set |
| `a & b` | `a.intersection(b)` | in both sets |
| `a - b` | `a.difference(b)` | in `a` but not in `b` |
| `a ^ b` | `a.symmetric_difference(b)` | in one set but not both |

```python tryit
monday = {"Ali", "Bo", "Cy", "Di"}
tuesday = {"Cy", "Di", "Ed"}

print("came at least once:", sorted(monday | tuesday))
print("came both days:    ", sorted(monday & tuesday))
print("only Monday:       ", sorted(monday - tuesday))
print("only one day:      ", sorted(monday ^ tuesday))
```

The methods also accept lists: `monday.union(["Fi", "Gu"])`. The operators need two sets.

## Changing a set in place

Each operation has an *update* version that changes the left set instead of making a new one: `|=`, `&=`, `-=`, `^=`.

```python tryit
allowed = {"read", "write", "delete"}
allowed -= {"delete"}
print(sorted(allowed))
```

## Subsets and supersets

```python tryit
needed = {"flour", "eggs"}
pantry = {"flour", "eggs", "milk", "salt"}
print(needed <= pantry)           # True: every needed item is in the pantry
print(needed.issubset(pantry))    # the same check
print(pantry.issuperset(needed))  # the other way round
print(needed.isdisjoint({"tea"})) # True: nothing in common
```

## Frozen sets

A `frozenset` is a set that cannot change. Like a tuple, it can be a dictionary key or live inside another set.

```python tryit
pair = frozenset({"red", "blue"})
same = frozenset({"blue", "red"})
print(pair == same)     # order never matters in sets
```

## Summary

- Sets drop duplicates and have no order; use `sorted()` to show them.
- `add`, `update`, `remove`, `discard` change a set.
- `|` union, `&` intersection, `-` difference, `^` symmetric difference.
- `<=` tests for a subset.

```exercise
{
  "title": "Shared interests",
  "prompt_md": "Print, as sorted lists, first the hobbies that **both** friends share, then the hobbies that **only Max** has. The output must be:\n\n```\n['chess', 'hiking']\n['climbing', 'piano']\n```",
  "starter_code": "max_hobbies = {\"chess\", \"hiking\", \"piano\", \"climbing\"}\nzoe_hobbies = {\"hiking\", \"chess\", \"painting\"}\n",
  "solution_code": "max_hobbies = {\"chess\", \"hiking\", \"piano\", \"climbing\"}\nzoe_hobbies = {\"hiking\", \"chess\", \"painting\"}\nprint(sorted(max_hobbies & zoe_hobbies))\nprint(sorted(max_hobbies - zoe_hobbies))",
  "check_type": "output",
  "expected_value": "['chess', 'hiking']\n['climbing', 'piano']",
  "hint": "& gives the values in both sets, - the values only in the left one. Wrap each in sorted()."
}
```

```exercise
{
  "title": "Count the different words",
  "prompt_md": "How many **different** words are in `text`, ignoring capitals? Lower-case the text, split it into words, turn the words into a set and print its length. The output must be `5`.",
  "starter_code": "text = \"The cat saw the dog and the Dog saw THE cat\"\n",
  "solution_code": "text = \"The cat saw the dog and the Dog saw THE cat\"\nprint(len(set(text.lower().split())))",
  "check_type": "output",
  "expected_value": "5",
  "hint": "set(text.lower().split()) keeps each word once."
}
```

```quiz
[
  {"question": "What does {} create?", "options": ["An empty set", "An empty dictionary", "An error"], "answer": 1, "explanation": "{} is an empty dict; use set() for an empty set."},
  {"question": "{1, 2, 3} & {2, 3, 4} gives...", "options": ["{1, 2, 3, 4}", "{2, 3}", "{1, 4}"], "answer": 1, "explanation": "& keeps the values found in both sets."},
  {"question": "Which method removes a value without an error when it is missing?", "options": ["remove", "discard", "pop"], "answer": 1, "explanation": "discard is silent; remove raises KeyError."}
]
```
