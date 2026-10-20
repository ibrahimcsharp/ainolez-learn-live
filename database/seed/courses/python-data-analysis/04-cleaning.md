---
title: Cleaning Data
slug: cleaning
summary: Find and fix missing values, duplicates, wrong types and messy text.
minutes: 9
---
## Real data is messy

Before analysing, check for missing values, duplicates, numbers stored as text and inconsistent spelling. Cleaning often takes most of an analyst's time.

## Missing values

pandas shows a missing value as `NaN` (or `None`).

```python tryit
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "name": ["Amara", "Ben", "Chen", "Dana"],
    "age": [21, np.nan, 28, 45],
    "city": ["Lagos", "London", None, "London"],
})
print(df.isna().sum())                 # missing values per column
print(df.dropna())                     # drop rows with any missing value
print(df.fillna({"age": df["age"].median(), "city": "unknown"}))
```

Dropping rows is simple but loses data; filling with a typical value keeps the row. Choose based on what the column means.

## Duplicates

```python tryit
import pandas as pd

orders = pd.DataFrame({"order": [101, 102, 102, 103], "item": ["Pen", "Lamp", "Lamp", "Mug"]})
print(orders.duplicated().sum(), "duplicate rows")
print(orders.drop_duplicates())
```

## Types and text

```python tryit
import pandas as pd

df = pd.DataFrame({
    "city": [" london", "London ", "LAGOS", "lagos"],
    "price": ["12", "8", "n/a", "30"],
    "day": ["2026-03-01", "2026-03-02", "2026-03-02", "2026-03-04"],
})
df["city"] = df["city"].str.strip().str.title()
df["price"] = pd.to_numeric(df["price"], errors="coerce")   # "n/a" becomes NaN
df["day"] = pd.to_datetime(df["day"])
print(df)
print(df.dtypes)
print(df["city"].value_counts())
```

## Renaming and dropping columns

```python
df = df.rename(columns={"price": "price_usd"})
df = df.drop(columns=["notes"])
```

## Summary

- `isna().sum()` counts missing values; `dropna()` and `fillna()` handle them.
- `drop_duplicates()` removes repeated rows.
- `.str` methods clean text; `to_numeric` and `to_datetime` fix types.

```exercise
{
  "title": "Fill the gaps",
  "prompt_md": "Fill the missing `score` values with `0`, then print the **sum** of the column as an integer. The output must be exactly `150`",
  "starter_code": "import numpy as np\nimport pandas as pd\n\ndf = pd.DataFrame({\"score\": [70, np.nan, 80, np.nan]})\n",
  "solution_code": "import numpy as np\nimport pandas as pd\n\ndf = pd.DataFrame({\"score\": [70, np.nan, 80, np.nan]})\ndf[\"score\"] = df[\"score\"].fillna(0)\nprint(int(df[\"score\"].sum()))",
  "check_type": "output",
  "expected_value": "150",
  "hint": "df[\"score\"].fillna(0), then int(...sum())"
}
```

```quiz
[
  {"question": "Which call counts the missing values in each column?", "options": ["df.isna().sum()", "df.count_nan()", "df.missing()"], "answer": 0, "explanation": "isna() marks missing values; sum() counts them."},
  {"question": "What does pd.to_numeric(col, errors=\"coerce\") do with \"n/a\"?", "options": ["Turns it into NaN", "Raises an error", "Turns it into 0"], "answer": 0, "explanation": "coerce replaces values it cannot convert with NaN."}
]
```
