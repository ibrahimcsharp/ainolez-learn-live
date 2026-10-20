---
title: Python Booleans and Comparisons
slug: booleans
summary: Compare values, combine conditions with and, or, not, and convert between types.
minutes: 7
---
## True or False

A boolean (`bool`) is either `True` or `False`. Comparisons give booleans.

```python tryit
print(5 > 3)
print(5 == 3)
print("cat" != "dog")
```

| Operator | Meaning |
|---|---|
| `==` | equal |
| `!=` | not equal |
| `>`, `<` | greater, less |
| `>=`, `<=` | greater or equal, less or equal |

!!! warning
    `=` stores a value, `==` compares two values. Mixing them up is the most common beginner mistake.

## Combining conditions

```python tryit
age = 20
has_ticket = True
print(age >= 18 and has_ticket)   # both must be True
print(age < 12 or age > 65)        # at least one must be True
print(not has_ticket)              # flips True and False
```

## Converting types

Values from forms and files usually arrive as text. Convert them before calculating.

```python tryit
text = "42"
number = int(text)
print(number + 8)
print(float("2.5") * 2)
print(str(100) + "%")
print(bool(0), bool(7), bool(""), bool("hi"))
```

Empty values (`0`, `""`, empty lists) count as `False`; everything else counts as `True`.

## Summary

- Comparisons such as `==` and `>` give `True` or `False`.
- `and`, `or` and `not` combine conditions.
- `int()`, `float()`, `str()` and `bool()` convert values.

```exercise
{
  "title": "Can they vote?",
  "prompt_md": "Print whether a person can vote: they must be at least `18` **and** be a citizen. With the values given, the output must be exactly `False`.",
  "starter_code": "age = 17\ncitizen = True\n",
  "solution_code": "age = 17\ncitizen = True\nprint(age >= 18 and citizen)",
  "check_type": "output",
  "expected_value": "False",
  "hint": "Use >= and the word and."
}
```

```quiz
[
  {"question": "What is 3 == 3.0?", "options": ["True", "False"], "answer": 0, "explanation": "The values are equal, even though one is an int and one a float."},
  {"question": "What is True and False?", "options": ["True", "False"], "answer": 1, "explanation": "and needs both sides to be True."},
  {"question": "What is int(\"7\") + 3?", "options": ["73", "10", "an error"], "answer": 1, "explanation": "int() turns the text \"7\" into the number 7."}
]
```
