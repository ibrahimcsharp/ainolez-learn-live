---
title: Python Functions
slug: functions
summary: Write your own functions with parameters and return values, and reuse them.
minutes: 10
---
## Why functions?

A function is a named block of code you can run whenever you need it. Functions avoid copy-paste and make programs easier to read.

```python tryit
def greet():
    print("Hello!")
    print("Welcome to ainolez")

greet()
greet()
```

`def` defines the function; `greet()` calls (runs) it.

## Parameters

Parameters let you pass values into a function.

```python tryit
def greet(name):
    print(f"Hello, {name}!")

greet("Sara")
greet("Tom")
```

## Returning a value

`return` sends a result back to the caller. The caller can store or print it.

```python tryit
def area(width, height):
    return width * height

room = area(4, 5)
print(room)
print(area(2, 3) + area(1, 1))
```

!!! note
    `print()` only shows a value. `return` hands the value back so the rest of the program can use it.

## Default and keyword arguments

```python tryit
def price_with_tax(price, tax=0.2):
    return round(price * (1 + tax), 2)

print(price_with_tax(10))            # uses the default tax
print(price_with_tax(10, tax=0.05))  # keyword argument
```

## Scope

Variables created inside a function exist only inside it.

```python tryit
def make_total():
    total = 99
    return total

print(make_total())
# print(total) would fail: total only lives inside the function
```

## Summary

- `def name(parameters):` creates a function; `name()` calls it.
- `return` gives a result back.
- Parameters can have defaults, and arguments can be passed by name.

```exercise
{
  "title": "Celsius to Fahrenheit",
  "prompt_md": "Write a function `to_fahrenheit(celsius)` that **returns** `celsius * 9 / 5 + 32`. The program then prints `to_fahrenheit(25)`, which must show exactly `77.0`.",
  "starter_code": "def to_fahrenheit(celsius):\n    pass\n\nprint(to_fahrenheit(25))",
  "solution_code": "def to_fahrenheit(celsius):\n    return celsius * 9 / 5 + 32\n\nprint(to_fahrenheit(25))",
  "check_type": "output",
  "expected_value": "77.0",
  "hint": "Replace pass with a return line."
}
```

```quiz
[
  {"question": "Which keyword creates a function?", "options": ["function", "def", "fn"], "answer": 1, "explanation": "Python functions start with def."},
  {"question": "What does a function without return give back?", "options": ["0", "None", "an error"], "answer": 1, "explanation": "Without return a function returns None."},
  {"question": "def f(x, y=2): return x * y. What is f(5)?", "options": ["5", "10", "7"], "answer": 1, "explanation": "y uses its default 2, so 5 * 2 = 10."}
]
```
