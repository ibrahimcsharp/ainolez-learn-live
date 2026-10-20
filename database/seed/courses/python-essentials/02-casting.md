---
title: Python Type Conversion (Casting)
slug: casting
summary: Turn text into numbers and numbers into text with int(), float(), str() and bool().
minutes: 8
---
## Why convert?

Every value has a type. Some operations only work with the right type: you cannot add the text `"5"` to the number `3`.

```python tryit
print(type(5), type(5.0), type("5"), type(True))
print("5" + "3")   # joins text: 53
print(5 + 3)       # adds numbers: 8
```

Converting a value to another type is called **casting**. Each type has a function with the same name.

## int(): whole numbers

```python tryit
print(int("42") + 1)   # text to number
print(int(7.9))        # cuts off the decimals (does not round)
print(int(-7.9))
print(int(True))       # True is 1, False is 0
```

`int("4.5")` and `int("hello")` fail with a `ValueError`: the text must look like a whole number.

## float(): numbers with decimals

```python tryit
print(float("3.25") * 2)
print(float(10))
print(float("1e3"))   # scientific notation: 1000.0
```

## str(): text

`str()` turns anything into text. It is useful when you join values with `+`.

```python tryit
age = 30
print("I am " + str(age) + " years old")
print(str(3.5) + "!")
print(len(str(123456)))  # how many digits?
```

## bool(): true or false

Empty or zero values become `False`; everything else becomes `True`.

```python tryit
print(bool(0), bool(0.0), bool(""), bool([]))
print(bool(7), bool("no"), bool([0]))
```

## Converting safely

Text from users or files may not be a number. Check first, or catch the error.

```python tryit
for text in ["12", "seven", "3.5"]:
    if text.isdigit():
        print(text, "->", int(text))
    else:
        print(text, "-> not a whole number")
```

## Summary

- `int()`, `float()`, `str()` and `bool()` convert values.
- `int()` cuts decimals off; it does not round.
- Empty and zero values are `False`.

```exercise
{
  "title": "Add the prices",
  "prompt_md": "The prices arrive as text. Convert them and print their total as a number with decimals. The output must be `19.5`.",
  "starter_code": "a = \"12.25\"\nb = \"7.25\"\n",
  "solution_code": "a = \"12.25\"\nb = \"7.25\"\nprint(float(a) + float(b))",
  "check_type": "output",
  "expected_value": "19.5",
  "hint": "float(\"12.25\") turns the text into 12.25."
}
```

```quiz
[
  {"question": "What does int(9.99) give?", "options": ["10", "9", "9.99"], "answer": 1, "explanation": "int() removes the decimals without rounding."},
  {"question": "What does \"2\" + str(2) give?", "options": ["4", "\"22\"", "an error"], "answer": 1, "explanation": "Both are strings, so + joins them."},
  {"question": "Which value is False?", "options": ["bool(\"False\")", "bool(\"\")", "bool(-1)"], "answer": 1, "explanation": "Only the empty string is False; \"False\" is a non-empty string."}
]
```
