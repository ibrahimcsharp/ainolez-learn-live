---
title: Python Built-in Functions
slug: built-in-functions
summary: A guided tour of the functions Python always has - for numbers, text, collections, types and looking things up.
minutes: 12
---
## Always there, no import needed

Python has about 70 **built-in functions** that you can use anywhere without importing anything. You already know `print`, `len`, `input` and `range`. This lesson groups the others you will reach for most.

## Numbers

| Function | Does |
|---|---|
| `abs(x)` | distance from zero |
| `round(x, n)` | round to `n` decimals |
| `min(...)`, `max(...)` | smallest, largest |
| `sum(items)` | add up |
| `pow(x, y)` | `x ** y` (with a third number: the remainder after dividing) |
| `divmod(a, b)` | `(a // b, a % b)` in one go |

```python tryit
print(abs(-7.5))
print(round(3.14159, 2), round(1234, -2))
print(min(4, 9, 1), max([4, 9, 1]))
print(sum([0.5, 1.5, 2]), sum([1, 2], 10))   # optional start value
print(pow(2, 8), pow(2, 8, 5))
hours, minutes = divmod(135, 60)
print(hours, "h", minutes, "min")
```

`round()` rounds halves to the nearest **even** number: `round(2.5)` is `2` and `round(3.5)` is `4`. This avoids a bias when you round many values.

## Checking a whole collection: any and all

`any()` is `True` if **at least one** item is true. `all()` is `True` if **every** item is true.

```python tryit
marks = [72, 88, 45, 91]
print(any(m < 50 for m in marks))    # did anyone fail?
print(all(m >= 40 for m in marks))   # did everyone reach 40?

password = "secret7"
print(any(ch.isdigit() for ch in password))
print(all([]), any([]))              # empty: all is True, any is False
```

## Looping helpers

```python tryit
names = ["Ada", "Linus", "Grace"]
years = [1815, 1969, 1906]

for i, name in enumerate(names, start=1):
    print(i, name)

for name, year in zip(names, years):
    print(f"{name} was born in {year}")

print(list(reversed(names)))
print(sorted(years, reverse=True))
```

`zip` stops at the **shortest** input. `reversed` and `sorted` work on any iterable, and `sorted` always returns a list.

## Converting between types

```python tryit
print(int("42"), int(7.9), int("ff", 16))    # int() cuts the decimals off
print(float("2.5"), str(99), bool(0), bool("no"))
print(list("abc"), tuple([1, 2]), set("hello"))
print(dict([("a", 1), ("b", 2)]))
print(bin(10), oct(10), hex(255))
print(ord("A"), chr(66))                     # character <-> code number
```

## Looking at types and objects

```python tryit
value = [1, 2, 3]
print(type(value))
print(isinstance(value, list))
print(isinstance(3.0, (int, float)))   # any of several types
print(callable(len), callable(value))
print(len(dir(value)), "names on a list, for example", dir(value)[-3:])
```

`isinstance` is better than comparing `type(x) == list`, because it also accepts subclasses.

## Getting attributes by name

`getattr`, `setattr` and `hasattr` work with attribute names held in strings. They are useful when the name is only known while the program runs.

```python tryit
class Settings:
    theme = "dark"

s = Settings()
for name in ["theme", "language"]:
    print(name, hasattr(s, name), getattr(s, name, "not set"))
setattr(s, "language", "en")
print(s.language)
```

## Text and help

```python tryit
print(repr("tab\there"))       # shows quotes and escapes
print(format(1234567.891, ",.2f"))
print(ascii("café"))
print(len.__doc__)             # the documentation help(len) shows
```

In a normal Python window, `help(len)` shows that documentation, and `help()` on its own opens an interactive help system.

## Not every name is a function

`print`, `len` and `sum` are functions, but `int`, `str`, `list`, `dict` and `range` are actually **classes**. Calling a class creates a new value, which is why `list("abc")` makes a list.

## Summary

- Numbers: `abs`, `round`, `min`, `max`, `sum`, `pow`, `divmod`.
- Collections: `any`, `all`, `enumerate`, `zip`, `reversed`, `sorted`.
- Types: `int`, `float`, `str`, `list`, `dict`, `set`, `bool`, `type`, `isinstance`.
- Objects: `dir`, `getattr`, `hasattr`, `setattr`, `help`.

```exercise
{
  "title": "Grade check",
  "prompt_md": "Using built-in functions only (no loops you write yourself), print on separate lines: the highest mark, the lowest mark, the average rounded to 1 decimal, and whether **all** marks are at least 50. The output must be:\n\n```\n94\n51\n73.6\nTrue\n```",
  "starter_code": "marks = [67, 94, 51, 80, 76]\n",
  "solution_code": "marks = [67, 94, 51, 80, 76]\nprint(max(marks))\nprint(min(marks))\nprint(round(sum(marks) / len(marks), 1))\nprint(all(mark >= 50 for mark in marks))",
  "check_type": "output",
  "expected_value": "94\n51\n73.6\nTrue",
  "hint": "max, min, round(sum(...) / len(...), 1) and all(mark >= 50 for mark in marks)."
}
```

```exercise
{
  "title": "Pair them up",
  "prompt_md": "Use `zip` and `enumerate` to print each city with its rank (starting at 1) and population, like this:\n\n```\n1. Tokyo 37.4\n2. Delhi 32.9\n3. Shanghai 29.2\n```",
  "starter_code": "cities = [\"Tokyo\", \"Delhi\", \"Shanghai\"]\npopulations = [37.4, 32.9, 29.2]\n",
  "solution_code": "cities = [\"Tokyo\", \"Delhi\", \"Shanghai\"]\npopulations = [37.4, 32.9, 29.2]\nfor rank, (city, people) in enumerate(zip(cities, populations), start=1):\n    print(f\"{rank}. {city} {people}\")",
  "check_type": "output",
  "expected_value": "1. Tokyo 37.4\n2. Delhi 32.9\n3. Shanghai 29.2",
  "hint": "for rank, (city, people) in enumerate(zip(cities, populations), start=1):"
}
```

```quiz
[
  {"question": "What does divmod(17, 5) return?", "options": ["3.4", "(3, 2)", "(2, 3)"], "answer": 1, "explanation": "It returns (17 // 5, 17 % 5)."},
  {"question": "What is any([0, \"\", None])?", "options": ["True", "False"], "answer": 1, "explanation": "0, the empty string and None are all false, so no item is true."},
  {"question": "What does round(2.5) give?", "options": ["2", "3", "2.5"], "answer": 0, "explanation": "Python rounds halves to the nearest even number."},
  {"question": "zip([1, 2, 3], [\"a\", \"b\"]) makes how many pairs?", "options": ["2", "3", "an error"], "answer": 0, "explanation": "zip stops at the shortest input."}
]
```
