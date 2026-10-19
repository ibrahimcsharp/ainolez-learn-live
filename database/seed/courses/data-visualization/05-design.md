---
title: Designing Clear Charts
slug: chart-design
summary: Choose the right chart, remove clutter, highlight the message and keep charts honest.
minutes: 7
---
## Pick the chart for the question

| Question | Chart |
|----------|-------|
| How does it change over time? | line |
| Which category is bigger? | bar (sorted) |
| How are the values spread? | histogram, box plot |
| Do two values move together? | scatter |
| What share of the whole? | stacked bar (or pie, with 2–4 parts only) |

## Less ink, more message

Remove what does not help the reader: heavy grids, boxes, 3D effects, legends you could replace with labels. Then make the important part stand out.

```python tryit
import matplotlib.pyplot as plt

teams = ["Design", "Sales", "Support", "Engineering", "Marketing"]
satisfaction = [72, 64, 58, 81, 69]
colors = ["#C9CED6"] * len(teams)
colors[teams.index("Support")] = "#E8590C"     # the one we talk about

fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(teams, satisfaction, color=colors)
ax.set_title("Support has the lowest satisfaction (58%)", loc="left", fontsize=13)
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlim(0, 100)
ax.set_xlabel("Satisfaction (%)")
plt.show()
```

The title states the **finding**, not just the topic. Grey for context, one strong colour for the point.

## Keep charts honest

- Bars start at zero.
- Do not stretch an axis to make a small change look dramatic.
- Label units and say where the data comes from.
- Use colour-blind friendly palettes (matplotlib's default and `viridis` are).

## Accessibility

Do not rely on colour alone: add labels, markers or patterns. Write the key number in the title or alt text so everyone gets the message.

## Summary

- Choose the chart type from the question.
- Remove clutter; highlight one thing.
- Titles state the finding; axes stay honest.

```exercise
{
  "title": "Remove the clutter",
  "prompt_md": "Hide the **top** and **right** borders of the chart with `ax.spines[[\"top\", \"right\"]].set_visible(False)`.",
  "starter_code": "import matplotlib.pyplot as plt\n\nfig, ax = plt.subplots()\nax.bar([\"A\", \"B\", \"C\"], [5, 9, 3])\n\nplt.show()",
  "solution_code": "import matplotlib.pyplot as plt\n\nfig, ax = plt.subplots()\nax.bar([\"A\", \"B\", \"C\"], [5, 9, 3])\nax.spines[[\"top\", \"right\"]].set_visible(False)\nplt.show()",
  "check_type": "regex",
  "expected_value": "spines\\[\\[\\s*[\"'](top|right)[\"']\\s*,\\s*[\"'](top|right)[\"']\\s*\\]\\]\\.set_visible\\(\\s*False",
  "hint": "ax.spines[[\"top\", \"right\"]].set_visible(False)"
}
```

```quiz
{
  "title": "Final quiz: Data Visualization with Python",
  "final": true,
  "questions": [
    {"question": "Which chart shows change over time best?", "options": ["Line chart", "Pie chart", "Histogram"], "answer": 0, "explanation": "Lines follow a value through time."},
    {"question": "Which chart compares categories?", "options": ["Bar chart", "Scatter plot", "Histogram"], "answer": 0, "explanation": "Bars compare amounts per category."},
    {"question": "What does a histogram show?", "options": ["How values are spread", "A relationship between two values", "Shares of a whole"], "answer": 0, "explanation": "It counts values in ranges (bins)."},
    {"question": "What does plt.subplots(2, 2) create?", "options": ["A figure with four charts", "Two figures", "A chart with two lines"], "answer": 0, "explanation": "2 rows by 2 columns of axes."},
    {"question": "What makes a good chart title?", "options": ["It states the finding", "It is as short as possible, like 'Data'", "It repeats the axis labels"], "answer": 0, "explanation": "Tell the reader what to see."},
    {"question": "A strong correlation proves that...", "options": ["Nothing about cause on its own", "One value causes the other", "The data is wrong"], "answer": 0, "explanation": "Correlation is not causation."}
  ]
}
```
