---
title: Python Raising and Custom Exceptions
slug: exceptions
summary: The exception family tree, raise with a clear message, write your own exception classes, re-raise and chain errors, and clean up with finally and with.
minutes: 13
---
## A quick recap

`try` runs code that might fail, `except` handles a failure, `else` runs only when nothing failed and `finally` always runs.

```python tryit
def read_number(text):
    try:
        value = int(text)
    except ValueError:
        print(f"{text!r} is not a whole number")
    else:
        print("got", value)
    finally:
        print("checked", repr(text))

read_number("12")
read_number("twelve")
```

## The exception family tree

Exceptions are classes, and they are arranged in a tree. Catching a parent class also catches all of its children.

```
BaseException
 └── Exception
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── ValueError
      ├── TypeError
      └── OSError
           └── FileNotFoundError
```

```python tryit
data = {"a": 1}
for attempt in [lambda: [1, 2][5], lambda: data["z"]]:
    try:
        attempt()
    except LookupError as error:
        print(type(error).__name__, "caught as a LookupError")
```

Catch the **most specific** class you can. A bare `except:` or `except Exception:` hides typing mistakes and real bugs.

## Catching several types at once

Put the classes in a tuple, and use `as` to get the exception object.

```python tryit
def safe_ratio(a, b):
    try:
        return a / b
    except (ZeroDivisionError, TypeError) as error:
        print("problem:", type(error).__name__, "-", error)
        return None

print(safe_ratio(6, 3))
print(safe_ratio(6, 0))
print(safe_ratio(6, "3"))
```

## raise: report a problem yourself

When your function gets a value it cannot work with, `raise` an exception with a message that says what went wrong. Pick the built-in class that fits: `ValueError` for a bad value, `TypeError` for a wrong type.

```python tryit
def set_volume(level):
    if not isinstance(level, int):
        raise TypeError(f"level must be an int, not {type(level).__name__}")
    if not 0 <= level <= 10:
        raise ValueError(f"level must be 0 to 10, got {level}")
    return level

for value in [7, 15, "loud"]:
    try:
        print("volume", set_volume(value))
    except (TypeError, ValueError) as error:
        print("rejected:", error)
```

## Your own exception classes

For errors that belong to your program, make a class that inherits from `Exception` (or from a fitting built-in like `ValueError`). A small family of your own lets callers catch all of them at once.

```python tryit
class ShopError(Exception):
    """Something went wrong in the shop."""

class OutOfStock(ShopError):
    def __init__(self, item):
        super().__init__(f"sorry, {item} is sold out")
        self.item = item

class CardDeclined(ShopError):
    pass

stock = {"tea": 3, "mug": 0}

def buy(item):
    if stock.get(item, 0) == 0:
        raise OutOfStock(item)
    stock[item] -= 1
    return f"bought {item}"

for item in ["tea", "mug"]:
    try:
        print(buy(item))
    except ShopError as error:
        print("ShopError:", error)
```

## Re-raising and chaining

Inside `except`, a plain `raise` sends the same exception on after you have done something with it, such as logging. `raise New(...) from error` replaces a low-level error with one that makes sense to the caller, while keeping the original as the cause.

```python tryit
class ConfigError(Exception):
    pass

def read_port(settings):
    try:
        return int(settings["port"])
    except (KeyError, ValueError) as error:
        raise ConfigError("the port setting is missing or not a number") from error

try:
    read_port({"port": "eighty"})
except ConfigError as error:
    print("ConfigError:", error)
    print("caused by:", repr(error.__cause__))
```

## Cleaning up: finally and with

`finally` is the place for clean-up that must happen whether or not there was an error. For files and other resources, a `with` block does the clean-up for you.

```python tryit
log = []

def process(job):
    log.append(f"start {job}")
    try:
        if job == "bad":
            raise RuntimeError("job failed")
        return f"{job} done"
    finally:
        log.append(f"end {job}")     # runs even after the error

for job in ["good", "bad"]:
    try:
        print(process(job))
    except RuntimeError as error:
        print("error:", error)
print(log)
```

## assert: checks for the programmer

`assert condition, message` raises `AssertionError` when the condition is false. Use it to catch your own mistakes while developing, not to check user input: Python skips asserts when run with the `-O` option.

```python tryit
def average(numbers):
    assert len(numbers) > 0, "average() needs at least one number"
    return sum(numbers) / len(numbers)

print(average([2, 4]))
try:
    average([])
except AssertionError as error:
    print("AssertionError:", error)
```

## Summary

- Exceptions form a class tree; catching a parent catches its children.
- Catch specific classes; group several in a tuple.
- `raise ValueError("clear message")` reports bad input.
- Subclass `Exception` to make your own error family.
- `raise` re-raises; `raise New(...) from error` chains.
- `finally` and `with` guarantee clean-up.

```exercise
{
  "title": "Validate an age",
  "prompt_md": "Write `check_age(age)` that raises `ValueError` with the message `age must be between 0 and 130` when `age` is outside 0 to 130, and otherwise returns `age`. The loop below must print:\n\n```\n42\nage must be between 0 and 130\nage must be between 0 and 130\n```",
  "starter_code": "def check_age(age):\n    pass\n\nfor age in [42, -1, 200]:\n    try:\n        print(check_age(age))\n    except ValueError as error:\n        print(error)",
  "solution_code": "def check_age(age):\n    if not 0 <= age <= 130:\n        raise ValueError(\"age must be between 0 and 130\")\n    return age\n\nfor age in [42, -1, 200]:\n    try:\n        print(check_age(age))\n    except ValueError as error:\n        print(error)",
  "check_type": "output",
  "expected_value": "42\nage must be between 0 and 130\nage must be between 0 and 130",
  "hint": "if not 0 <= age <= 130: raise ValueError(\"age must be between 0 and 130\")"
}
```

```exercise
{
  "title": "Your own exception",
  "prompt_md": "Create `class InsufficientFunds(Exception)`. Make `withdraw(balance, amount)` raise it with the message `need 30 more` when the amount is bigger than the balance (the number is `amount - balance`), and otherwise return the new balance. The code below must print:\n\n```\n50\nInsufficientFunds: need 30 more\n```",
  "starter_code": "def withdraw(balance, amount):\n    pass\n\nprint(withdraw(80, 30))\ntry:\n    withdraw(20, 50)\nexcept InsufficientFunds as error:\n    print(\"InsufficientFunds:\", error)",
  "solution_code": "class InsufficientFunds(Exception):\n    pass\n\ndef withdraw(balance, amount):\n    if amount > balance:\n        raise InsufficientFunds(f\"need {amount - balance} more\")\n    return balance - amount\n\nprint(withdraw(80, 30))\ntry:\n    withdraw(20, 50)\nexcept InsufficientFunds as error:\n    print(\"InsufficientFunds:\", error)",
  "check_type": "output",
  "expected_value": "50\nInsufficientFunds: need 30 more",
  "hint": "class InsufficientFunds(Exception): pass - then raise InsufficientFunds(f\"need {amount - balance} more\")."
}
```

```quiz
[
  {"question": "except LookupError catches which of these?", "options": ["Only LookupError", "IndexError and KeyError too", "Every exception"], "answer": 1, "explanation": "IndexError and KeyError are children of LookupError."},
  {"question": "Which class should your own exception inherit from?", "options": ["BaseException", "Exception", "object"], "answer": 1, "explanation": "Exception is the base for normal program errors; BaseException also covers things like Ctrl+C."},
  {"question": "What does a plain raise inside an except block do?", "options": ["Raises a new empty error", "Sends the same exception on", "Ignores the error"], "answer": 1, "explanation": "A bare raise re-raises the exception being handled."},
  {"question": "Why not use assert to check user input?", "options": ["assert is slow", "Asserts are skipped when Python runs with -O", "assert only works in tests"], "answer": 1, "explanation": "Optimised runs remove assert statements, so the check would disappear."}
]
```
