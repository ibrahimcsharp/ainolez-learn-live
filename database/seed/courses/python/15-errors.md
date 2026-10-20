---
title: Python Errors and Exceptions
slug: errors
summary: Read error messages and handle problems with try and except so programs keep running.
minutes: 8
---
## Reading an error

When Python cannot run a line, it stops and shows an error. The **last line** tells you the type of error and why.

```python tryit
numbers = [1, 2, 3]
print(numbers[5])
```

`IndexError: list index out of range` means there is no item at position 5.

Common errors:

| Error | Usual cause |
|---|---|
| `SyntaxError` | a typo: missing bracket, quote or colon |
| `NameError` | a name that does not exist (often a spelling mistake) |
| `TypeError` | a wrong type, like `"5" + 2` |
| `ValueError` | a right type but wrong value, like `int("five")` |
| `ZeroDivisionError` | dividing by zero |

## try and except

`try` runs code that might fail. If it fails, the `except` block runs instead of stopping the program.

```python tryit
text = "five"
try:
    number = int(text)
    print("Number:", number)
except ValueError:
    print(f"'{text}' is not a number")
print("The program goes on")
```

## Several errors, else and finally

```python tryit
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "cannot divide by zero"
    except TypeError:
        return "use numbers only"
    else:
        return result          # runs only when there was no error
    finally:
        print("checked", a, b)  # always runs

print(divide(10, 2))
print(divide(1, 0))
```

## Raising your own errors

```python tryit
def set_age(age):
    if age < 0:
        raise ValueError("age cannot be negative")
    return age

try:
    set_age(-3)
except ValueError as error:
    print("Error:", error)
```

## Summary

- The last line of an error message names the error and the reason.
- `try` / `except` handles errors; `else` runs on success, `finally` always.
- `raise` signals a problem in your own code.

```exercise
{
  "title": "Safe conversion",
  "prompt_md": "Convert each item to an `int`. Skip items that are not numbers by catching `ValueError`. Print the total of the numbers; the output must be exactly `15`.",
  "starter_code": "items = [\"4\", \"x\", \"5\", \"six\", \"6\"]\ntotal = 0\nfor item in items:\n    total += int(item)\nprint(total)",
  "solution_code": "items = [\"4\", \"x\", \"5\", \"six\", \"6\"]\ntotal = 0\nfor item in items:\n    try:\n        total += int(item)\n    except ValueError:\n        pass\nprint(total)",
  "check_type": "output",
  "expected_value": "15",
  "hint": "Wrap total += int(item) in try, and use except ValueError: pass."
}
```

```quiz
[
  {"question": "Which part of an error message is most useful first?", "options": ["The first line", "The last line", "The file name"], "answer": 1, "explanation": "The last line has the error type and message."},
  {"question": "When does a finally block run?", "options": ["Only after an error", "Only without an error", "Always"], "answer": 2, "explanation": "finally runs whether or not an error happened."}
]
```
