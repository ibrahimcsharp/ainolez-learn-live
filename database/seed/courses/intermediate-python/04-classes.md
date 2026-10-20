---
title: Classes and Objects
slug: classes
summary: Model real things with classes, attributes and methods, and create objects from them.
minutes: 10
---
## Why classes?

A class bundles data and the functions that work on that data. It is a blueprint; each **object** made from it has its own values.

```python tryit
class Dog:
    def __init__(self, name, age):
        self.name = name      # attributes
        self.age = age

    def bark(self):           # a method
        return f"{self.name} says woof!"

rex = Dog("Rex", 3)
luna = Dog("Luna", 5)
print(rex.bark())
print(luna.name, luna.age)
```

- `__init__` runs when you create an object; it sets the starting values.
- `self` is the object itself. Python passes it automatically.

## Changing state

Methods can change an object's attributes.

```python tryit
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("not enough money")
        self.balance -= amount

account = BankAccount("Ana", 100)
account.deposit(50)
account.withdraw(30)
print(account.owner, account.balance)
```

## Class attributes

An attribute defined on the class itself is shared by every object.

```python tryit
class Circle:
    pi = 3.14159              # shared by all circles

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return round(Circle.pi * self.radius ** 2, 2)

print(Circle(1).area(), Circle(2).area())
```

## Readable objects with __str__

```python tryit
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

print(Point(3, 4))
```

## dataclasses

For classes that mostly hold data, `dataclass` writes `__init__` and a readable display for you.

```python tryit
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    pages: int

book = Book("Dune", 412)
print(book)
print(book.pages)
```

## Summary

- A class is a blueprint; objects are made by calling it: `Dog("Rex", 3)`.
- `__init__` sets attributes on `self`; methods use and change them.
- `@dataclass` saves boilerplate for data classes.

```exercise
{
  "title": "A rectangle class",
  "prompt_md": "Finish the `Rectangle` class: `__init__` stores `width` and `height`, `area()` returns width times height. The program prints `Rectangle(4, 5).area()`, which must show exactly `20`.",
  "starter_code": "class Rectangle:\n    def __init__(self, width, height):\n        pass\n\n    def area(self):\n        pass\n\nprint(Rectangle(4, 5).area())",
  "solution_code": "class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n    def area(self):\n        return self.width * self.height\n\nprint(Rectangle(4, 5).area())",
  "check_type": "output",
  "expected_value": "20",
  "hint": "Store the values with self.width = width, then return self.width * self.height."
}
```

```quiz
[
  {"question": "What is self in a method?", "options": ["The class name", "The object the method was called on", "A keyword for private data"], "answer": 1, "explanation": "self refers to the current object."},
  {"question": "When does __init__ run?", "options": ["When the class is defined", "When an object is created", "When the program ends"], "answer": 1, "explanation": "Calling the class creates an object and runs __init__."}
]
```
