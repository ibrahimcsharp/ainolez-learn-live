---
title: Python Output and Comments
slug: output
summary: Show text and numbers with print() and explain your code with comments.
minutes: 6
---
## Printing text and numbers

`print()` shows whatever you put between the brackets. Text must be inside quotes. Numbers do not need quotes.

```python tryit
print("Learning Python")
print(42)
print(3.5)
```

Each `print()` starts a new line.

## Printing several values

Separate values with commas. Python puts a space between them.

```python tryit
print("I am", 25, "years old")
```

You can change the separator with `sep`, and what comes at the end of the line with `end`:

```python tryit
print("2026", "10", "18", sep="-")
print("Loading", end="...")
print("done")
```

## Comments

A comment starts with `#`. Python ignores everything after it on that line. Use comments to explain *why* the code does something.

```python tryit
# Show a welcome message
print("Welcome!")  # this part is ignored too
# print("This line does not run")
```

!!! note
    Python cares about spelling and capitals: `print` works, `Print` gives an error.

## Summary

- `print()` shows values; commas print several values with spaces between them.
- `sep` changes the separator and `end` changes the line ending.
- `#` starts a comment.

```exercise
{
  "title": "Print a date",
  "prompt_md": "Use **one** `print()` with the values `\"18\"`, `\"10\"` and `\"2026\"` and `sep` so that it prints exactly `18/10/2026`",
  "starter_code": "print(\"18\", \"10\", \"2026\")",
  "solution_code": "print(\"18\", \"10\", \"2026\", sep=\"/\")",
  "check_type": "output",
  "expected_value": "18/10/2026",
  "hint": "Add sep=\"/\" after the last value."
}
```

```quiz
[
  {"question": "What does print(\"a\", \"b\") show?", "options": ["ab", "a b", "a,b"], "answer": 1, "explanation": "Commas print the values with one space between them."},
  {"question": "Which line is a comment?", "options": ["// hello", "# hello", "<!-- hello -->"], "answer": 1, "explanation": "In Python comments start with #."},
  {"question": "What does end=\"\" change?", "options": ["What is printed after the values", "The separator between values", "Nothing"], "answer": 0, "explanation": "end replaces the new line that print() normally adds at the end."}
]
```
