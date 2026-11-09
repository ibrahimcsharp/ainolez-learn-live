---
title: Python Function Arguments
slug: arguments
summary: Positional and keyword arguments, default values, *args, **kwargs, keyword-only and positional-only parameters, and unpacking into a call.
minutes: 13
---
## Parameters and arguments

The names in the `def` line are **parameters**. The values you pass when you call the function are **arguments**.

```python tryit
def greet(name, greeting):      # name and greeting are parameters
    print(f"{greeting}, {name}!")

greet("Omar", "Good morning")   # "Omar" and "Good morning" are arguments
```

## Positional and keyword arguments

Positional arguments are matched by **order**. Keyword arguments are matched by **name**, so their order does not matter and the call reads more clearly.

```python tryit
def book_flight(origin, destination, seats):
    print(f"{seats} seat(s) from {origin} to {destination}")

book_flight("Cairo", "Rome", 2)
book_flight(destination="Rome", seats=2, origin="Cairo")
book_flight("Cairo", seats=1, destination="Oslo")   # mix: positional first
```

Positional arguments must come before keyword arguments in a call.

## Default values

A parameter with `=value` is optional. Parameters with defaults come after the ones without.

```python tryit
def make_tea(sugar=0, milk=False):
    extra = " with milk" if milk else ""
    print(f"Tea, {sugar} sugar{extra}")

make_tea()
make_tea(2)
make_tea(milk=True)
```

## The mutable default trap

A default value is created **once**, when the function is defined, not on every call. A list or dictionary as a default is therefore shared between calls.

```python tryit
def add_item_bad(item, basket=[]):
    basket.append(item)
    return basket

print(add_item_bad("apple"))
print(add_item_bad("pear"))     # the apple is still there!

def add_item(item, basket=None):
    if basket is None:
        basket = []             # a fresh list each call
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("pear"))
```

Use `None` as the default and create the list inside the function.

## *args: any number of positional arguments

A parameter written `*args` collects every extra positional argument into a **tuple**. The name `args` is only a habit; the star is what matters.

```python tryit
def average(*numbers):
    print("got", numbers)
    return sum(numbers) / len(numbers) if numbers else 0

print(average(4, 8))
print(average(1, 2, 3, 4, 5))
print(average())
```

## **kwargs: any number of keyword arguments

`**kwargs` collects every extra keyword argument into a **dictionary**.

```python tryit
def make_tag(tag, text, **attributes):
    parts = "".join(f' {key}="{value}"' for key, value in attributes.items())
    return f"<{tag}{parts}>{text}</{tag}>"

print(make_tag("a", "Home", href="/", title="Start page"))
print(make_tag("p", "Plain"))
```

The full order in a `def` line is: normal parameters, `*args`, keyword-only parameters, `**kwargs`.

## Keyword-only and positional-only

Parameters **after** a bare `*` must be passed by name. Parameters **before** a `/` must be passed by position. Both make a function harder to call the wrong way.

```python tryit
def transfer(amount, *, to, note=""):
    print(f"Send {amount} to {to}. {note}")

transfer(50, to="Lina")
# transfer(50, "Lina")   # TypeError: 'to' must be named

def power(base, exponent, /):
    return base ** exponent

print(power(2, 10))
# power(base=2, exponent=10)   # TypeError: these are positional-only
```

## Unpacking into a call

The stars also work the other way round: `*` spreads a list into positional arguments and `**` spreads a dictionary into keyword arguments.

```python tryit
def describe(name, age, city):
    print(f"{name}, {age}, lives in {city}")

row = ["Ivo", 41, "Zagreb"]
describe(*row)

info = {"city": "Quito", "name": "Paz", "age": 29}
describe(**info)
```

## Summary

- Positional arguments match by order, keyword arguments by name.
- Defaults make parameters optional; never use a list or dict as a default.
- `*args` collects extra positional arguments into a tuple, `**kwargs` keyword ones into a dict.
- After a bare `*`, parameters are keyword-only; before `/`, positional-only.
- `f(*items)` and `f(**mapping)` unpack values into a call.

```exercise
{
  "title": "Join any number of words",
  "prompt_md": "Write `join_words(*words, sep=\" \")` that joins any number of words with `sep` between them. The calls below must print:\n\n```\nred green blue\n2024-06-01\n```",
  "starter_code": "def join_words():\n    pass\n\nprint(join_words(\"red\", \"green\", \"blue\"))\nprint(join_words(\"2024\", \"06\", \"01\", sep=\"-\"))",
  "solution_code": "def join_words(*words, sep=\" \"):\n    return sep.join(words)\n\nprint(join_words(\"red\", \"green\", \"blue\"))\nprint(join_words(\"2024\", \"06\", \"01\", sep=\"-\"))",
  "check_type": "output",
  "expected_value": "red green blue\n2024-06-01",
  "hint": "words is a tuple of strings; sep.join(words) glues them. Because sep comes after *words, it can only be given by name."
}
```

```exercise
{
  "title": "Build a profile",
  "prompt_md": "Write `profile(name, **details)` that prints the name, then each detail as `- key: value` on its own line, in the order given. The call below must print:\n\n```\nMina\n- job: pilot\n- city: Seoul\n```",
  "starter_code": "def profile(name, **details):\n    pass\n\nprofile(\"Mina\", job=\"pilot\", city=\"Seoul\")",
  "solution_code": "def profile(name, **details):\n    print(name)\n    for key, value in details.items():\n        print(f\"- {key}: {value}\")\n\nprofile(\"Mina\", job=\"pilot\", city=\"Seoul\")",
  "check_type": "output",
  "expected_value": "Mina\n- job: pilot\n- city: Seoul",
  "hint": "details is a dictionary: loop over details.items()."
}
```

```quiz
[
  {"question": "Inside def f(*args), what type is args?", "options": ["list", "tuple", "dict"], "answer": 1, "explanation": "*args collects extra positional arguments into a tuple."},
  {"question": "Why is def f(items=[]) risky?", "options": ["Lists cannot be defaults", "The same list is shared by every call", "It is slower"], "answer": 1, "explanation": "The default is created once, so changes to it carry over to later calls."},
  {"question": "def f(a, *, b). Which call works?", "options": ["f(1, 2)", "f(1, b=2)", "f(a=1, 2)"], "answer": 1, "explanation": "b comes after the bare *, so it must be passed by name."},
  {"question": "nums = [3, 4]. What does pow(*nums) compute?", "options": ["pow([3, 4])", "pow(3, 4)", "an error"], "answer": 1, "explanation": "* spreads the list into two positional arguments."}
]
```
