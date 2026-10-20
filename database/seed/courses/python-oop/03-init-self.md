---
title: Python __init__ and self
slug: init-self
summary: Set up every new object with __init__, and understand what self really is.
minutes: 8
---
## The __init__ method

`__init__` runs automatically every time you create an object. Use it to give the object its starting attributes. (The double underscores are pronounced "dunder": *dunder init*.)

```python tryit
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
        self.scores = []

ana = Student("Ana", 9)
ben = Student("Ben", 10)
print(ana.name, ana.grade, ana.scores)
print(ben.name, ben.grade)
```

The values in `Student("Ana", 9)` are passed to `__init__` as `name` and `grade`.

## What is self?

`self` is the object being created or used. Python passes it in for you as the first argument.

When you write `ana = Student("Ana", 9)`, Python:

1. creates a new, empty object,
2. calls `Student.__init__(that_object, "Ana", 9)`,
3. gives you the object back as `ana`.

So `self.name = name` means *store `name` on this particular object*.

```python tryit
class Student:
    def __init__(self, name):
        self.name = name
        print("inside __init__, self is", id(self))

ana = Student("Ana")
print("outside, ana is        ", id(ana))   # the same number: the same object
```

!!! note
    `self` is only a convention - any name would work - but every Python programmer uses `self`. Stick to it.

## Default values

Parameters of `__init__` can have defaults, just like in any function.

```python tryit
class Account:
    def __init__(self, owner, balance=0, currency="USD"):
        self.owner = owner
        self.balance = balance
        self.currency = currency

a = Account("Zara")
b = Account("Yusuf", 250, currency="EUR")
print(a.owner, a.balance, a.currency)
print(b.owner, b.balance, b.currency)
```

## Forgetting self

A very common mistake is to forget `self.` - the value then lives only inside `__init__` and is lost.

```python tryit
class Broken:
    def __init__(self, size):
        size = size          # a local variable, not an attribute!

box = Broken(3)
print(hasattr(box, "size"))  # False
```

## Summary

- `__init__(self, ...)` runs when an object is created and sets its attributes.
- `self` is the object itself; Python passes it automatically.
- Always write `self.attribute = value` to store data on the object.

```exercise
{
  "title": "Rectangle",
  "prompt_md": "Write a class `Rectangle` whose `__init__` stores `width` and `height`. Create `Rectangle(4, 7)` and print its width, height and area on one line: `4 7 28`.",
  "starter_code": "class Rectangle:\n    pass\n",
  "solution_code": "class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\nr = Rectangle(4, 7)\nprint(r.width, r.height, r.width * r.height)",
  "check_type": "output",
  "expected_value": "4 7 28",
  "hint": "def __init__(self, width, height): then self.width = width and self.height = height."
}
```

```quiz
[
  {"question": "When does __init__ run?", "options": ["When the class is defined", "Every time an object is created", "Only if you call it yourself"], "answer": 1, "explanation": "Creating an object calls __init__ automatically."},
  {"question": "What is self?", "options": ["The class", "The object the method works on", "A keyword for private data"], "answer": 1, "explanation": "self refers to the current instance."},
  {"question": "Inside __init__, which line stores color on the object?", "options": ["color = color", "self.color = color", "self = color"], "answer": 1, "explanation": "self.color makes it an attribute of the object."}
]
```
