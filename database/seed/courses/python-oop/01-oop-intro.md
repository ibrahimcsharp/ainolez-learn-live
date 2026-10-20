---
title: What is Object-Oriented Programming?
slug: oop-intro
summary: Why programmers group data and behaviour into objects, and the words you need to know.
minutes: 6
---
## Two ways to organise code

So far you have probably kept data in variables and dictionaries and written separate functions to work on them:

```python tryit
book = {"title": "Dune", "pages": 412, "read": 0}

def read_pages(book, count):
    book["read"] = min(book["read"] + count, book["pages"])

read_pages(book, 100)
print(book["read"], "of", book["pages"])
```

This works, but nothing connects `read_pages` to books. As a program grows, it gets hard to know which functions belong to which data.

**Object-oriented programming (OOP)** puts the data and the functions that use it together, in one **object**:

```python tryit
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
        self.read = 0

    def read_pages(self, count):
        self.read = min(self.read + count, self.pages)

dune = Book("Dune", 412)
dune.read_pages(100)
print(dune.read, "of", dune.pages)
```

Don't worry about the details yet - the next lessons explain every line.

## The vocabulary

| Word | Meaning | In the example |
|---|---|---|
| **class** | a blueprint that describes a kind of thing | `Book` |
| **object** (instance) | one thing made from the blueprint | `dune` |
| **attribute** | data stored in an object | `title`, `pages`, `read` |
| **method** | a function that belongs to a class | `read_pages` |

One class can create many objects, each with its own data - like one cookie cutter making many cookies.

## You already use objects

Everything in Python is an object. Strings, lists and dictionaries are classes with methods.

```python tryit
name = "ada"
print(type(name))          # <class 'str'>
print(name.upper())        # a method of str

numbers = [3, 1, 2]
numbers.sort()             # a method of list
print(numbers)
```

## The four ideas of OOP

- **Encapsulation** - keep an object's data and rules together and protect them.
- **Inheritance** - build a new class on top of an existing one.
- **Polymorphism** - different classes answer the same method call in their own way.
- **Abstraction** - use an object through simple methods without knowing its insides.

You will meet each of them in this course.

```quiz
[
  {"question": "What is a class?", "options": ["One object", "A blueprint for objects", "A kind of loop"], "answer": 1, "explanation": "A class describes what its objects store and can do."},
  {"question": "What do we call a function that belongs to a class?", "options": ["attribute", "method", "module"], "answer": 1, "explanation": "Functions inside a class are methods."},
  {"question": "Is a Python list an object?", "options": ["Yes", "No"], "answer": 0, "explanation": "Everything in Python is an object; list is a class."}
]
```
