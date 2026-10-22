---
title: How to Print Tables and Patterns with Loops
slug: loop-patterns
summary: Classic loop programs - a times table, FizzBuzz, triangles of stars and a number grid - and how to plan them row by row.
minutes: 9
---
## Plan row by row

Most pattern programs have the same shape: an **outer loop** for each row and, inside it, a way to build that row. Work out what changes from one row to the next, then write that as code.

## A times table

```python tryit
number = 7
for i in range(1, 11):
    print(f"{number} x {i:>2} = {number * i:>3}")
```

A full grid needs two loops: one for the rows and one for the columns. `end=""` keeps `print` on the same line.

```python tryit
size = 5
for row in range(1, size + 1):
    for col in range(1, size + 1):
        print(f"{row * col:>4}", end="")
    print()          # finish the row
```

## FizzBuzz

Count from 1 to 15. For multiples of 3 print `Fizz`, for multiples of 5 print `Buzz`, for multiples of both print `FizzBuzz`, otherwise the number. The trick is to test "both" **first**.

```python tryit
for n in range(1, 16):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
```

Another way builds the word piece by piece. `word or n` prints the number when the word is empty.

```python tryit
for n in range(1, 16):
    word = ""
    if n % 3 == 0:
        word += "Fizz"
    if n % 5 == 0:
        word += "Buzz"
    print(word or n, end=" ")
```

## Triangles of stars

Multiplying a string repeats it, so row `i` is just `"*" * i`.

```python tryit
height = 4
for i in range(1, height + 1):
    print("*" * i)

print()
for i in range(height, 0, -1):     # upside down
    print("*" * i)
```

## A centred pyramid

Each row has `2 * i - 1` stars and fewer spaces in front as it goes down.

```python tryit
height = 4
for i in range(1, height + 1):
    spaces = " " * (height - i)
    stars = "*" * (2 * i - 1)
    print(spaces + stars)
```

`str.center()` can do the padding: `("*" * (2 * i - 1)).center(2 * height - 1)`.

## A number triangle

```python tryit
for row in range(1, 6):
    print(" ".join(str(n) for n in range(1, row + 1)))
```

```exercise
{
  "title": "Number staircase",
  "prompt_md": "Print this staircase, where row `i` repeats the number `i`, `i` times:\n\n```\n1\n22\n333\n4444\n```",
  "starter_code": "for i in range(1, 5):\n    pass",
  "solution_code": "for i in range(1, 5):\n    print(str(i) * i)",
  "check_type": "output",
  "expected_value": "1\n22\n333\n4444",
  "hint": "str(i) * i repeats the digit i times."
}
```

```exercise
{
  "title": "FizzBuzz to 15",
  "prompt_md": "Write FizzBuzz for the numbers 1 to 15, one result per line: `Fizz` for multiples of 3, `Buzz` for multiples of 5, `FizzBuzz` for multiples of both, otherwise the number.",
  "starter_code": "for n in range(1, 16):\n    pass",
  "solution_code": "for n in range(1, 16):\n    if n % 15 == 0:\n        print(\"FizzBuzz\")\n    elif n % 3 == 0:\n        print(\"Fizz\")\n    elif n % 5 == 0:\n        print(\"Buzz\")\n    else:\n        print(n)",
  "check_type": "output",
  "expected_value": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
  "hint": "Check n % 15 == 0 first, then n % 3, then n % 5."
}
```

```quiz
[
  {"question": "What does print(\"ab\" * 3) show?", "options": ["ab3", "ababab", "an error"], "answer": 1, "explanation": "Multiplying a string repeats it."},
  {"question": "In FizzBuzz, why test for 15 first?", "options": ["It is faster", "Otherwise 15 would stop at Fizz", "15 is the last number"], "answer": 1, "explanation": "elif stops at the first true test, and 15 is also a multiple of 3."},
  {"question": "What does print(\"x\", end=\"\") do?", "options": ["Prints nothing", "Prints x without a new line", "Prints x twice"], "answer": 1, "explanation": "end replaces the new line print normally adds."}
]
```
