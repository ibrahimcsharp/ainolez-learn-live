---
title: Python Variables
slug: variables
summary: Store values in named variables, change them and follow the naming rules.
minutes: 7
---
## What is a variable?

A variable is a name for a value. You create one with `=`:

```python tryit
name = "Amina"
age = 21
print(name)
print(age)
```

Read `name = "Amina"` as "name gets the value Amina". The `=` sign stores; it does not compare.

## Changing a variable

A variable can get a new value at any time. The old value is replaced.

```python tryit
score = 10
print(score)
score = score + 5
print(score)
```

The line `score = score + 5` first works out the right side (10 + 5), then stores the result back in `score`.

## Several variables at once

```python tryit
x, y, z = 1, 2, 3
print(x, y, z)

a = b = 0
print(a, b)
```

## Naming rules

- Names can contain letters, digits and `_`, but cannot start with a digit.
- Names are case sensitive: `age` and `Age` are two different variables.
- Use clear names in lowercase with underscores: `total_price`, not `tp`.
- You cannot use Python words such as `if`, `for` or `class` as names.

```python
user_name = "ok"     # good
2nd_place = "no"     # error: starts with a digit
```

## Summary

- `=` stores a value in a variable.
- A variable can be given a new value later.
- Good names make code easy to read.

```exercise
{
  "title": "Swap two values",
  "prompt_md": "The program starts with `a = 5` and `b = 9`. Swap them so that `print(a, b)` shows exactly `9 5`.",
  "starter_code": "a = 5\nb = 9\n# swap a and b here\n\nprint(a, b)",
  "solution_code": "a = 5\nb = 9\na, b = b, a\nprint(a, b)",
  "check_type": "output",
  "expected_value": "9 5",
  "hint": "Python can assign two variables in one line: a, b = ..., ..."
}
```

```quiz
[
  {"question": "After x = 4 and then x = x * 2, what is x?", "options": ["4", "8", "x * 2"], "answer": 1, "explanation": "The right side is worked out first (4 * 2), then stored in x."},
  {"question": "Which is a valid variable name?", "options": ["total-price", "2total", "total_price"], "answer": 2, "explanation": "Names use letters, digits and underscores and cannot start with a digit."},
  {"question": "Are score and Score the same variable?", "options": ["Yes", "No"], "answer": 1, "explanation": "Python names are case sensitive."}
]
```
