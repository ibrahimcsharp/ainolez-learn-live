---
title: Your First Line Chart
slug: line-charts
summary: Draw line charts with matplotlib and add a title, axis labels and a legend.
minutes: 7
---
## matplotlib

**matplotlib** is Python's most widely used chart library. Its `pyplot` part is imported as `plt` by convention. On this site the chart appears under the code when you press **Run** (the first run downloads matplotlib, which takes a few seconds).

```python tryit
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
visitors = [120, 180, 150, 240, 310, 290]

plt.plot(months, visitors)
plt.show()
```

`plt.plot(x, y)` draws a line through the points. Line charts are best for values that change **over time**.

## Labels make a chart readable

A chart without labels is a puzzle. Always add a title and name the axes:

```python tryit
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
visitors = [120, 180, 150, 240, 310, 290]

plt.plot(months, visitors, marker="o", color="#04AA6D")
plt.title("Website visitors per month")
plt.xlabel("Month")
plt.ylabel("Visitors")
plt.grid(alpha=0.3)
plt.show()
```

## Several lines and a legend

Give each line a `label`, then call `plt.legend()`:

```python tryit
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
plt.plot(months, [120, 180, 150, 240, 310, 290], marker="o", label="2026")
plt.plot(months, [100, 110, 140, 160, 200, 230], marker="o", linestyle="--", label="2025")
plt.title("Visitors per month")
plt.ylabel("Visitors")
plt.legend()
plt.show()
```

Useful style options: `color`, `linestyle` (`"-"`, `"--"`, `":"`), `marker` (`"o"`, `"s"`, `"^"`) and `linewidth`.

## Summary

- `import matplotlib.pyplot as plt`, then `plt.plot(x, y)`.
- Add `plt.title()`, `plt.xlabel()`, `plt.ylabel()`.
- `label=` on each line plus `plt.legend()` explains several lines.

```exercise
{
  "title": "Label the chart",
  "prompt_md": "Add the title `Daily steps` to the chart with `plt.title()`.",
  "starter_code": "import matplotlib.pyplot as plt\n\ndays = [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\"]\nsteps = [6200, 8100, 7400, 9900, 5600]\nplt.plot(days, steps, marker=\"o\")\n\nplt.show()",
  "solution_code": "import matplotlib.pyplot as plt\n\ndays = [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\"]\nsteps = [6200, 8100, 7400, 9900, 5600]\nplt.plot(days, steps, marker=\"o\")\nplt.title(\"Daily steps\")\nplt.show()",
  "check_type": "regex",
  "expected_value": "plt\\.title\\(\\s*[\"']Daily steps[\"']",
  "hint": "plt.title(\"Daily steps\")"
}
```

```quiz
[
  {"question": "Which chart type suits values over time?", "options": ["A line chart", "A pie chart", "A histogram"], "answer": 0, "explanation": "Lines show how a value rises and falls over time."},
  {"question": "What do you need for plt.legend() to show names?", "options": ["label= on each plot call", "A title", "A grid"], "answer": 0, "explanation": "The legend lists each line's label."}
]
```
