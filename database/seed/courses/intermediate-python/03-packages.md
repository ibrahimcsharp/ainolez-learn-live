---
title: Modules, Packages, pip and venv
slug: packages
summary: Split a program into modules and packages, install libraries with pip and isolate them in a virtual environment.
minutes: 9
---
## Your own module

Any `.py` file is a module. If you have a file `shapes.py`:

```python
# shapes.py
PI = 3.14159

def circle_area(radius):
    return PI * radius ** 2
```

another file in the same folder can use it:

```python
# main.py
import shapes
from shapes import circle_area

print(shapes.PI)
print(circle_area(2))
```

## Packages

A **package** is a folder of modules. A typical project looks like this:

```
my_app/
    main.py
    geometry/
        __init__.py
        shapes.py
        units.py
```

You import from it with dots: `from geometry.shapes import circle_area`. The `__init__.py` file marks the folder as a package; it can be empty.

## Run only when executed directly

Code under this check runs when you start the file, but not when another file imports it:

```python tryit
def main():
    print("Running the program")

if __name__ == "__main__":
    main()
```

## Installing libraries with pip

`pip` downloads packages from the Python Package Index (PyPI). On your computer, in a terminal:

```
pip install requests
pip install "pandas>=2.2"
pip list
pip freeze > requirements.txt
pip install -r requirements.txt
```

`requirements.txt` lists the exact versions a project needs, so others can install the same ones.

## Virtual environments

Different projects may need different versions of the same library. A **virtual environment** gives each project its own private set of packages.

```
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install requests      # goes into .venv only
deactivate
```

!!! tip
    Create one virtual environment per project and add `.venv` to `.gitignore`. Share `requirements.txt` instead.

## Summary

- Every `.py` file is a module; a folder with `__init__.py` is a package.
- `if __name__ == "__main__":` guards code that should only run directly.
- `pip install` adds libraries; `python -m venv` keeps them per project.

```quiz
[
  {"question": "What makes a folder a regular package?", "options": ["A main.py file", "An __init__.py file", "A requirements.txt file"], "answer": 1, "explanation": "__init__.py marks the folder as a package."},
  {"question": "Why use a virtual environment?", "options": ["To make Python faster", "To keep each project's packages separate", "To run Python online"], "answer": 1, "explanation": "Each project gets its own isolated set of packages and versions."},
  {"question": "Which command saves the installed versions to a file?", "options": ["pip freeze > requirements.txt", "pip save", "python -m venv"], "answer": 0, "explanation": "pip freeze prints the installed packages with versions."}
]
```
