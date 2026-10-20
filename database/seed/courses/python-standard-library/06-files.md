---
title: Python File Handling
slug: files
summary: Create, read, append to and delete files and folders with open(), os and pathlib.
minutes: 11
---
## Opening files

`open(name, mode)` opens a file. The mode says what you want to do:

| Mode | Meaning |
|---|---|
| `"r"` | read (the default); error if the file does not exist |
| `"w"` | write; creates the file or **empties** it first |
| `"a"` | append; adds to the end, creates the file if needed |
| `"x"` | create; error if the file already exists |

Always use `with`: it closes the file for you, even if an error happens.

!!! note
    In the browser, files live in a temporary space that is cleared when you reload the page. On your computer they are saved to disk.

## Writing and appending

```python tryit
with open("diary.txt", "w") as file:
    file.write("Monday: started Python\n")
    file.write("Tuesday: learned files\n")

with open("diary.txt", "a") as file:
    file.write("Wednesday: loved it\n")

with open("diary.txt") as file:
    print(file.read())
```

`write()` does not add a new line by itself: put `\n` at the end.

## Reading line by line

Looping over a file gives one line at a time. This works even for huge files.

```python tryit
with open("todo.txt", "w") as file:
    file.write("buy milk\ncall Sam\nwater plants\n")

with open("todo.txt") as file:
    for number, line in enumerate(file, start=1):
        print(number, line.strip())

with open("todo.txt") as file:
    lines = file.read().splitlines()
print(lines)
```

## Does it exist? Deleting files

The `os` module talks to the operating system.

```python tryit
import os

with open("old.txt", "w") as file:
    file.write("delete me")

print(os.path.exists("old.txt"))
os.remove("old.txt")                 # delete the file
print(os.path.exists("old.txt"))

if os.path.exists("missing.txt"):
    os.remove("missing.txt")
else:
    print("Nothing to delete")
```

## Folders

```python tryit
import os

os.makedirs("reports/2026", exist_ok=True)   # create, with parents
with open("reports/2026/jan.txt", "w") as file:
    file.write("January")
print(os.listdir("reports/2026"))

os.remove("reports/2026/jan.txt")
os.rmdir("reports/2026")                     # only removes empty folders
print(os.path.exists("reports/2026"))
```

## pathlib: the modern way

`pathlib.Path` treats paths as objects. Join them with `/`.

```python tryit
from pathlib import Path

folder = Path("notes")
folder.mkdir(exist_ok=True)
note = folder / "idea.txt"
note.write_text("Build a quiz app")
print(note.read_text())
print(note.name, note.suffix, note.exists())
print([p.name for p in folder.glob("*.txt")])
note.unlink()                                # delete
```

## CSV files

Comma-separated files are common for tables. The `csv` module handles quotes and commas for you.

```python tryit
import csv

with open("scores.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "score"])
    writer.writerows([["Ana", 91], ["Ben", 78]])

with open("scores.csv", newline="") as file:
    for row in csv.DictReader(file):
        print(row["name"], int(row["score"]) + 5)
```

## Summary

- `open(name, "r" / "w" / "a" / "x")` inside `with`.
- `os.path.exists`, `os.remove`, `os.makedirs`, `os.rmdir` manage files and folders.
- `pathlib.Path` and the `csv` module make common jobs easier.

```exercise
{
  "title": "Count the lines",
  "prompt_md": "Write the three names to `team.txt` (one per line), then open it again, count the lines and print `3 people`. Finally delete the file with `os.remove()`.",
  "starter_code": "import os\n\nnames = [\"Ana\", \"Ben\", \"Cleo\"]\n",
  "solution_code": "import os\n\nnames = [\"Ana\", \"Ben\", \"Cleo\"]\nwith open(\"team.txt\", \"w\") as file:\n    for name in names:\n        file.write(name + \"\\n\")\nwith open(\"team.txt\") as file:\n    count = len(file.read().splitlines())\nprint(f\"{count} people\")\nos.remove(\"team.txt\")",
  "check_type": "output",
  "expected_value": "3 people",
  "hint": "Write each name with name + \"\\n\". Read back with file.read().splitlines() and use len()."
}
```

```quiz
[
  {"question": "Which mode empties a file before writing?", "options": ["\"a\"", "\"w\"", "\"r\""], "answer": 1, "explanation": "\"w\" starts with an empty file."},
  {"question": "Why use with open(...)?", "options": ["It is faster", "It closes the file automatically", "It makes a backup"], "answer": 1, "explanation": "with closes the file even when an error happens."},
  {"question": "Which function deletes a file?", "options": ["os.remove()", "os.rmdir()", "open(name, \"d\")"], "answer": 0, "explanation": "os.remove deletes a file; os.rmdir removes an empty folder."}
]
```
