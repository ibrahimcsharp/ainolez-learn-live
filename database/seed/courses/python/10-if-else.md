---
title: Python If ... Else
slug: if-else
summary: Make your program choose what to do with if, elif and else.
minutes: 8
---
## The if statement

`if` runs a block of code only when a condition is `True`. The block is the indented lines below it.

```python tryit
temperature = 34
if temperature > 30:
    print("It is hot today")
    print("Drink water")
print("This line always runs")
```

!!! note
    Python uses **indentation** (usually 4 spaces) to know which lines belong to the `if`. Other languages use `{ }`.

## else and elif

```python tryit
score = 72
if score >= 90:
    print("Grade A")
elif score >= 70:
    print("Grade B")
elif score >= 50:
    print("Grade C")
else:
    print("Try again")
```

Python checks the conditions from top to bottom and runs only the **first** block whose condition is true.

## Conditions with and / or

```python tryit
age = 15
with_parent = True
if age >= 16 or with_parent:
    print("You can watch the film")
else:
    print("Sorry, not today")
```

## Short form

For simple choices you can write the `if` in one line:

```python tryit
stock = 0
message = "in stock" if stock > 0 else "sold out"
print(message)
```

## Summary

- `if` runs indented code when a condition is true.
- `elif` adds more conditions; `else` catches the rest.
- Only the first matching branch runs.

```exercise
{
  "title": "Even or odd",
  "prompt_md": "Print `even` if `n` is even and `odd` if it is odd. With `n = 7` the output must be exactly `odd`.",
  "starter_code": "n = 7\n",
  "solution_code": "n = 7\nif n % 2 == 0:\n    print(\"even\")\nelse:\n    print(\"odd\")",
  "check_type": "output",
  "expected_value": "odd",
  "hint": "A number is even when n % 2 == 0."
}
```

```quiz
[
  {"question": "How does Python know which lines belong to an if?", "options": ["By curly brackets", "By indentation", "By semicolons"], "answer": 1, "explanation": "The indented lines under the if form its block."},
  {"question": "If x = 5, what prints? if x > 3: print(\"A\") elif x > 1: print(\"B\")", "options": ["A", "B", "A and B"], "answer": 0, "explanation": "Only the first true branch runs."}
]
```
