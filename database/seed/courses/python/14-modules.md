---
title: Python Modules
slug: modules
summary: Import ready-made tools from Python's standard library, such as math, random and datetime.
minutes: 7
---
## What is a module?

A module is a file of Python code that someone already wrote. Python comes with a large **standard library** of modules. You load one with `import`.

```python tryit
import math

print(math.sqrt(81))
print(math.pi)
print(math.ceil(4.1), math.floor(4.9))
```

## Importing only what you need

```python tryit
from math import sqrt, pi
print(sqrt(16) * pi)

import statistics as stats   # a shorter name
print(stats.mean([4, 8, 6]))
```

## random

```python tryit
import random

print(random.randint(1, 6))               # a dice roll
print(random.choice(["rock", "paper", "scissors"]))
cards = [1, 2, 3, 4, 5]
random.shuffle(cards)
print(cards)
```

Run it several times: the results change.

## datetime

```python tryit
from datetime import date, timedelta

today = date(2026, 10, 18)
print(today.year, today.month, today.day)
print(today + timedelta(days=30))
print(today.strftime("%d %B %Y"))
```

## Packages from the community

Beyond the standard library, thousands of packages exist, installed with `pip install name`. You will meet some of the most famous later: **numpy** and **pandas** for data, **matplotlib** for charts and **scikit-learn** for machine learning. In this website's editor they are already available.

## Summary

- `import module` loads a module; use it as `module.name`.
- `from module import name` imports one part; `as` gives a short name.
- `math`, `random`, `statistics` and `datetime` are part of every Python.

```exercise
{
  "title": "Circle area",
  "prompt_md": "Import `pi` from `math` and print the area of a circle with radius `3` (pi times radius squared), rounded to 2 decimals. The output must be exactly `28.27`.",
  "starter_code": "radius = 3\n",
  "solution_code": "from math import pi\nradius = 3\nprint(round(pi * radius ** 2, 2))",
  "check_type": "output",
  "expected_value": "28.27",
  "hint": "pi * radius ** 2, then round(..., 2)."
}
```

```quiz
[
  {"question": "How do you use sqrt after import math?", "options": ["sqrt(9)", "math.sqrt(9)", "import.sqrt(9)"], "answer": 1, "explanation": "After import math, its functions are reached through math."},
  {"question": "Which module gives random numbers?", "options": ["math", "random", "datetime"], "answer": 1, "explanation": "random has randint, choice, shuffle and more."}
]
```
