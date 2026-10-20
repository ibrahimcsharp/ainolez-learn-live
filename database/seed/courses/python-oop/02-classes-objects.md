---
title: Python Classes and Objects
slug: classes-objects
summary: Define a class, create objects from it, and give each object its own data.
minutes: 7
---
## Defining a class

Use the keyword `class` and a name in CapitalisedWords. The indented block is the class body.

```python tryit
class Dog:
    species = "Canis familiaris"

print(Dog.species)
```

## Creating objects

Call the class like a function to create an **object** (also called an **instance**).

```python tryit
class Dog:
    species = "Canis familiaris"

rex = Dog()
luna = Dog()
print(rex.species)
print(luna.species)
print(rex is luna)          # False: two separate objects
print(isinstance(rex, Dog)) # True
```

## Each object has its own data

You can attach attributes to an object with a dot. They belong to that object only.

```python tryit
class Dog:
    pass        # an empty class body

rex = Dog()
rex.name = "Rex"
rex.age = 4

luna = Dog()
luna.name = "Luna"
luna.age = 2

print(rex.name, rex.age)
print(luna.name, luna.age)
```

Setting attributes from outside like this is error-prone: it is easy to forget one. The next lesson shows the proper way, with `__init__`.

## Changing and deleting attributes

```python tryit
class Dog:
    pass

rex = Dog()
rex.name = "Rex"
rex.name = "Rex the Brave"   # change
print(rex.name)
del rex.name                 # delete
print(hasattr(rex, "name"))
```

## Objects in collections

Objects can go in lists and dictionaries like any other value.

```python tryit
class Dog:
    pass

pack = []
for name in ["Rex", "Luna", "Milo"]:
    dog = Dog()
    dog.name = name
    pack.append(dog)

print([dog.name for dog in pack])
```

## Summary

- `class Name:` defines a class; `Name()` creates an object.
- Each object has its own attributes, read and set with a dot.
- `isinstance(obj, Name)` checks the class of an object.

```exercise
{
  "title": "Two cars",
  "prompt_md": "Create a class `Car` with an empty body. Make two objects, give each a `brand` attribute (`Toyota` and `Kia`), and print both brands on one line: `Toyota Kia`.",
  "starter_code": "class Car:\n    pass\n",
  "solution_code": "class Car:\n    pass\n\na = Car()\na.brand = \"Toyota\"\nb = Car()\nb.brand = \"Kia\"\nprint(a.brand, b.brand)",
  "check_type": "output",
  "expected_value": "Toyota Kia",
  "hint": "a = Car() then a.brand = \"Toyota\"."
}
```

```quiz
[
  {"question": "How do you create an object from class Cat?", "options": ["new Cat", "Cat()", "Cat.create"], "answer": 1, "explanation": "Calling the class creates an instance."},
  {"question": "Two objects made from the same class...", "options": ["share all their data", "each have their own attributes", "are the same object"], "answer": 1, "explanation": "Each instance stores its own data."},
  {"question": "Which function checks the class of an object?", "options": ["isinstance()", "classof()", "type_is()"], "answer": 0, "explanation": "isinstance(obj, Class) returns True or False."}
]
```
