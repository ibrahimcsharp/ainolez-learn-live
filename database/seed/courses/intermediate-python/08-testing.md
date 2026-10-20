---
title: Testing Your Code
slug: testing
summary: Check that code works with assert and write automated tests with pytest.
minutes: 9
---
## Why test?

A test is code that checks other code. Tests catch mistakes early and let you change code without fear: if the tests still pass, you did not break anything.

## assert

`assert condition` does nothing when the condition is true and raises `AssertionError` when it is false.

```python tryit
def add_vat(price, rate=0.2):
    return round(price * (1 + rate), 2)

assert add_vat(100) == 120.0
assert add_vat(10, rate=0.05) == 10.5
print("All checks passed")
```

Change `120.0` to `121` and run again to see a failing check.

## Testing edge cases

Good tests try the unusual inputs, not just the happy path.

```python tryit
def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

assert average([2, 4]) == 3
assert average([5]) == 5
assert average([]) == 0          # edge case: empty list
print("average() works")
```

## pytest

On your computer, `pytest` finds and runs tests for you. Put functions whose names start with `test_` in files whose names start with `test_`:

```python
# test_prices.py
import pytest
from prices import add_vat

def test_default_rate():
    assert add_vat(100) == 120.0

def test_custom_rate():
    assert add_vat(10, rate=0.05) == 10.5

def test_negative_price_is_refused():
    with pytest.raises(ValueError):
        add_vat(-1)
```

```
pip install pytest
pytest
```

pytest prints a dot for each passing test and a clear report for each failure, showing the values on both sides of the failed `assert`.

!!! tip
    Write a test when you fix a bug. The bug can then never come back without you noticing.

## Summary

- `assert` checks a condition and fails loudly when it is false.
- Test normal cases and edge cases such as empty or negative input.
- pytest runs every `test_` function and reports failures clearly.

```exercise
{
  "title": "Fix the function",
  "prompt_md": "The `is_leap` function has a bug, so an `assert` fails. A year is a leap year if it is divisible by 4, **except** years divisible by 100 that are not divisible by 400. Fix the function so all checks pass and the program prints exactly `ok`.",
  "starter_code": "def is_leap(year):\n    return year % 4 == 0\n\nassert is_leap(2024)\nassert not is_leap(1900)\nassert is_leap(2000)\nprint(\"ok\")",
  "solution_code": "def is_leap(year):\n    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n\nassert is_leap(2024)\nassert not is_leap(1900)\nassert is_leap(2000)\nprint(\"ok\")",
  "check_type": "output",
  "expected_value": "ok",
  "hint": "year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)"
}
```

```quiz
{
  "title": "Final quiz: Intermediate Python",
  "final": true,
  "questions": [
    {"question": "What does [n for n in range(6) if n % 3 == 0] give?", "options": ["[0, 3]", "[3]", "[0, 3, 6]"], "answer": 0, "explanation": "range(6) stops at 5; 0 and 3 are divisible by 3."},
    {"question": "What does key= do in sorted()?", "options": ["Sets the sort direction", "Says what to compare for each item", "Removes duplicates"], "answer": 1, "explanation": "key is a function applied to each item before comparing."},
    {"question": "What does super().__init__(...) do in a child class?", "options": ["Creates a new class", "Runs the parent's __init__", "Deletes the parent"], "answer": 1, "explanation": "super() reaches the parent class."},
    {"question": "Which keyword makes a generator?", "options": ["yield", "return", "lambda"], "answer": 0, "explanation": "yield pauses the function and hands out a value."},
    {"question": "What does a decorator return?", "options": ["Nothing", "A new function that wraps the original", "A class"], "answer": 1, "explanation": "The returned wrapper replaces the original function."},
    {"question": "Which function names does pytest run?", "options": ["Names starting with test_", "Names ending with _check", "Every function"], "answer": 0, "explanation": "pytest collects functions named test_..."}
  ]
}
```
