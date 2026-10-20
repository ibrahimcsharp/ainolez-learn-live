---
title: Python Syntax and Comments
slug: syntax
summary: How Python reads your code - lines, indentation, blocks, comments and docstrings.
minutes: 8
---
## One instruction per line

A Python program is a list of instructions (statements). Python runs them from top to bottom, one line at a time.

```python tryit
print("first")
print("second")
total = 3 + 4
print(total)
```

There is no semicolon at the end of a line and no curly braces around blocks. Python uses something simpler: indentation.

## Indentation makes blocks

When a line ends with a colon (`:`), the lines that belong to it are **indented** (moved right). Together they form a block.

```python tryit
temperature = 31

if temperature > 30:
    print("It is hot")        # inside the if-block
    print("Drink some water") # also inside
print("Done")                 # outside: always runs
```

Use 4 spaces for each level. Every line in the same block must have the same indentation, otherwise Python stops with an `IndentationError`.

```python
if temperature > 30:
print("It is hot")      # IndentationError: expected an indented block
```

## Long lines

A statement inside brackets can continue over several lines. This keeps long lists or calls readable.

```python tryit
colours = [
    "red",
    "green",
    "blue",
]
total = (10 + 20 +
         30 + 40)
print(colours, total)
```

## Comments

A comment starts with `#`. Python ignores everything after it on that line, so comments are notes for humans.

```python tryit
# Work out the price of 3 tickets
price = 12.5
count = 3  # number of tickets
print(price * count)
# print("this line is switched off")
```

Good comments explain **why** you did something, not what the code obviously does.

## Docstrings

A string on the first line of a function describes what the function does. It is called a docstring, and tools such as `help()` show it.

```python tryit
def area(width, height):
    """Return the area of a rectangle."""
    return width * height

print(area(3, 4))
print(area.__doc__)
```

!!! tip
    Python has no special multi-line comment. Use several `#` lines, or a docstring for functions, classes and modules.

## Summary

- Python runs statements top to bottom, one per line.
- A colon starts a block; the block is indented by 4 spaces.
- `#` starts a comment; `"""..."""` at the top of a function is a docstring.

```exercise
{
  "title": "Fix the block",
  "prompt_md": "The `if` block is not indented, so the code fails. Indent the two `print` lines inside the `if` so the output is:\n\n```\nYou passed\nWell done\n```",
  "starter_code": "score = 72\nif score >= 50:\nprint(\"You passed\")\nprint(\"Well done\")\n",
  "solution_code": "score = 72\nif score >= 50:\n    print(\"You passed\")\n    print(\"Well done\")\n",
  "check_type": "output",
  "expected_value": "You passed\nWell done",
  "hint": "Put 4 spaces before each print line."
}
```

```quiz
[
  {"question": "What marks the start of a block in Python?", "options": ["{ curly braces }", "a colon and indentation", "the word begin"], "answer": 1, "explanation": "A line ending in : is followed by an indented block."},
  {"question": "Which character starts a comment?", "options": ["//", "#", "--"], "answer": 1, "explanation": "Python comments start with #."},
  {"question": "What is a docstring?", "options": ["A string that describes a function, written on its first line", "A comment that starts with ##", "A string printed when an error happens"], "answer": 0, "explanation": "Docstrings document functions, classes and modules."}
]
```
