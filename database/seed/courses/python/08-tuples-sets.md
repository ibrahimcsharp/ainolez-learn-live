---
title: Python Tuples and Sets
slug: tuples-sets
summary: Use tuples for fixed groups of values and sets for unique values.
minutes: 7
---
## Tuples

A tuple is like a list that cannot change. Use round brackets.

```python tryit
point = (3, 4)
print(point[0], point[1])

colors = ("red", "green", "blue")
print(len(colors), "green" in colors)
```

Tuples are good for values that belong together and should not change, like a coordinate or a date.

## Unpacking

You can split a tuple into variables in one line:

```python tryit
person = ("Lina", 34, "Cairo")
name, age, city = person
print(name, "lives in", city)
```

```python
point[0] = 10   # TypeError: tuples cannot be changed
```

## Sets

A set keeps **unique** values with no order. Use curly brackets or `set()`.

```python tryit
tags = {"python", "ai", "python", "data"}
print(tags)          # "python" appears once
tags.add("web")
print(len(tags))

visitors = ["ana", "ben", "ana", "cy", "ben"]
print(len(set(visitors)), "unique visitors")
```

The order of a set can look different every time; do not rely on it.

## Set operations

```python tryit
python_fans = {"ana", "ben", "cy"}
ai_fans = {"ben", "dee"}
print(python_fans & ai_fans)   # in both
print(python_fans | ai_fans)   # in either
print(python_fans - ai_fans)   # only in the first
```

## Summary

- Tuples `( )` are ordered and cannot change.
- Sets `{ }` hold unique values without order.
- `&`, `|` and `-` combine sets.

```exercise
{
  "title": "Unique languages",
  "prompt_md": "Print how many **different** languages are in the list. The output must be exactly `3`.",
  "starter_code": "languages = [\"python\", \"sql\", \"python\", \"html\", \"sql\"]\n",
  "solution_code": "languages = [\"python\", \"sql\", \"python\", \"html\", \"sql\"]\nprint(len(set(languages)))",
  "check_type": "output",
  "expected_value": "3",
  "hint": "set() removes duplicates and len() counts."
}
```

```quiz
[
  {"question": "Which collection cannot be changed after it is made?", "options": ["list", "tuple", "set"], "answer": 1, "explanation": "Tuples are immutable."},
  {"question": "What is len({1, 1, 2})?", "options": ["3", "2", "1"], "answer": 1, "explanation": "A set keeps each value only once."}
]
```
