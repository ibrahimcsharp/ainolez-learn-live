---
title: Decorators
slug: decorators
summary: Wrap functions with decorators to add behaviour such as timing, logging or caching.
minutes: 9
---
## Functions are values

In Python a function can be stored in a variable, passed to another function and returned from one.

```python tryit
def shout(text):
    return text.upper() + "!"

def apply(function, value):
    return function(value)

print(apply(shout, "hello"))
```

## A first decorator

A **decorator** is a function that takes a function and returns a new function that wraps it.

```python tryit
def announce(function):
    def wrapper(*args, **kwargs):
        print(f"Calling {function.__name__}...")
        result = function(*args, **kwargs)
        print("Done")
        return result
    return wrapper

@announce
def add(a, b):
    return a + b

print(add(2, 3))
```

`@announce` above `add` means `add = announce(add)`. `*args` and `**kwargs` pass any arguments through.

## Keeping the name: functools.wraps

```python tryit
import functools

def announce(function):
    @functools.wraps(function)        # keeps the name and docstring
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper

@announce
def greet():
    "Say hello."
    return "hi"

print(greet.__name__, "-", greet.__doc__)
```

## Useful built-in decorators

`functools.lru_cache` remembers results, which makes repeated work fast:

```python tryit
from functools import lru_cache

@lru_cache
def fibonacci(n):
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(80))
```

Without the cache this would take far too long. You have also met `@dataclass`; web frameworks use decorators such as `@app.route("/")` for URLs.

## Decorators with arguments

```python tryit
def repeat(times):
    def decorator(function):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                function(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def cheer():
    print("Go!")

cheer()
```

## Summary

- A decorator takes a function and returns a wrapped version.
- `@name` above a function applies it; use `functools.wraps` in wrappers.
- `lru_cache` and `dataclass` are decorators you will use often.

```exercise
{
  "title": "Double the result",
  "prompt_md": "Write a decorator `doubled` whose wrapper returns **twice** the result of the decorated function. The program prints `ten()`, which must show exactly `20`.",
  "starter_code": "def doubled(function):\n    def wrapper(*args, **kwargs):\n        pass\n    return wrapper\n\n@doubled\ndef ten():\n    return 10\n\nprint(ten())",
  "solution_code": "def doubled(function):\n    def wrapper(*args, **kwargs):\n        return 2 * function(*args, **kwargs)\n    return wrapper\n\n@doubled\ndef ten():\n    return 10\n\nprint(ten())",
  "check_type": "output",
  "expected_value": "20",
  "hint": "Inside wrapper: return 2 * function(*args, **kwargs)"
}
```

```quiz
[
  {"question": "@log above def f(): ... is the same as...", "options": ["f = log(f)", "log = f(log)", "f(log)"], "answer": 0, "explanation": "The decorator is called with the function and replaces it."},
  {"question": "What does lru_cache do?", "options": ["Logs every call", "Remembers results for the same arguments", "Runs the function in parallel"], "answer": 1, "explanation": "It caches return values so repeated calls are instant."}
]
```
