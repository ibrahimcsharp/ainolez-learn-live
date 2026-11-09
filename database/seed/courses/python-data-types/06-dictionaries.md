---
title: Python Dictionary Methods and Nested Dictionaries
slug: dictionary-methods
summary: Read keys safely with get, add and remove items, loop over keys and values, copy, merge and work with dictionaries inside dictionaries.
minutes: 12
---
## Reading values safely

`book["title"]` raises a `KeyError` when the key is missing. `get()` returns `None`, or a default you choose, instead.

```python tryit
book = {"title": "Dune", "year": 1965}
print(book["title"])
print(book.get("pages"))          # None
print(book.get("pages", 0))       # 0
print("year" in book)             # checks keys
```

## Adding, changing and merging

Assigning to a key adds it or replaces its value. `update()` copies in every item of another dictionary. The `|` operator merges two into a **new** one; when both have a key, the right side wins.

```python tryit
book = {"title": "Dune", "year": 1965}
book["author"] = "Frank Herbert"
book["year"] = 1966                    # changed
book.update({"pages": 412, "year": 1965})
print(book)

defaults = {"theme": "light", "size": 12}
mine = {"size": 16}
print(defaults | mine)
```

## setdefault: get it or create it

`setdefault(key, value)` returns the value for `key`; if the key is missing, it first stores `value`. It is handy for grouping.

```python tryit
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
by_letter = {}
for word in words:
    by_letter.setdefault(word[0], []).append(word)
print(by_letter)
```

## Removing items

| Way | What it does |
|---|---|
| `pop(key)` | removes the key and returns its value (`KeyError` if missing) |
| `pop(key, default)` | the same, but returns `default` when missing |
| `popitem()` | removes and returns the **last** added `(key, value)` pair |
| `del d[key]` | removes the key |
| `clear()` | removes everything |

```python tryit
stock = {"pens": 40, "clips": 300, "tape": 12, "glue": 5}
taken = stock.pop("tape")
print(taken, stock)
print(stock.pop("ink", "none left"))
print(stock.popitem())
del stock["pens"]
print(stock)
```

## Looping

`keys()`, `values()` and `items()` give **views**: live windows onto the dictionary. Looping over a dictionary itself gives its keys.

```python tryit
prices = {"tea": 2.5, "cake": 3.2, "juice": 2.9}
for item in prices:
    print(item)

print(sum(prices.values()))

for item, price in prices.items():
    print(f"{item:<6}{price:>5.2f}")

cheapest = min(prices, key=prices.get)
print("cheapest:", cheapest)
```

Do not add or remove keys **while** looping over a dictionary; loop over `list(d)` if you must.

## Building dictionaries quickly

```python tryit
squares = {n: n * n for n in range(1, 6)}
print(squares)

empty_scores = dict.fromkeys(["ana", "ben", "cy"], 0)
print(empty_scores)

pairs = zip(["x", "y"], [3, 7])
print(dict(pairs))
```

## Copying

Like lists, `b = a` shares one dictionary. `a.copy()` or `dict(a)` makes a shallow copy.

```python tryit
settings = {"volume": 5}
backup = settings.copy()
settings["volume"] = 9
print(settings, backup)
```

## Nested dictionaries

A value can be another dictionary, which makes a small tree of data. Chain the keys to reach inside.

```python tryit
school = {
    "class_a": {"teacher": "Ms Park", "pupils": 24},
    "class_b": {"teacher": "Mr Diaz", "pupils": 27},
}
print(school["class_b"]["teacher"])

school["class_a"]["pupils"] += 1
school["class_c"] = {"teacher": "Mx Lee", "pupils": 22}

for name, info in school.items():
    print(f"{name}: {info['teacher']} with {info['pupils']} pupils")

total = sum(info["pupils"] for info in school.values())
print("total pupils:", total)
```

When some inner keys may be missing, chain `get()` with an empty dictionary as the default: `school.get("class_z", {}).get("teacher")`.

## Summary

- `get(key, default)` reads without a `KeyError`.
- `update()` and `|` merge; `setdefault()` creates a value when it is missing.
- `pop`, `popitem`, `del` and `clear` remove items.
- `items()` gives key-value pairs to loop over.
- Nested dictionaries are reached with `d["outer"]["inner"]`.

```exercise
{
  "title": "Count the votes",
  "prompt_md": "Count how many votes each colour got, using a dictionary and `get()`. Then print each colour and its count, one per line, in the order the colours first appear:\n\n```\nred 3\nblue 2\ngreen 1\n```",
  "starter_code": "votes = [\"red\", \"blue\", \"red\", \"green\", \"blue\", \"red\"]\ncounts = {}\n",
  "solution_code": "votes = [\"red\", \"blue\", \"red\", \"green\", \"blue\", \"red\"]\ncounts = {}\nfor colour in votes:\n    counts[colour] = counts.get(colour, 0) + 1\nfor colour, number in counts.items():\n    print(colour, number)",
  "check_type": "output",
  "expected_value": "red 3\nblue 2\ngreen 1",
  "hint": "counts[colour] = counts.get(colour, 0) + 1 starts each new colour at 0."
}
```

```exercise
{
  "title": "Inside the nest",
  "prompt_md": "`users` is a nested dictionary. Print the city of `\"kai\"`, then the names of everyone whose age is 30 or more, as a sorted list. The output must be:\n\n```\nOsaka\n['kai', 'nia']\n```",
  "starter_code": "users = {\n    \"kai\": {\"age\": 34, \"city\": \"Osaka\"},\n    \"lea\": {\"age\": 22, \"city\": \"Bern\"},\n    \"nia\": {\"age\": 30, \"city\": \"Accra\"},\n}\n",
  "solution_code": "users = {\n    \"kai\": {\"age\": 34, \"city\": \"Osaka\"},\n    \"lea\": {\"age\": 22, \"city\": \"Bern\"},\n    \"nia\": {\"age\": 30, \"city\": \"Accra\"},\n}\nprint(users[\"kai\"][\"city\"])\nprint(sorted(name for name, info in users.items() if info[\"age\"] >= 30))",
  "check_type": "output",
  "expected_value": "Osaka\n['kai', 'nia']",
  "hint": "users[\"kai\"][\"city\"] reaches inside. Loop over users.items() to check each age."
}
```

```quiz
[
  {"question": "d = {\"a\": 1}. What does d.get(\"b\", 5) return?", "options": ["None", "5", "a KeyError"], "answer": 1, "explanation": "get returns the default when the key is missing."},
  {"question": "{\"x\": 1} | {\"x\": 2} gives...", "options": ["{\"x\": 1}", "{\"x\": 2}", "{\"x\": [1, 2]}"], "answer": 1, "explanation": "When both sides have a key, the right side wins."},
  {"question": "What does looping with for k in d give you?", "options": ["The values", "The keys", "(key, value) pairs"], "answer": 1, "explanation": "Looping over a dict gives its keys; use items() for pairs."},
  {"question": "Which removes the most recently added item?", "options": ["pop()", "popitem()", "clear()"], "answer": 1, "explanation": "popitem() removes and returns the last added pair."}
]
```
