---
title: Python collections
slug: collections
summary: Counter, defaultdict, namedtuple and deque - smarter containers from the collections module.
minutes: 9
---
## Counter: counting made easy

`Counter` counts how often each item appears.

```python tryit
from collections import Counter

votes = ["tea", "coffee", "tea", "juice", "tea", "coffee"]
counts = Counter(votes)
print(counts)
print(counts["tea"], counts["water"])   # missing items count as 0
print(counts.most_common(2))

letters = Counter("mississippi")
print(letters.most_common(1))
```

## defaultdict: no more KeyError

A `defaultdict` creates a starting value the first time you use a missing key.

```python tryit
from collections import defaultdict

words = ["apple", "avocado", "banana", "blueberry", "cherry"]
by_letter = defaultdict(list)       # missing keys start as []
for word in words:
    by_letter[word[0]].append(word)
print(dict(by_letter))

totals = defaultdict(int)           # missing keys start as 0
for item, amount in [("rent", 900), ("food", 120), ("food", 80)]:
    totals[item] += amount
print(dict(totals))
```

## namedtuple: tuples with names

A `namedtuple` is a small, unchangeable record. You read fields by name instead of by position.

```python tryit
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)
print(p)

City = namedtuple("City", "name country population")
cities = [City("Lagos", "Nigeria", 15_400_000), City("Lima", "Peru", 10_700_000)]
biggest = max(cities, key=lambda c: c.population)
print(biggest.name)
```

## deque: a fast double-ended queue

Adding or removing at the **start** of a list is slow for long lists. A `deque` is fast at both ends.

```python tryit
from collections import deque

line = deque(["Ana", "Ben"])
line.append("Cy")          # join at the back
line.appendleft("VIP")     # jump to the front
print(line.popleft())      # serve the first person
print(line)

recent = deque(maxlen=3)   # keeps only the last 3 items
for page in ["home", "news", "sport", "weather", "music"]:
    recent.append(page)
print(list(recent))
```

## Summary

- `Counter` counts items and finds the most common.
- `defaultdict(list)` / `defaultdict(int)` give missing keys a starting value.
- `namedtuple` makes readable records; `deque` is a fast queue with an optional `maxlen`.

```exercise
{
  "title": "Most common word",
  "prompt_md": "Use `Counter` to find the most common word in `text` (already lower case) and print it with its count, like `the 3`.",
  "starter_code": "from collections import Counter\n\ntext = \"the cat saw the dog and the dog saw a bird\"\n",
  "solution_code": "from collections import Counter\n\ntext = \"the cat saw the dog and the dog saw a bird\"\nword, count = Counter(text.split()).most_common(1)[0]\nprint(word, count)",
  "check_type": "output",
  "expected_value": "the 3",
  "hint": "Counter(text.split()).most_common(1) gives a list with one (word, count) pair."
}
```

```quiz
[
  {"question": "What is Counter(\"aab\")[\"z\"]?", "options": ["KeyError", "0", "None"], "answer": 1, "explanation": "A Counter returns 0 for missing items."},
  {"question": "What does defaultdict(list) give for a new key?", "options": ["None", "[]", "an error"], "answer": 1, "explanation": "It calls list() to create an empty list."},
  {"question": "Which is fast at removing from the front?", "options": ["list", "deque", "tuple"], "answer": 1, "explanation": "deque.popleft() is fast; list.pop(0) moves every item."}
]
```
