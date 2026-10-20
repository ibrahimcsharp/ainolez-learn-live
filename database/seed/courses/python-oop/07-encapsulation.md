---
title: Python Encapsulation
slug: encapsulation
summary: Protect an object's data with private names and @property getters and setters.
minutes: 9
---
## Why protect data?

If any code can change any attribute, objects can end up in impossible states:

```python tryit
class Account:
    def __init__(self, balance):
        self.balance = balance

acc = Account(100)
acc.balance = -5000      # nothing stops this!
print(acc.balance)
```

**Encapsulation** means the object controls its own data: outside code goes through methods that check the rules.

## The underscore convention

Python has no truly private attributes. Instead, a name starting with `_` means *internal - please don't touch from outside*.

```python tryit
class Account:
    def __init__(self, balance):
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Not enough money")
        self._balance -= amount

    def balance(self):
        return self._balance

acc = Account(100)
acc.deposit(50)
acc.withdraw(30)
print(acc.balance())
try:
    acc.withdraw(1000)
except ValueError as error:
    print("Refused:", error)
```

## Double underscore: name mangling

Two underscores (`__name`) make Python rename the attribute to `_ClassName__name`. It is harder to reach by accident and avoids name clashes in subclasses.

```python tryit
class Safe:
    def __init__(self, code):
        self.__code = code

    def open(self, attempt):
        return attempt == self.__code

s = Safe("4096")
print(s.open("1234"), s.open("4096"))
print(hasattr(s, "__code"))         # False
print(s._Safe__code)                # still reachable - it is not real security
```

## @property: attributes with rules

A **property** looks like a normal attribute from outside, but runs a method when it is read or set. This lets you add checks without changing how the class is used.

```python tryit
class Thermostat:
    def __init__(self, celsius):
        self.celsius = celsius       # goes through the setter below

    @property
    def celsius(self):               # getter
        return self._celsius

    @celsius.setter
    def celsius(self, value):        # setter with a rule
        if not 5 <= value <= 30:
            raise ValueError("Choose 5 to 30 degrees")
        self._celsius = value

    @property
    def fahrenheit(self):            # read-only, worked out on demand
        return self._celsius * 9 / 5 + 32

t = Thermostat(21)
t.celsius = 23
print(t.celsius, t.fahrenheit)
try:
    t.celsius = 90
except ValueError as error:
    print(error)
```

Without a setter (like `fahrenheit`), the property is read-only.

## Summary

- Encapsulation: the object guards its data and rules.
- `_name` = internal by convention; `__name` = name mangling.
- `@property` and `@name.setter` add checks while keeping attribute syntax.

```exercise
{
  "title": "Valid age",
  "prompt_md": "Add an `age` property to `Person`. The setter must raise `ValueError` if the age is below 0. The code must print:\n\n```\n30\nAge cannot be negative\n30\n```",
  "starter_code": "class Person:\n    def __init__(self, age):\n        self.age = age\n\n    # add the age property and its setter here\n\np = Person(30)\nprint(p.age)\ntry:\n    p.age = -1\nexcept ValueError as error:\n    print(error)\nprint(p.age)\n",
  "solution_code": "class Person:\n    def __init__(self, age):\n        self.age = age\n\n    @property\n    def age(self):\n        return self._age\n\n    @age.setter\n    def age(self, value):\n        if value < 0:\n            raise ValueError(\"Age cannot be negative\")\n        self._age = value\n\np = Person(30)\nprint(p.age)\ntry:\n    p.age = -1\nexcept ValueError as error:\n    print(error)\nprint(p.age)\n",
  "check_type": "output",
  "expected_value": "30\nAge cannot be negative\n30",
  "hint": "Store the real value in self._age. The getter returns it; the setter checks the value first."
}
```

```quiz
[
  {"question": "What does a leading underscore (_balance) mean?", "options": ["The attribute is deleted", "Internal: don't use it from outside", "It is a class attribute"], "answer": 1, "explanation": "It is a convention, not enforced."},
  {"question": "Which decorator creates a getter?", "options": ["@getter", "@property", "@attribute"], "answer": 1, "explanation": "@property turns a method into a readable attribute."},
  {"question": "A property has a getter but no setter. What happens on assignment?", "options": ["It works", "AttributeError", "The value is ignored"], "answer": 1, "explanation": "The property is read-only."}
]
```
