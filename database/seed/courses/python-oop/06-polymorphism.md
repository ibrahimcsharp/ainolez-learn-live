---
title: Python Polymorphism
slug: polymorphism
summary: Write one piece of code that works with many types - through shared method names, inheritance and duck typing.
minutes: 8
---
## One call, many forms

**Polymorphism** means *many forms*: the same operation behaves correctly for different types. You already know an example:

```python tryit
print(len("hello"))          # characters
print(len([1, 2, 3]))        # items
print(len({"a": 1, "b": 2})) # keys
print(3 + 4, "3" + "4", [3] + [4])
```

`len()` and `+` work on many types, and each type decides what they mean.

## Polymorphism with classes

Different classes can have methods with the same name. Code that calls that method does not need to know which class it has.

```python tryit
class Circle:
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r ** 2

class Square:
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

class Triangle:
    def __init__(self, base, height):
        self.base, self.height = base, height
    def area(self):
        return self.base * self.height / 2

shapes = [Circle(1), Square(3), Triangle(4, 5)]
for shape in shapes:
    print(type(shape).__name__, round(shape.area(), 2))
print("Total:", round(sum(s.area() for s in shapes), 2))
```

To support a new shape, write a new class with `area()` - the loop does not change.

## Polymorphism through inheritance

A parent class defines the method; each child overrides it. A parent method that only raises an error forces children to provide their own.

```python tryit
class Notification:
    def __init__(self, to):
        self.to = to
    def send(self, text):
        raise NotImplementedError("Each notification type must define send()")

class Email(Notification):
    def send(self, text):
        return f"Email to {self.to}: {text}"

class SMS(Notification):
    def send(self, text):
        return f"SMS to {self.to}: {text[:20]}"

for channel in [Email("ana@example.com"), SMS("+44 7700 900123")]:
    print(channel.send("Your order has shipped and will arrive tomorrow"))
```

## Duck typing

Python does not check classes before calling a method; it just calls it. *If it walks like a duck and quacks like a duck, it is a duck.* Classes do not need a common parent to be used together.

```python tryit
class Duck:
    def speak(self):
        return "Quack"

class Robot:
    def speak(self):
        return "Beep boop"

def make_it_talk(thing):
    print(thing.speak())

make_it_talk(Duck())
make_it_talk(Robot())
```

## Abstract base classes

To make the rule "every child must have this method" official, use the `abc` module. Python then refuses to create a child that forgets it.

```python tryit
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount): ...

class Card(Payment):
    def pay(self, amount):
        return f"Paid {amount} by card"

print(Card().pay(20))
try:
    Payment()
except TypeError as error:
    print("Error:", error)
```

## Summary

- Polymorphism = the same call works on different types.
- Give classes methods with the same name, or override a parent's method.
- Duck typing: Python only cares that the method exists; `ABC` and `@abstractmethod` can enforce it.

```exercise
{
  "title": "Pay everyone",
  "prompt_md": "Add a `pay()` method to `Freelancer` that returns `hours * rate`. The loop then prints every worker's pay. The output must be:\n\n```\n3000\n1200\n```",
  "starter_code": "class Employee:\n    def __init__(self, salary):\n        self.salary = salary\n    def pay(self):\n        return self.salary\n\nclass Freelancer:\n    def __init__(self, hours, rate):\n        self.hours = hours\n        self.rate = rate\n\nfor worker in [Employee(3000), Freelancer(40, 30)]:\n    print(worker.pay())\n",
  "solution_code": "class Employee:\n    def __init__(self, salary):\n        self.salary = salary\n    def pay(self):\n        return self.salary\n\nclass Freelancer:\n    def __init__(self, hours, rate):\n        self.hours = hours\n        self.rate = rate\n    def pay(self):\n        return self.hours * self.rate\n\nfor worker in [Employee(3000), Freelancer(40, 30)]:\n    print(worker.pay())\n",
  "check_type": "output",
  "expected_value": "3000\n1200",
  "hint": "def pay(self): return self.hours * self.rate"
}
```

```quiz
[
  {"question": "What does polymorphism mean?", "options": ["One class with many attributes", "The same call works on different types", "A class with many parents"], "answer": 1, "explanation": "Many forms: each type answers the same call its own way."},
  {"question": "Do two classes need a common parent to be used in the same loop?", "options": ["Yes, always", "No - duck typing only needs the method to exist"], "answer": 1, "explanation": "Python just calls the method."},
  {"question": "What happens when you create an object of an ABC with an abstract method?", "options": ["It works", "TypeError", "The method returns None"], "answer": 1, "explanation": "Abstract classes cannot be instantiated."}
]
```
