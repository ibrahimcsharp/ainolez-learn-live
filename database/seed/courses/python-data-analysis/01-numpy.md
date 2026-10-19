---
title: NumPy Arrays
slug: numpy
summary: Do fast maths on whole arrays of numbers at once with NumPy.
minutes: 8
---
## Why NumPy?

Python lists are flexible but slow for maths on millions of numbers. **NumPy** stores numbers in compact arrays and runs operations on the whole array at once. pandas, scikit-learn and matplotlib are all built on it.

The first run downloads NumPy into your browser, so it takes a few seconds.

```python tryit
import numpy as np

prices = np.array([12.5, 8.0, 30.0, 4.5])
print(prices * 2)          # every item doubled, no loop
print(prices + 1)
print(prices.sum(), prices.mean(), prices.max())
```

## Vectorised operations

An operation between two arrays works item by item:

```python tryit
import numpy as np

quantity = np.array([3, 10, 1, 4])
price = np.array([12.5, 8.0, 30.0, 4.5])
revenue = quantity * price
print(revenue)
print("Total:", revenue.sum())
```

## Filtering with conditions

A condition on an array gives an array of `True`/`False`, which you can use to pick items:

```python tryit
import numpy as np

scores = np.array([45, 82, 67, 91, 38, 74])
passed = scores >= 50
print(passed)
print(scores[passed])
print("Pass rate:", passed.mean())   # True counts as 1
```

## Creating arrays

```python tryit
import numpy as np

print(np.arange(0, 10, 2))      # like range()
print(np.linspace(0, 1, 5))     # 5 evenly spaced numbers
print(np.zeros(3), np.ones(3))
grid = np.arange(6).reshape(2, 3)
print(grid)
print(grid.shape)
```

## Summary

- `np.array()` makes an array; maths applies to every item.
- `arr[arr > 10]` filters with a condition.
- `.sum()`, `.mean()`, `.max()` and `.shape` describe an array.

```exercise
{
  "title": "Above average",
  "prompt_md": "Print only the temperatures that are **above the mean** of the array. The output must be exactly `[25 28 30]`",
  "starter_code": "import numpy as np\n\ntemps = np.array([18, 25, 21, 28, 19, 30])\n",
  "solution_code": "import numpy as np\n\ntemps = np.array([18, 25, 21, 28, 19, 30])\nprint(temps[temps > temps.mean()])",
  "check_type": "output",
  "expected_value": "[25 28 30]",
  "hint": "temps[temps > temps.mean()]"
}
```

```quiz
[
  {"question": "What is np.array([1, 2, 3]) * 2?", "options": ["[2 4 6]", "[1 2 3 1 2 3]", "An error"], "answer": 0, "explanation": "NumPy multiplies every item; a list would repeat instead."},
  {"question": "What does scores[scores > 50] return?", "options": ["The scores greater than 50", "True or False", "The count of scores"], "answer": 0, "explanation": "A boolean array selects the matching items."}
]
```
