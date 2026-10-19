---
title: Combining Tables
slug: merge
summary: Join DataFrames with merge, stack them with concat, and save the result to CSV.
minutes: 8
---
## merge: join on a key

`pd.merge()` combines two tables on a shared column, like an SQL `JOIN`:

```python tryit
import pandas as pd

customers = pd.DataFrame({"customer_id": [1, 2, 3], "name": ["Amara", "Ben", "Chen"]})
orders = pd.DataFrame({"customer_id": [1, 1, 2], "item": ["Pen", "Notebook", "Backpack"], "price": [2, 5, 35]})

print(pd.merge(orders, customers, on="customer_id"))
print(pd.merge(customers, orders, on="customer_id", how="left"))
```

| `how=` | Keeps |
|--------|-------|
| `"inner"` (default) | rows with a match in both tables |
| `"left"` | every row of the left table |
| `"right"` | every row of the right table |
| `"outer"` | every row of both |

## concat: stack tables

When two tables have the same columns, `pd.concat()` puts one under the other:

```python tryit
import pandas as pd

january = pd.DataFrame({"product": ["Pen", "Lamp"], "units": [30, 4]})
february = pd.DataFrame({"product": ["Pen", "Mug"], "units": [25, 9]})
year = pd.concat([january, february], ignore_index=True)
print(year)
print(year.groupby("product")["units"].sum())
```

## Saving results

```python tryit
import pandas as pd

report = pd.DataFrame({"product": ["Pen", "Lamp"], "units": [55, 4]})
report.to_csv("report.csv", index=False)
print(open("report.csv").read())
```

`index=False` leaves out the row numbers. `to_excel()` and `to_json()` work the same way.

## Summary

- `pd.merge(a, b, on="key", how=...)` joins tables.
- `pd.concat([a, b])` stacks tables with the same columns.
- `to_csv()` saves the result.

```exercise
{
  "title": "Spending per customer",
  "prompt_md": "Merge `orders` with `customers`, then print the total `price` per customer `name` as a dictionary. The output must be exactly `{'Amara': 7, 'Ben': 35}`",
  "starter_code": "import pandas as pd\n\ncustomers = pd.DataFrame({\"customer_id\": [1, 2], \"name\": [\"Amara\", \"Ben\"]})\norders = pd.DataFrame({\"customer_id\": [1, 1, 2], \"price\": [2, 5, 35]})\n",
  "solution_code": "import pandas as pd\n\ncustomers = pd.DataFrame({\"customer_id\": [1, 2], \"name\": [\"Amara\", \"Ben\"]})\norders = pd.DataFrame({\"customer_id\": [1, 1, 2], \"price\": [2, 5, 35]})\njoined = pd.merge(orders, customers, on=\"customer_id\")\ntotals = joined.groupby(\"name\")[\"price\"].sum()\nprint({name: int(value) for name, value in totals.items()})",
  "check_type": "output",
  "expected_value": "{'Amara': 7, 'Ben': 35}",
  "hint": "pd.merge(orders, customers, on=\"customer_id\").groupby(\"name\")[\"price\"].sum()"
}
```

```quiz
{
  "title": "Final quiz: Python for Data Analysis",
  "final": true,
  "questions": [
    {"question": "What is np.array([2, 4]) + 1?", "options": ["[3 5]", "[2 4 1]", "An error"], "answer": 0, "explanation": "NumPy adds to every item."},
    {"question": "Which function loads a CSV file into a DataFrame?", "options": ["pd.read_csv()", "pd.open()", "pd.load()"], "answer": 0, "explanation": "read_csv reads a path, URL or text buffer."},
    {"question": "How do you keep rows where score is above 80?", "options": ["df[df[\"score\"] > 80]", "df.score > 80", "df.filter(80)"], "answer": 0, "explanation": "A boolean condition inside [] filters rows."},
    {"question": "Which call replaces missing values?", "options": ["fillna()", "dropna()", "isna()"], "answer": 0, "explanation": "fillna fills; dropna removes; isna detects."},
    {"question": "What does df.groupby(\"city\")[\"sales\"].sum() give?", "options": ["Total sales per city", "The number of cities", "The first sale per city"], "answer": 0, "explanation": "It sums sales within each city group."},
    {"question": "Which merge keeps every row of the left table?", "options": ["how=\"left\"", "how=\"inner\"", "how=\"right\""], "answer": 0, "explanation": "A left merge keeps all left rows, like LEFT JOIN."}
  ]
}
```
