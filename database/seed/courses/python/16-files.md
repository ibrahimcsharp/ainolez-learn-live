---
title: Python Files
slug: files
summary: Write and read text files and use with so files are always closed.
minutes: 7
---
## Writing a file

`open()` opens a file. The second argument is the mode: `"w"` writes (and replaces the file), `"a"` adds to the end, `"r"` reads.

```python tryit
with open("notes.txt", "w") as file:
    file.write("Learn it.\n")
    file.write("Code it.\n")
    file.write("Own it.\n")
print("Saved")
```

`with` closes the file for you, even if an error happens. Always use it.

!!! note
    In this editor files live in your browser's memory and disappear when you reload. On your own computer they are saved on disk.

## Reading a file

```python tryit
with open("notes.txt", "w") as file:
    file.write("Learn it.\nCode it.\nOwn it.\n")

with open("notes.txt") as file:
    text = file.read()
print(text)

with open("notes.txt") as file:
    for number, line in enumerate(file, start=1):
        print(number, line.strip())
```

`strip()` removes the line break at the end of each line.

## Adding to a file

```python tryit
with open("log.txt", "w") as file:
    file.write("first entry\n")
with open("log.txt", "a") as file:
    file.write("second entry\n")

with open("log.txt") as file:
    print(file.readlines())
```

## Missing files

Reading a file that does not exist raises `FileNotFoundError`; handle it with `try` / `except`.

```python tryit
try:
    with open("missing.txt") as file:
        print(file.read())
except FileNotFoundError:
    print("No such file yet")
```

## Summary

- `open(name, mode)`: `"w"` write, `"a"` append, `"r"` read.
- `with open(...) as file:` always closes the file.
- `read()` gives all text; looping over the file gives lines.

```exercise
{
  "title": "Count lines",
  "prompt_md": "The starter code writes a file with three cities. Read it back and print how many lines it has. The output must be exactly `3`.",
  "starter_code": "with open(\"cities.txt\", \"w\") as file:\n    file.write(\"Paris\\nTokyo\\nLima\\n\")\n\n# read the file and print the number of lines\n",
  "solution_code": "with open(\"cities.txt\", \"w\") as file:\n    file.write(\"Paris\\nTokyo\\nLima\\n\")\n\nwith open(\"cities.txt\") as file:\n    print(len(file.readlines()))",
  "check_type": "output",
  "expected_value": "3",
  "hint": "file.readlines() returns a list of lines; len() counts them."
}
```

```quiz
[
  {"question": "Which mode adds to the end of a file?", "options": ["\"w\"", "\"a\"", "\"r\""], "answer": 1, "explanation": "\"a\" (append) keeps the old text and adds new text after it."},
  {"question": "Why use with open(...)?", "options": ["It is faster", "It closes the file automatically", "It is required for reading"], "answer": 1, "explanation": "with makes sure the file is closed, even after an error."}
]
```
