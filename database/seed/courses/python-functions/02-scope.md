---
title: Python Scope
slug: scope
summary: Where a variable can be seen - local, enclosing, global and built-in scope - and when to use the global and nonlocal keywords.
minutes: 10
---
## What scope means

The **scope** of a name is the part of the program where that name can be used. A variable made inside a function is **local**: it exists only while the function runs and cannot be seen outside it.

```python tryit
def bake():
    flavour = "lemon"      # local to bake()
    print("baking", flavour)

bake()
# print(flavour)   # NameError: flavour only exists inside bake()
```

Each call gets fresh local variables, and two functions can use the same local name without clashing.

## Global variables

A variable made at the top level of a file is **global**. Functions can **read** it.

```python tryit
site_name = "ainolez"     # global

def footer():
    return f"(c) {site_name}"

print(footer())
```

## Assigning creates a local name

If a function **assigns** to a name, Python treats that name as local for the whole function, even if a global with the same name exists. The global is left alone.

```python tryit
level = 1

def level_up():
    level = 2            # a new local variable, not the global
    print("inside:", level)

level_up()
print("outside:", level)  # still 1
```

Reading the global first and then assigning to it gives an `UnboundLocalError`, because Python already decided the name is local:

```python tryit
counter = 0

def increase():
    try:
        counter = counter + 1
    except UnboundLocalError as error:
        print("Error:", error)

increase()
```

## The global keyword

`global name` tells Python that assignments inside the function should change the **global** variable.

```python tryit
visits = 0

def record_visit():
    global visits
    visits += 1

record_visit()
record_visit()
print(visits)   # 2
```

Use `global` sparingly. A function that returns a new value is easier to test and reuse:

```python tryit
def add_visit(visits):
    return visits + 1

visits = 0
visits = add_visit(visits)
print(visits)
```

## Enclosing scope and nonlocal

A function defined inside another function can read the outer function's variables. That outer layer is the **enclosing** scope. To **change** one of those variables, declare it `nonlocal`.

```python tryit
def make_counter():
    count = 0                 # enclosing variable

    def step():
        nonlocal count        # change the outer count, not a new local
        count += 1
        return count

    return step

tick = make_counter()
print(tick(), tick(), tick())   # 1 2 3

other = make_counter()
print(other())                  # 1: its own count
```

## The LEGB rule

When Python meets a name, it looks in four places, in this order, and uses the first one it finds:

1. **L**ocal - inside the current function
2. **E**nclosing - inside any outer functions
3. **G**lobal - at the top level of the file
4. **B**uilt-in - names Python always has, like `print`, `len` and `max`

```python tryit
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)
    inner()
    print(x)

outer()
print(x)
```

This is also why naming a variable `list` or `max` is a bad idea: your global name hides the built-in one.

```python tryit
max = 10                  # hides the built-in max()
try:
    print(max(3, 7))
except TypeError as error:
    print("Error:", error)
del max                   # remove our name, the built-in is visible again
print(max(3, 7))
```

## Summary

- Names assigned in a function are local to it.
- Functions can read global names; `global` lets them assign to one.
- `nonlocal` changes a variable of the enclosing function.
- Python looks up names in the order Local, Enclosing, Global, Built-in.

```exercise
{
  "title": "Fix the score keeper",
  "prompt_md": "`add_points` should add to the global `score`, but it crashes. Add one line so it works. The output must be `15`.",
  "starter_code": "score = 0\n\ndef add_points(points):\n    score += points\n\nadd_points(10)\nadd_points(5)\nprint(score)",
  "solution_code": "score = 0\n\ndef add_points(points):\n    global score\n    score += points\n\nadd_points(10)\nadd_points(5)\nprint(score)",
  "check_type": "output",
  "expected_value": "15",
  "hint": "Write global score as the first line inside the function."
}
```

```exercise
{
  "title": "A running total",
  "prompt_md": "Finish `make_totaller()`. It returns a function `add(amount)` that adds `amount` to a total kept in the enclosing scope and returns the new total. The code below must print `5 12 20`.",
  "starter_code": "def make_totaller():\n    total = 0\n\n    def add(amount):\n        pass\n\n    return add\n\nadd = make_totaller()\nprint(add(5), add(7), add(8))",
  "solution_code": "def make_totaller():\n    total = 0\n\n    def add(amount):\n        nonlocal total\n        total += amount\n        return total\n\n    return add\n\nadd = make_totaller()\nprint(add(5), add(7), add(8))",
  "check_type": "output",
  "expected_value": "5 12 20",
  "hint": "Declare nonlocal total inside add, then add the amount and return the total."
}
```

```quiz
[
  {"question": "A variable created inside a function is...", "options": ["global", "local to that function", "built-in"], "answer": 1, "explanation": "It exists only inside the function call."},
  {"question": "Which keyword lets an inner function change a variable of its outer function?", "options": ["global", "nonlocal", "outer"], "answer": 1, "explanation": "nonlocal refers to the nearest enclosing function's variable."},
  {"question": "In which order does Python look names up?", "options": ["Global, Local, Built-in, Enclosing", "Local, Enclosing, Global, Built-in", "Built-in, Global, Enclosing, Local"], "answer": 1, "explanation": "The LEGB rule: Local, Enclosing, Global, Built-in."}
]
```
