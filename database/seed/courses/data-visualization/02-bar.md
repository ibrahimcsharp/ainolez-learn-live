---
title: Bar Charts
slug: bar-charts
summary: Compare categories with vertical, horizontal, sorted and grouped bar charts.
minutes: 7
---
## Comparing categories

Bar charts compare amounts across **categories**: sales per product, votes per party, users per country.

```python tryit
import matplotlib.pyplot as plt

languages = ["Python", "JavaScript", "SQL", "Java", "C#"]
learners = [520, 410, 300, 180, 150]

plt.bar(languages, learners, color="#04AA6D")
plt.title("Learners per language")
plt.ylabel("Learners")
plt.show()
```

Bar charts should start at zero: a cut axis makes small differences look huge.

## Horizontal and sorted bars

With long names or many categories, horizontal bars are easier to read. Sorting puts the biggest on top:

```python tryit
import matplotlib.pyplot as plt

countries = {"Nigeria": 820, "India": 1340, "United Kingdom": 410, "Brazil": 560, "Bangladesh": 690}
ordered = sorted(countries.items(), key=lambda pair: pair[1])
names = [name for name, _ in ordered]
values = [value for _, value in ordered]

plt.barh(names, values, color="#05192D")
plt.title("Learners by country")
plt.xlabel("Learners")
for y, value in enumerate(values):
    plt.text(value + 10, y, str(value), va="center")   # value labels
plt.show()
```

## Grouped bars

To compare two series per category, shift the bars side by side:

```python tryit
import matplotlib.pyplot as plt
import numpy as np

quarters = ["Q1", "Q2", "Q3", "Q4"]
online = [40, 55, 62, 80]
shop = [60, 58, 50, 45]
x = np.arange(len(quarters))
width = 0.4

plt.bar(x - width / 2, online, width, label="Online")
plt.bar(x + width / 2, shop, width, label="Shop")
plt.xticks(x, quarters)
plt.title("Sales by channel")
plt.legend()
plt.show()
```

## Summary

- `plt.bar()` and `plt.barh()` draw bars.
- Start bars at zero and sort them to make comparisons easy.
- Shift bar positions to group two series.

```exercise
{
  "title": "A horizontal bar chart",
  "prompt_md": "Draw the scores as a **horizontal** bar chart with `plt.barh(names, scores)`.",
  "starter_code": "import matplotlib.pyplot as plt\n\nnames = [\"Amara\", \"Ben\", \"Chen\"]\nscores = [88, 72, 95]\n\nplt.show()",
  "solution_code": "import matplotlib.pyplot as plt\n\nnames = [\"Amara\", \"Ben\", \"Chen\"]\nscores = [88, 72, 95]\nplt.barh(names, scores)\nplt.show()",
  "check_type": "regex",
  "expected_value": "plt\\.barh\\(\\s*names\\s*,\\s*scores",
  "hint": "plt.barh(names, scores)"
}
```

```quiz
[
  {"question": "Why should a bar chart's axis start at zero?", "options": ["Otherwise small differences look much bigger than they are", "matplotlib requires it", "It makes bars thinner"], "answer": 0, "explanation": "Bar length is read as the amount, so it must start at zero."},
  {"question": "When are horizontal bars better?", "options": ["With long category names or many categories", "For time series", "Never"], "answer": 0, "explanation": "Labels fit and read left to right."}
]
```
