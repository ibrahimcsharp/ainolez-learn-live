---
title: Histograms and Scatter Plots
slug: hist-scatter
summary: Show how values are spread with histograms and how two values relate with scatter plots.
minutes: 8
---
## Histograms: how are values spread?

A **histogram** sorts numbers into ranges (bins) and counts how many fall into each. It shows the shape of the data: where most values are, how wide they spread, and odd outliers.

```python tryit
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(seed=1)
heights = rng.normal(loc=170, scale=8, size=500)   # 500 random heights in cm

plt.hist(heights, bins=20, color="#04AA6D", edgecolor="white")
plt.axvline(heights.mean(), color="black", linestyle="--", label="mean")
plt.title("Heights of 500 people")
plt.xlabel("Height (cm)")
plt.ylabel("People")
plt.legend()
plt.show()
```

Try `bins=5` and `bins=50`: too few bins hide detail, too many make noise.

## Scatter plots: do two values move together?

Each point is one item, placed by two values. Scatter plots reveal **relationships** (correlation):

```python tryit
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(seed=2)
hours = rng.uniform(0, 10, 60)
score = 40 + 5 * hours + rng.normal(0, 6, 60)

plt.scatter(hours, score, alpha=0.7)
plt.title("Study time and exam score")
plt.xlabel("Hours studied")
plt.ylabel("Score")
plt.show()

print("Correlation:", round(np.corrcoef(hours, score)[0, 1], 2))
```

A correlation near **1** means "go up together", near **-1** "one up, the other down", near **0** "no straight-line relationship".

!!! warning
    Correlation is not causation. Ice-cream sales and sunburn rise together, but ice cream does not cause sunburn: hot weather drives both.

## Colour and size as extra information

```python tryit
import matplotlib.pyplot as plt

price = [5, 8, 12, 20, 25, 30]
rating = [3.1, 3.8, 4.0, 4.5, 4.2, 4.8]
reviews = [40, 120, 300, 80, 500, 220]

plt.scatter(price, rating, s=reviews, c=rating, cmap="viridis", alpha=0.7)
plt.colorbar(label="Rating")
plt.title("Price, rating and number of reviews (dot size)")
plt.xlabel("Price ($)")
plt.ylabel("Rating")
plt.show()
```

## Summary

- `plt.hist(values, bins=...)` shows a distribution.
- `plt.scatter(x, y)` shows a relationship; `np.corrcoef` measures it.
- Correlation does not prove cause.

```exercise
{
  "title": "Plot the relationship",
  "prompt_md": "Draw a scatter plot of `temperature` (x) against `ice_cream` (y) with `plt.scatter`.",
  "starter_code": "import matplotlib.pyplot as plt\n\ntemperature = [14, 18, 22, 25, 29, 33]\nice_cream = [20, 34, 51, 60, 80, 95]\n\nplt.show()",
  "solution_code": "import matplotlib.pyplot as plt\n\ntemperature = [14, 18, 22, 25, 29, 33]\nice_cream = [20, 34, 51, 60, 80, 95]\nplt.scatter(temperature, ice_cream)\nplt.show()",
  "check_type": "regex",
  "expected_value": "plt\\.scatter\\(\\s*temperature\\s*,\\s*ice_cream",
  "hint": "plt.scatter(temperature, ice_cream)"
}
```

```quiz
[
  {"question": "Which chart shows how values are spread out?", "options": ["Histogram", "Line chart", "Pie chart"], "answer": 0, "explanation": "A histogram counts values in ranges."},
  {"question": "A correlation of -0.9 means...", "options": ["When one value rises, the other falls", "No relationship", "One causes the other"], "answer": 0, "explanation": "Negative correlation: opposite directions."}
]
```
