---
title: Python Numbers
slug: numbers
summary: Use whole numbers and decimals and calculate with Python's arithmetic operators.
minutes: 7
---
## Two kinds of numbers

Python has whole numbers called `int` and decimal numbers called `float`. `type()` tells you which one a value is.

```python tryit
print(type(7))
print(type(7.5))
```

## Arithmetic

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | add | `7 + 2` | `9` |
| `-` | subtract | `7 - 2` | `5` |
| `*` | multiply | `7 * 2` | `14` |
| `/` | divide | `7 / 2` | `3.5` |
| `//` | divide, drop the decimals | `7 // 2` | `3` |
| `%` | remainder | `7 % 2` | `1` |
| `**` | power | `7 ** 2` | `49` |

```python tryit
print(7 / 2)
print(7 // 2)
print(7 % 2)
print(2 ** 10)
```

`/` always gives a float, even when the result is whole: `6 / 3` is `2.0`.

## Order of operations

Like in maths, `*` and `/` come before `+` and `-`. Use brackets to choose the order.

```python tryit
print(2 + 3 * 4)
print((2 + 3) * 4)
```

## Rounding and converting

```python tryit
price = 19.987
print(round(price, 2))
print(int(9.99))     # cuts off the decimals
print(float(3))
print(abs(-12))
```

## Summary

- `int` is a whole number, `float` has decimals.
- `//` drops the decimals and `%` gives the remainder.
- Brackets control the order; `round()` rounds.

```exercise
{
  "title": "Minutes and seconds",
  "prompt_md": "A video is `200` seconds long. Use `//` and `%` to print the minutes and the seconds on one line, so the output is exactly `3 20`.",
  "starter_code": "seconds = 200\n",
  "solution_code": "seconds = 200\nprint(seconds // 60, seconds % 60)",
  "check_type": "output",
  "expected_value": "3 20",
  "hint": "There are 60 seconds in a minute. seconds // 60 gives whole minutes."
}
```

```quiz
[
  {"question": "What is 9 // 2?", "options": ["4.5", "4", "1"], "answer": 1, "explanation": "// divides and drops the decimal part."},
  {"question": "What is 9 % 2?", "options": ["1", "4", "0"], "answer": 0, "explanation": "% gives the remainder: 9 = 4 * 2 + 1."},
  {"question": "What type is 10 / 5?", "options": ["int", "float"], "answer": 1, "explanation": "The / operator always returns a float (2.0)."}
]
```
