---
title: Python Inner Classes and Composition
slug: inner-classes
summary: Define a class inside another, and build objects out of other objects.
minutes: 7
---
## A class inside a class

You can define a class inside another class. The inner class belongs to the outer one and is reached through it: `Outer.Inner`. This keeps small helper classes next to the only class that uses them.

```python tryit
class Car:
    class Engine:
        def __init__(self, horsepower):
            self.horsepower = horsepower

        def start(self):
            return f"{self.horsepower} hp engine started"

    def __init__(self, model, horsepower):
        self.model = model
        self.engine = Car.Engine(horsepower)

    def drive(self):
        return f"{self.model}: {self.engine.start()}"

car = Car("Civic", 158)
print(car.drive())

spare = Car.Engine(90)    # you can still create one from outside
print(spare.start())
```

!!! note
    An inner class does **not** get access to the outer object automatically. If it needs it, pass it in, as you would to any class.

## When to nest

Nesting is only about organisation - grouping names. Use it for small classes that make no sense on their own, such as configuration or the parts of a data structure:

```python tryit
class Playlist:
    class Song:
        def __init__(self, title, seconds):
            self.title = title
            self.seconds = seconds

    def __init__(self, name):
        self.name = name
        self.songs = []

    def add(self, title, seconds):
        self.songs.append(Playlist.Song(title, seconds))

    def length(self):
        total = sum(song.seconds for song in self.songs)
        return f"{total // 60}:{total % 60:02d}"

mix = Playlist("Focus")
mix.add("Rain", 185)
mix.add("Waves", 242)
print(mix.name, len(mix.songs), "songs,", mix.length())
```

If other code uses the inner class a lot, make it a normal top-level class instead.

## Composition: objects made of objects

Both examples above use **composition**: an object holds other objects as attributes. A car *has an* engine; a playlist *has* songs. Composition is often a better choice than inheritance:

- Inheritance: "is a" - a `Manager` **is an** `Employee`.
- Composition: "has a" - a `Car` **has an** `Engine`.

```python tryit
class Wheel:
    def __init__(self, size):
        self.size = size

class Bike:
    def __init__(self):
        self.wheels = [Wheel(28), Wheel(28)]

    def wheel_sizes(self):
        return [wheel.size for wheel in self.wheels]

print(Bike().wheel_sizes())
```

## Summary

- An inner class is defined inside another and used as `Outer.Inner`.
- It is a way to group code, not a special link between objects.
- Composition ("has a") builds objects from other objects.

```exercise
{
  "title": "Classroom",
  "prompt_md": "Inside `School`, define an inner class `Room` whose `__init__` stores `number` and `seats`. `School.add_room()` creates a `School.Room` and appends it to `self.rooms`. The code must print `2 rooms, 55 seats`.",
  "starter_code": "class School:\n    # define the inner class Room here\n\n    def __init__(self):\n        self.rooms = []\n\n    def add_room(self, number, seats):\n        pass  # create a School.Room and append it\n\nschool = School()\nschool.add_room(101, 30)\nschool.add_room(102, 25)\nprint(f\"{len(school.rooms)} rooms, {sum(r.seats for r in school.rooms)} seats\")\n",
  "solution_code": "class School:\n    class Room:\n        def __init__(self, number, seats):\n            self.number = number\n            self.seats = seats\n\n    def __init__(self):\n        self.rooms = []\n\n    def add_room(self, number, seats):\n        self.rooms.append(School.Room(number, seats))\n\nschool = School()\nschool.add_room(101, 30)\nschool.add_room(102, 25)\nprint(f\"{len(school.rooms)} rooms, {sum(r.seats for r in school.rooms)} seats\")\n",
  "check_type": "output",
  "expected_value": "2 rooms, 55 seats",
  "hint": "class Room: goes inside class School:, indented. In add_room write self.rooms.append(School.Room(number, seats))."
}
```

```quiz
[
  {"question": "How do you create an inner class Engine of Car from outside?", "options": ["Engine()", "Car.Engine()", "Car().Engine"], "answer": 1, "explanation": "Reach it through the outer class."},
  {"question": "Can an inner class read the outer object's attributes automatically?", "options": ["Yes", "No, you must pass the object in"], "answer": 1, "explanation": "Nesting only groups names."},
  {"question": "\"A library has books\" describes...", "options": ["inheritance", "composition"], "answer": 1, "explanation": "Has-a relationships are composition."}
]
```
