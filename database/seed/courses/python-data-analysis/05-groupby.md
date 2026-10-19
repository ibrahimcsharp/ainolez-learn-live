---
title: Grouping and Aggregating
slug: groupby
summary: Answer "per category" questions with groupby, agg and pivot tables.
minutes: 8
---
## Split, apply, combine

`groupby` splits the rows into groups, applies a calculation to each group and combines the results. It is the pandas version of SQL's `GROUP BY`.

```python tryit
import pandas as pd

sales = pd.DataFrame({
    "region": ["north", "south", "north", "east", "south", "north"],
    "product": ["Pen", "Pen", "Lamp", "Lamp", "Lamp", "Pen"],
    "revenue": [100, 250, 300, 50, 150, 80],
})
print(sales.groupby("region")["revenue"].sum())
print(sales.groupby("region")["revenue"].mean().round(1))
```

## Several statistics at once

```python tryit
import pandas as pd

sales = pd.DataFrame({
    "region": ["north", "south", "north", "east", "south", "north"],
    "revenue": [100, 250, 300, 50, 150, 80],
})
summary = sales.groupby("region").agg(
    orders=("revenue", "count"),
    total=("revenue", "sum"),
    biggest=("revenue", "max"),
)
print(summary.sort_values("total", ascending=False))
```

## Grouping by two columns

```python tryit
import pandas as pd

sales = pd.DataFrame({
    "region": ["north", "south", "north", "east", "south", "north"],
    "product": ["Pen", "Pen", "Lamp", "Lamp", "Lamp", "Pen"],
    "revenue": [100, 250, 300, 50, 150, 80],
})
print(sales.groupby(["region", "product"])["revenue"].sum())
print(sales.pivot_table(index="region", columns="product", values="revenue", aggfunc="sum", fill_value=0))
```

A **pivot table** puts one group along the rows and another along the columns, like a spreadsheet pivot.

## Summary

- `df.groupby("col")["value"].sum()` totals per group.
- `.agg(name=(column, function))` computes several statistics.
- `pivot_table` makes a two-way summary.

```exercise
{
  "title": "Revenue per product",
  "prompt_md": "Print the total `revenue` per `product` as a dictionary. The output must be exactly `{'Lamp': 500, 'Pen': 430}`",
  "starter_code": "import pandas as pd\n\nsales = pd.DataFrame({\n    \"product\": [\"Pen\", \"Pen\", \"Lamp\", \"Lamp\", \"Lamp\", \"Pen\"],\n    \"revenue\": [100, 250, 300, 50, 150, 80],\n})\n",
  "solution_code": "import pandas as pd\n\nsales = pd.DataFrame({\n    \"product\": [\"Pen\", \"Pen\", \"Lamp\", \"Lamp\", \"Lamp\", \"Pen\"],\n    \"revenue\": [100, 250, 300, 50, 150, 80],\n})\ntotals = sales.groupby(\"product\")[\"revenue\"].sum()\nprint({name: int(value) for name, value in totals.items()})",
  "check_type": "output",
  "expected_value": "{'Lamp': 500, 'Pen': 430}",
  "hint": "sales.groupby(\"product\")[\"revenue\"].sum(), then turn it into a dict of ints."
}
```

```quiz
[
  {"question": "Which SQL clause does groupby match?", "options": ["GROUP BY", "WHERE", "JOIN"], "answer": 0, "explanation": "Both split rows into groups and aggregate them."},
  {"question": "What does a pivot table show?", "options": ["One group along rows and another along columns", "Only the first rows", "Missing values"], "answer": 0, "explanation": "It is a two-way summary."}
]
```
