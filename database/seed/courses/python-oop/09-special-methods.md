---
title: Python Special (Dunder) Methods
slug: special-methods
summary: Make your objects print nicely, compare, add, have a length and work with in and for.
minutes: 10
---
## Methods Python calls for you

Methods with double underscores on both sides - *dunder methods* - are called by Python when you use built-in operations. `__init__` is one. Defining others makes your objects feel built in.

## __str__ and __repr__: printing

```python tryit
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):        # for users: print(), str(), f-strings
        return f"{self.title} by {self.author}"

    def __repr__(self):       # for developers: the console, lists, debugging
        return f"Book({self.title!r}, {self.author!r})"

b = Book("Beloved", "Toni Morrison")
print(b)
print([b])
```

Without them, Python prints something like `<__main__.Book object at 0x7f...>`.

## __eq__ and __lt__: comparing

```python tryit
class Money:
    def __init__(self, cents):
        self.cents = cents

    def __eq__(self, other):
        return self.cents == other.cents

    def __lt__(self, other):
        return self.cents < other.cents

    def __repr__(self):
        return f"${self.cents / 100:.2f}"

print(Money(500) == Money(500))     # True: same value
prices = [Money(1999), Money(450), Money(1200)]
print(sorted(prices))               # sorted() uses __lt__
print(min(prices), max(prices))
```

## __add__: operators

```python tryit
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, number):
        return Vector(self.x * number, self.y * number)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

print(Vector(1, 2) + Vector(3, 4))
print(Vector(1, 2) * 3)
```

## __len__, __contains__, __getitem__ and __iter__

These make an object act like a collection.

```python tryit
class Team:
    def __init__(self, *members):
        self.members = list(members)

    def __len__(self):
        return len(self.members)

    def __contains__(self, name):
        return name in self.members

    def __getitem__(self, index):
        return self.members[index]

    def __iter__(self):
        return iter(self.members)

team = Team("Ana", "Ben", "Cleo")
print(len(team))
print("Ben" in team, "Zed" in team)
print(team[0], team[-1])
for member in team:
    print("-", member)
```

## Common dunder methods

| You write | Python calls |
|---|---|
| `print(x)`, `str(x)` | `x.__str__()` |
| `x == y`, `x < y` | `x.__eq__(y)`, `x.__lt__(y)` |
| `x + y`, `x * y` | `x.__add__(y)`, `x.__mul__(y)` |
| `len(x)` | `x.__len__()` |
| `item in x` | `x.__contains__(item)` |
| `x[i]` | `x.__getitem__(i)` |
| `for item in x` | `x.__iter__()` |

!!! tip
    The `dataclasses` module writes `__init__`, `__repr__` and `__eq__` for you: put `@dataclass` above a class and list its fields with type hints.

## Summary

- Dunder methods connect your class to Python's built-in syntax.
- `__str__` / `__repr__` for printing, `__eq__` / `__lt__` for comparing, `__add__` for `+`.
- `__len__`, `__contains__`, `__getitem__`, `__iter__` make collection-like objects.

```exercise
{
  "title": "Fractions",
  "prompt_md": "Give `Fraction` a `__str__` that returns `\"top/bottom\"` and an `__add__` that returns a new Fraction (a/b + c/d = (a*d + c*b)/(b*d)). The code must print `5/6`.",
  "starter_code": "class Fraction:\n    def __init__(self, top, bottom):\n        self.top = top\n        self.bottom = bottom\n\n    # add __str__ and __add__ here\n\nprint(Fraction(1, 2) + Fraction(1, 3))\n",
  "solution_code": "class Fraction:\n    def __init__(self, top, bottom):\n        self.top = top\n        self.bottom = bottom\n\n    def __str__(self):\n        return f\"{self.top}/{self.bottom}\"\n\n    def __add__(self, other):\n        return Fraction(self.top * other.bottom + other.top * self.bottom, self.bottom * other.bottom)\n\nprint(Fraction(1, 2) + Fraction(1, 3))\n",
  "check_type": "output",
  "expected_value": "5/6",
  "hint": "1/2 + 1/3 = (1*3 + 1*2) / (2*3) = 5/6. __add__ returns Fraction(new_top, new_bottom)."
}
```

```quiz
[
  {"question": "Which method does print(obj) use?", "options": ["__print__", "__str__", "__init__"], "answer": 1, "explanation": "print calls str(), which calls __str__."},
  {"question": "Which method makes len(obj) work?", "options": ["__len__", "__size__", "__count__"], "answer": 0, "explanation": "len() calls __len__."},
  {"question": "What does sorted() need to compare your objects?", "options": ["__lt__", "__sort__", "__order__"], "answer": 0, "explanation": "Sorting uses the < operator, which calls __lt__."}
]
```
