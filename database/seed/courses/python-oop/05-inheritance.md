---
title: Python Inheritance
slug: inheritance
summary: Build new classes on existing ones, override methods and call the parent with super().
minutes: 10
---
## Reusing a class

**Inheritance** lets a new class (the *child* or *subclass*) take everything from an existing class (the *parent* or *base class*) and add or change parts.

```python tryit
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating")

class Cat(Animal):          # Cat inherits from Animal
    def meow(self):
        print(f"{self.name} says meow")

tom = Cat("Tom")
tom.eat()      # inherited from Animal
tom.meow()     # Cat's own method
```

Put the parent's name in brackets after the class name.

## Overriding methods

A child can replace a parent's method by defining one with the same name.

```python tryit
class Animal:
    def __init__(self, name):
        self.name = name

    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):
        return "Woof"

class Cow(Animal):
    def sound(self):
        return "Moo"

for animal in [Dog("Rex"), Cow("Daisy"), Animal("Mystery")]:
    print(animal.name, animal.sound())
```

## super(): calling the parent

`super()` gives you the parent class. Use it to extend a method instead of replacing it completely - especially `__init__`.

```python tryit
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        return f"{self.name} earns {self.salary}"

class Manager(Employee):
    def __init__(self, name, salary, team):
        super().__init__(name, salary)   # let Employee set name and salary
        self.team = team

    def describe(self):
        return super().describe() + f" and leads {len(self.team)} people"

boss = Manager("Rosa", 5200, ["Ali", "Mei", "Tom"])
print(boss.describe())
```

## Checking relationships

```python tryit
class Animal: pass
class Bird(Animal): pass
class Penguin(Bird): pass

pingu = Penguin()
print(isinstance(pingu, Penguin), isinstance(pingu, Bird), isinstance(pingu, Animal))
print(issubclass(Penguin, Animal), issubclass(Animal, Penguin))
```

A penguin **is a** bird and **is an** animal. Use inheritance when that "is a" sentence makes sense.

## Multiple inheritance

A class can have more than one parent. Python searches the parents from left to right.

```python tryit
class Swimmer:
    def swim(self):
        return "swimming"

class Flyer:
    def fly(self):
        return "flying"

class Duck(Swimmer, Flyer):
    pass

d = Duck()
print(d.swim(), d.fly())
print([cls.__name__ for cls in Duck.__mro__])  # the search order
```

Small "mixin" classes like these are the most common use of multiple inheritance. Keep hierarchies shallow and simple.

## Summary

- `class Child(Parent):` inherits attributes and methods.
- A method with the same name **overrides** the parent's.
- `super().method(...)` calls the parent's version - always use it in a child's `__init__`.

```exercise
{
  "title": "Electric car",
  "prompt_md": "Make `ElectricCar` inherit from `Car`. Its `__init__` takes `brand` and `battery`, calls `super().__init__(brand)` and stores `battery`. Override `info()` to return the parent's info plus the battery. The code must print `Tesla car, 75 kWh`.",
  "starter_code": "class Car:\n    def __init__(self, brand):\n        self.brand = brand\n\n    def info(self):\n        return f\"{self.brand} car\"\n\n# write ElectricCar here\n\nprint(ElectricCar(\"Tesla\", 75).info())\n",
  "solution_code": "class Car:\n    def __init__(self, brand):\n        self.brand = brand\n\n    def info(self):\n        return f\"{self.brand} car\"\n\nclass ElectricCar(Car):\n    def __init__(self, brand, battery):\n        super().__init__(brand)\n        self.battery = battery\n\n    def info(self):\n        return f\"{super().info()}, {self.battery} kWh\"\n\nprint(ElectricCar(\"Tesla\", 75).info())\n",
  "check_type": "output",
  "expected_value": "Tesla car, 75 kWh",
  "hint": "In info(), use super().info() to get \"Tesla car\" and add the battery to it."
}
```

```quiz
[
  {"question": "How does Dog inherit from Animal?", "options": ["class Dog extends Animal:", "class Dog(Animal):", "class Dog: inherit Animal"], "answer": 1, "explanation": "The parent goes in brackets."},
  {"question": "What does super().__init__(name) do in a child class?", "options": ["Creates a new parent object", "Runs the parent's __init__ on this object", "Deletes the parent"], "answer": 1, "explanation": "It lets the parent set up its part of the object."},
  {"question": "A child defines a method with the same name as the parent. This is called...", "options": ["overloading", "overriding", "hiding"], "answer": 1, "explanation": "The child's version overrides the parent's."}
]
```
