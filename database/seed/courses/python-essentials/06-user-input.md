---
title: Python User Input
slug: user-input
summary: Read what the user types with input(), convert it, and check it before you use it.
minutes: 8
---
## Asking a question

`input()` shows a message, waits for the user to type something and press Enter, and returns what they typed **as a string**.

```python
name = input("What is your name? ")
print(f"Nice to meet you, {name}!")
```

Run this on your own computer (in a terminal or an editor such as VS Code or IDLE) to type an answer.

!!! note
    The examples on this page replace `input()` with a fixed answer, so they run the same way every time in the browser. In your own programs, use `input()`.

## Input is always text

Even if the user types `42`, you get the string `"42"`. Convert it before doing maths.

```python tryit
answer = "42"          # pretend the user typed 42
print(answer + "1")    # 421 - joined as text
age = int(answer)
print(age + 1)         # 43
```

## Cleaning the answer

Users add spaces and mix capitals. `strip()` and `lower()` make answers easier to compare.

```python tryit
answer = "  YES "      # what the user typed
if answer.strip().lower() == "yes":
    print("Great, let's go!")
```

## Checking the answer

Never trust input. Check that it is valid and ask again if it is not.

```python tryit
attempts = ["abc", "-5", "21"]   # pretend the user typed these, one per question

for text in attempts:
    if text.isdigit():
        age = int(text)
        print("Thanks, age", age)
        break
    print(f"'{text}' is not a valid age, please try again")
```

In a real program the loop looks like this:

```python
while True:
    text = input("Your age: ")
    if text.isdigit():
        age = int(text)
        break
    print("Please type a whole number.")
```

## Several values on one line

`split()` cuts the answer into a list of words.

```python tryit
line = "3 7 12"            # pretend the user typed: 3 7 12
numbers = [int(part) for part in line.split()]
print(numbers, sum(numbers))
```

## Summary

- `input("question ")` returns what the user typed, always as a string.
- Convert with `int()` / `float()` and clean with `strip()` / `lower()`.
- Check input before using it, and ask again if it is wrong.

```exercise
{
  "title": "Tidy the answer",
  "prompt_md": "The user typed `answer` with extra spaces and capitals. Clean it with `strip()` and `title()` and print the greeting `Hello, Maria Lopez!`.",
  "starter_code": "answer = \"   maria LOPEZ  \"\n",
  "solution_code": "answer = \"   maria LOPEZ  \"\nname = answer.strip().title()\nprint(f\"Hello, {name}!\")",
  "check_type": "output",
  "expected_value": "Hello, Maria Lopez!",
  "hint": "answer.strip() removes the spaces; .title() capitalises each word."
}
```

```quiz
[
  {"question": "What type does input() always return?", "options": ["int", "str", "it depends on what was typed"], "answer": 1, "explanation": "input() always returns a string."},
  {"question": "The user types 5. What does input() + \"0\" give?", "options": ["50", "\"50\"", "5"], "answer": 1, "explanation": "Both are strings, so they are joined into \"50\"."},
  {"question": "Which method checks that text contains only digits?", "options": ["isdigit()", "isnumber()", "int()"], "answer": 0, "explanation": "str.isdigit() returns True when every character is a digit."}
]
```
