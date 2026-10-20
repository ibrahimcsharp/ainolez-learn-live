---
title: Inheritance and Special Methods
slug: inheritance
summary: Reuse code with inheritance and super(), and make objects work with len, == and +.
minutes: 9
---
## Inheritance

A class can **inherit** from another class: it gets all its attributes and methods and can add or change some.

```python tryit
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def introduce(self):
        return f"I am {self.name} and I say {self.speak()}"

class Cat(Animal):
    def speak(self):          # overrides the parent's method
        return "meow"

class Cow(Animal):
    def speak(self):
        return "moo"

for animal in [Cat("Tom"), Cow("Daisy")]:
    print(animal.introduce())
```

`introduce()` is written once in `Animal`, but each child gives its own `speak()`. This is called **polymorphism**.

## super()

`super()` calls the parent's version of a method, so the child only adds what is new.

```python tryit
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Manager(Employee):
    def __init__(self, name, salary, team):
        super().__init__(name, salary)
        self.team = team

boss = Manager("Rosa", 5000, ["Ali", "Kim"])
print(boss.name, boss.salary, len(boss.team))
print(isinstance(boss, Employee))
```

## Special (dunder) methods

Methods with double underscores let your objects work with Python's operators and built-ins.

```python tryit
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        return Money(self.amount + other.amount)

    def __eq__(self, other):
        return self.amount == other.amount

    def __repr__(self):
        return f"Money({self.amount})"

total = Money(5) + Money(7)
print(total)
print(Money(3) == Money(3))
```

| Method | Used by |
|---|---|
| `__str__`, `__repr__` | `print()`, the console |
| `__len__` | `len(obj)` |
| `__eq__`, `__lt__` | `==`, `<` (and sorting) |
| `__add__` | `+` |
| `__getitem__` | `obj[key]` |

## Summary

- `class Child(Parent):` inherits; methods can be overridden.
- `super()` reaches the parent's methods.
- Dunder methods connect objects to operators and built-in functions.

```exercise
{
  "title": "A playlist with len()",
  "prompt_md": "Add a `__len__` method to `Playlist` that returns the number of songs. The program prints `len(p)`, which must show exactly `3`.",
  "starter_code": "class Playlist:\n    def __init__(self, songs):\n        self.songs = songs\n\np = Playlist([\"Intro\", \"Rain\", \"Home\"])\nprint(len(p))",
  "solution_code": "class Playlist:\n    def __init__(self, songs):\n        self.songs = songs\n\n    def __len__(self):\n        return len(self.songs)\n\np = Playlist([\"Intro\", \"Rain\", \"Home\"])\nprint(len(p))",
  "check_type": "output",
  "expected_value": "3",
  "hint": "def __len__(self): return len(self.songs)"
}
```

```quiz
[
  {"question": "class B(A): means...", "options": ["A inherits from B", "B inherits from A", "A and B are unrelated"], "answer": 1, "explanation": "The class in brackets is the parent."},
  {"question": "Which method makes obj1 + obj2 work?", "options": ["__plus__", "__add__", "__sum__"], "answer": 1, "explanation": "The + operator calls __add__."}
]
```
