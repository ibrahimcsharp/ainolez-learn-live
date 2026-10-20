---
title: Selecting and Filtering
slug: selecting
summary: Pick columns and rows with [], loc and iloc, filter with conditions and sort.
minutes: 8
---
## Columns

```python tryit
import pandas as pd

people = pd.DataFrame({
    "name": ["Amara", "Ben", "Chen", "Dana", "Eli"],
    "age": [21, 34, 28, 45, 19],
    "city": ["Lagos", "London", "Beijing", "London", "Lagos"],
    "score": [88, 72, 95, 64, 81],
})
print(people["name"])               # one column (a Series)
print(people[["name", "score"]])    # several columns (a DataFrame)
```

## Filtering rows

A condition gives `True`/`False` for each row. Put it in `[ ]` to keep the matching rows:

```python tryit
import pandas as pd

people = pd.DataFrame({
    "name": ["Amara", "Ben", "Chen", "Dana", "Eli"],
    "age": [21, 34, 28, 45, 19],
    "city": ["Lagos", "London", "Beijing", "London", "Lagos"],
    "score": [88, 72, 95, 64, 81],
})
print(people[people["score"] > 80])
print(people[(people["city"] == "London") & (people["age"] > 30)])
print(people[people["city"].isin(["Lagos", "Beijing"])])
```

Use `&` (and), `|` (or) and `~` (not), and put each condition in brackets.

## loc and iloc

- `loc[rows, columns]` selects by **labels** and conditions.
- `iloc[rows, columns]` selects by **position**, like list indexes.

```python tryit
import pandas as pd

people = pd.DataFrame({
    "name": ["Amara", "Ben", "Chen"],
    "age": [21, 34, 28],
    "score": [88, 72, 95],
})
print(people.loc[people["age"] < 30, ["name", "score"]])
print(people.iloc[0])          # first row
print(people.iloc[:2, 1:])     # first two rows, columns from the second on
```

## Sorting

```python tryit
import pandas as pd

people = pd.DataFrame({"name": ["Amara", "Ben", "Chen", "Dana"], "score": [88, 72, 95, 64]})
print(people.sort_values("score", ascending=False))
print(people.nlargest(2, "score"))
```

## Summary

- `df["col"]` and `df[["a", "b"]]` select columns.
- `df[condition]` filters rows; combine with `&` and `|`.
- `loc` uses labels, `iloc` uses positions; `sort_values()` sorts.

```exercise
{
  "title": "Top Londoners",
  "prompt_md": "Print the `name`s of people from `London` with a score **of 70 or more**, as a list. The output must be exactly `['Ben', 'Fay']`",
  "starter_code": "import pandas as pd\n\npeople = pd.DataFrame({\n    \"name\": [\"Amara\", \"Ben\", \"Dana\", \"Fay\"],\n    \"city\": [\"Lagos\", \"London\", \"London\", \"London\"],\n    \"score\": [88, 72, 64, 90],\n})\n",
  "solution_code": "import pandas as pd\n\npeople = pd.DataFrame({\n    \"name\": [\"Amara\", \"Ben\", \"Dana\", \"Fay\"],\n    \"city\": [\"Lagos\", \"London\", \"London\", \"London\"],\n    \"score\": [88, 72, 64, 90],\n})\nchosen = people[(people[\"city\"] == \"London\") & (people[\"score\"] >= 70)]\nprint(chosen[\"name\"].tolist())",
  "check_type": "output",
  "expected_value": "['Ben', 'Fay']",
  "hint": "people[(people[\"city\"] == \"London\") & (people[\"score\"] >= 70)][\"name\"].tolist()"
}
```

```quiz
[
  {"question": "How do you combine two conditions with AND in pandas?", "options": ["(a) & (b)", "a and b", "a && b"], "answer": 0, "explanation": "pandas uses & with brackets around each condition."},
  {"question": "What does df.iloc[0] return?", "options": ["The first row", "The column named 0", "The first column"], "answer": 0, "explanation": "iloc selects by position."}
]
```
