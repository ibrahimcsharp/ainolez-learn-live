---
title: Python Attributes and Methods
slug: attributes-methods
summary: Instance and class attributes, methods that change an object, and class and static methods.
minutes: 10
---
## Methods

A method is a function inside a class. Its first parameter is `self`, so it can read and change the object's attributes.

```python tryit
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self, step=1):
        self.value += step

    def reset(self):
        self.value = 0

clicks = Counter()
clicks.increment()
clicks.increment(5)
print(clicks.value)
clicks.reset()
print(clicks.value)
```

When you call `clicks.increment(5)`, Python runs `Counter.increment(clicks, 5)`.

## Methods that return values

```python tryit
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def to_fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    def is_freezing(self):
        return self.celsius <= 0

today = Temperature(22)
print(today.to_fahrenheit(), today.is_freezing())
```

## Methods calling methods

Inside a class, call another method with `self.`.

```python tryit
class Basket:
    def __init__(self):
        self.items = []

    def add(self, name, price):
        self.items.append((name, price))

    def total(self):
        return sum(price for _, price in self.items)

    def summary(self):
        return f"{len(self.items)} items, total {self.total():.2f}"

basket = Basket()
basket.add("bread", 2.2)
basket.add("milk", 1.15)
print(basket.summary())
```

## Class attributes: shared by all

An attribute set in the class body (not on `self`) is shared by every object. It is good for constants and counters.

```python tryit
class Player:
    max_health = 100          # class attribute: the same for everyone
    count = 0

    def __init__(self, name):
        self.name = name                  # instance attribute
        self.health = Player.max_health
        Player.count += 1

a = Player("Ivy")
b = Player("Kai")
print(a.health, b.health, Player.count)
```

!!! warning
    Do not use a list or dict as a class attribute for per-object data: every object would share the same list. Create it in `__init__` with `self.items = []`.

## Class methods and static methods

- A **class method** (`@classmethod`) receives the class as `cls`. It is often used as an alternative way to create objects.
- A **static method** (`@staticmethod`) receives neither; it is a plain helper function that lives in the class.

```python tryit
class Date:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_text(cls, text):
        year, month, day = (int(part) for part in text.split("-"))
        return cls(year, month, day)

    @staticmethod
    def is_leap(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

d = Date.from_text("2028-02-29")
print(d.year, d.month, d.day)
print(Date.is_leap(2028), Date.is_leap(2100))
```

## Summary

- Methods take `self` first and use `self.` to reach attributes and other methods.
- Class attributes are shared; instance attributes belong to one object.
- `@classmethod` gets the class (`cls`); `@staticmethod` gets nothing extra.

```exercise
{
  "title": "Piggy bank",
  "prompt_md": "Complete the class: `deposit(amount)` adds to `self.coins`, and `is_full()` returns `True` when `coins` is at least `goal`. The code below must print:\n\n```\n30 False\n55 True\n```",
  "starter_code": "class PiggyBank:\n    def __init__(self, goal):\n        self.goal = goal\n        self.coins = 0\n\n    # write deposit and is_full here\n\npig = PiggyBank(50)\npig.deposit(10)\npig.deposit(20)\nprint(pig.coins, pig.is_full())\npig.deposit(25)\nprint(pig.coins, pig.is_full())\n",
  "solution_code": "class PiggyBank:\n    def __init__(self, goal):\n        self.goal = goal\n        self.coins = 0\n\n    def deposit(self, amount):\n        self.coins += amount\n\n    def is_full(self):\n        return self.coins >= self.goal\n\npig = PiggyBank(50)\npig.deposit(10)\npig.deposit(20)\nprint(pig.coins, pig.is_full())\npig.deposit(25)\nprint(pig.coins, pig.is_full())\n",
  "check_type": "output",
  "expected_value": "30 False\n55 True",
  "hint": "def deposit(self, amount): self.coins += amount. def is_full(self): return self.coins >= self.goal"
}
```

```quiz
[
  {"question": "What is the first parameter of a normal method?", "options": ["cls", "self", "this"], "answer": 1, "explanation": "Instance methods receive the object as self."},
  {"question": "Where does a class attribute live?", "options": ["On each object", "On the class, shared by all objects", "Only inside __init__"], "answer": 1, "explanation": "Class attributes are shared."},
  {"question": "What does a @classmethod receive first?", "options": ["self", "cls (the class)", "nothing"], "answer": 1, "explanation": "Class methods get the class as cls."}
]
```
