---
title: pandas Plotting and Subplots
slug: pandas-subplots
summary: Plot straight from DataFrames and put several charts in one figure with subplots.
minutes: 8
---
## Plotting from pandas

Every DataFrame and Series has a `.plot()` method that uses matplotlib for you:

```python tryit
import matplotlib.pyplot as plt
import pandas as pd

sales = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "online": [40, 48, 55, 62, 70, 81],
    "shop": [60, 59, 57, 50, 48, 45],
}).set_index("month")

sales.plot(marker="o", title="Sales by channel")
plt.ylabel("Sales")
plt.show()
```

`kind=` picks the chart type: `"line"`, `"bar"`, `"barh"`, `"hist"`, `"scatter"`, `"box"`.

```python tryit
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.DataFrame({
    "product": ["Pen", "Lamp", "Pen", "Mug", "Lamp", "Pen", "Mug"],
    "revenue": [20, 50, 15, 12, 45, 30, 9],
})
orders.groupby("product")["revenue"].sum().sort_values().plot(kind="barh", color="#04AA6D")
plt.title("Revenue per product")
plt.show()
```

## Figures and axes

For more control, create a **figure** (the whole image) with one or more **axes** (charts) using `plt.subplots()`:

```python tryit
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
ages = rng.normal(32, 9, 300)
months = ["Jan", "Feb", "Mar", "Apr"]
signups = [120, 160, 210, 260]

fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))

left.plot(months, signups, marker="o")
left.set_title("Signups per month")

right.hist(ages, bins=15, color="#05192D")
right.set_title("Age of learners")
right.set_xlabel("Age")

fig.suptitle("Learner dashboard")
fig.tight_layout()
plt.show()
```

With axes you call `ax.set_title()`, `ax.set_xlabel()` and so on instead of `plt.title()`.

## Saving a chart

```python
fig.savefig("dashboard.png", dpi=150, bbox_inches="tight")
```

## Summary

- `df.plot(kind=...)` charts a DataFrame in one line.
- `fig, axes = plt.subplots(rows, cols)` makes several charts in one figure.
- `fig.savefig()` saves the image.

```exercise
{
  "title": "Two charts side by side",
  "prompt_md": "Create a figure with **1 row and 2 columns** of charts using `plt.subplots(1, 2)`, and draw anything on each.",
  "starter_code": "import matplotlib.pyplot as plt\n\n\nplt.show()",
  "solution_code": "import matplotlib.pyplot as plt\n\nfig, (a, b) = plt.subplots(1, 2)\na.plot([1, 2, 3], [3, 1, 2])\nb.bar([\"x\", \"y\"], [4, 6])\nplt.show()",
  "check_type": "regex",
  "expected_value": "plt\\.subplots\\(\\s*1\\s*,\\s*2",
  "hint": "fig, (a, b) = plt.subplots(1, 2)"
}
```

```quiz
[
  {"question": "What does df.plot(kind=\"bar\") draw?", "options": ["A bar chart of the DataFrame", "A table", "Nothing without matplotlib code"], "answer": 0, "explanation": "pandas calls matplotlib for you."},
  {"question": "In fig, ax = plt.subplots(), what is ax?", "options": ["One chart area you draw on", "The whole image file", "The data"], "answer": 0, "explanation": "The figure is the image; axes are the charts in it."}
]
```
