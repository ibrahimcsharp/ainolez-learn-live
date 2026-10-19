---
title: pandas DataFrames
slug: dataframes
summary: Create DataFrames, load CSV data and get a first overview with head, info and describe.
minutes: 8
---
## Series and DataFrame

pandas has two main types:

- a **Series**: one column of values with an index,
- a **DataFrame**: a table of named columns, like a spreadsheet or an SQL table.

```python tryit
import pandas as pd

df = pd.DataFrame({
    "name": ["Amara", "Ben", "Chen", "Dana"],
    "age": [21, 34, 28, 45],
    "city": ["Lagos", "London", "Beijing", "London"],
})
print(df)
print(df["age"])        # one column is a Series
```

## Loading a CSV file

Real data usually comes from a file. `pd.read_csv()` reads a path or URL; here we read text so the example works anywhere:

```python tryit
import io
import pandas as pd

csv = """date,product,units,price
2026-01-03,Pen,30,2
2026-01-03,Notebook,12,5
2026-01-04,Pen,18,2
2026-01-05,Backpack,3,35
2026-01-05,Notebook,9,5
"""
sales = pd.read_csv(io.StringIO(csv), parse_dates=["date"])
print(sales.head(3))
print(sales.shape)        # (rows, columns)
```

## A first look

These four calls are the start of every analysis:

```python tryit
import io
import pandas as pd

csv = """product,units,price
Pen,30,2
Notebook,12,5
Pen,18,2
Backpack,3,35
Notebook,9,5
"""
sales = pd.read_csv(io.StringIO(csv))
sales.info()                 # column types and missing values
print(sales.describe())      # count, mean, min, max...
print(sales.columns.tolist())
print(sales["product"].value_counts())
```

## New columns

Column maths works like NumPy, row by row:

```python tryit
import pandas as pd

sales = pd.DataFrame({"product": ["Pen", "Notebook", "Backpack"], "units": [30, 12, 3], "price": [2, 5, 35]})
sales["revenue"] = sales["units"] * sales["price"]
print(sales)
print("Total revenue:", sales["revenue"].sum())
```

## Summary

- A DataFrame is a table; each column is a Series.
- `pd.read_csv()` loads data.
- `head()`, `shape`, `info()`, `describe()` and `value_counts()` give an overview.

```exercise
{
  "title": "Total units",
  "prompt_md": "Add a column `revenue` (= `units * price`) and print the **sum** of `revenue`. The output must be exactly `225`",
  "starter_code": "import pandas as pd\n\nsales = pd.DataFrame({\"units\": [30, 12, 3], \"price\": [2, 5, 35]})\n",
  "solution_code": "import pandas as pd\n\nsales = pd.DataFrame({\"units\": [30, 12, 3], \"price\": [2, 5, 35]})\nsales[\"revenue\"] = sales[\"units\"] * sales[\"price\"]\nprint(sales[\"revenue\"].sum())",
  "check_type": "output",
  "expected_value": "225",
  "hint": "sales[\"revenue\"] = sales[\"units\"] * sales[\"price\"]"
}
```

```quiz
[
  {"question": "What is one column of a DataFrame?", "options": ["A Series", "A list", "An array of rows"], "answer": 0, "explanation": "Each column is a pandas Series."},
  {"question": "Which method summarises numeric columns with mean, min and max?", "options": ["describe()", "head()", "shape"], "answer": 0, "explanation": "describe() gives summary statistics."}
]
```
