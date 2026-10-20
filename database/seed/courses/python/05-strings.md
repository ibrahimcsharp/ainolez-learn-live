---
title: Python Strings
slug: strings
summary: Work with text, join and slice strings, and build messages with f-strings.
minutes: 9
---
## Text in Python

Text values are called strings (`str`). Use single or double quotes; both work the same.

```python tryit
city = "Lagos"
greeting = 'Hello'
print(greeting, city)
print(len(city))   # number of characters
```

## Joining and repeating

```python tryit
first = "Ada"
last = "Lovelace"
print(first + " " + last)
print("ha" * 3)
```

`+` only joins strings with strings. To join a number, turn it into a string with `str()`, or use an f-string.

## f-strings

Put an `f` before the quotes and write variables inside `{ }`. This is the easiest way to build messages.

```python tryit
name = "Ravi"
points = 120
print(f"{name} has {points} points")
print(f"Next level at {points + 30} points")
```

## Indexes and slices

Each character has a position (index), starting at 0. Negative indexes count from the end.

```python tryit
word = "Python"
print(word[0])    # P
print(word[-1])   # n
print(word[0:3])  # Pyt  (from 0 up to, not including, 3)
print(word[2:])   # thon
```

## Useful methods

```python tryit
text = "  Learn it. Code it.  "
print(text.strip())
print(text.upper())
print(text.replace("it", "Python"))
print("code" in text)
print("a,b,c".split(","))
```

Strings never change in place: methods like `upper()` return a new string.

## Summary

- Strings are text in quotes; `len()` counts characters.
- f-strings put values into text: `f"{name}"`.
- `word[0]` is the first character, `word[1:4]` a slice.

```exercise
{
  "title": "Initials",
  "prompt_md": "Use indexes on `first` and `last` and an f-string to print the initials with dots, so the output is exactly `G.R.`",
  "starter_code": "first = \"Grace\"\nlast = \"Rossi\"\n",
  "solution_code": "first = \"Grace\"\nlast = \"Rossi\"\nprint(f\"{first[0]}.{last[0]}.\")",
  "check_type": "output",
  "expected_value": "G.R.",
  "hint": "first[0] is the first letter. Inside an f-string write {first[0]}."
}
```

```quiz
[
  {"question": "What is \"Python\"[1]?", "options": ["P", "y", "t"], "answer": 1, "explanation": "Indexes start at 0, so index 1 is the second character."},
  {"question": "What does f\"{2 + 3} apples\" give?", "options": ["{2 + 3} apples", "5 apples", "2 + 3 apples"], "answer": 1, "explanation": "Expressions inside { } are worked out."},
  {"question": "What does \"a-b\".split(\"-\") return?", "options": ["[\"a\", \"b\"]", "\"ab\"", "[\"a-b\"]"], "answer": 0, "explanation": "split() cuts the string at each separator and returns a list."}
]
```
