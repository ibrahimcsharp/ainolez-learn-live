---
title: Python None
slug: none
summary: The value that means "nothing here yet", and how to test for it.
minutes: 6
---
## A value for "no value"

`None` is a special value that means *nothing*, *unknown* or *not set yet*. It has its own type, `NoneType`.

```python tryit
winner = None
print(winner)
print(type(winner))
```

`None` is not the same as `0`, `""` or `False`. Those are real values; `None` says there is no value at all.

## Functions return None by default

A function without a `return` line still gives back a value: `None`.

```python tryit
def say_hi():
    print("hi")

result = say_hi()
print(result)
```

## Testing for None

Use `is None` or `is not None`. This checks whether the value is exactly the one `None` object.

```python tryit
middle_name = None

if middle_name is None:
    print("No middle name")
else:
    print("Middle name:", middle_name)
```

!!! note
    `if not value:` is also true for `0` and `""`. When `0` is a valid answer, test `is None` instead.

## None as a starting value

`None` is handy for "not found yet" while you search.

```python tryit
scores = [55, 81, 74, 92, 68]
best = None
for score in scores:
    if best is None or score > best:
        best = score
print("Best score:", best)
```

## Optional parameters

Use `None` as a default when "not given" must be different from any real value.

```python tryit
def describe(name, age=None):
    if age is None:
        return f"{name} (age unknown)"
    return f"{name}, {age}"

print(describe("Lina"))
print(describe("Omar", 0))
```

## Summary

- `None` means no value; its type is `NoneType`.
- Functions without `return` give back `None`.
- Test with `is None` / `is not None`.

```exercise
{
  "title": "First long word",
  "prompt_md": "Find the first word with more than 5 letters. Start with `found = None` and print `found` at the end. The output must be `banana`. If no word matched, `None` would be printed.",
  "starter_code": "words = [\"fig\", \"kiwi\", \"banana\", \"cherries\"]\nfound = None\n",
  "solution_code": "words = [\"fig\", \"kiwi\", \"banana\", \"cherries\"]\nfound = None\nfor word in words:\n    if len(word) > 5:\n        found = word\n        break\nprint(found)",
  "check_type": "output",
  "expected_value": "banana",
  "hint": "Loop over the words; when len(word) > 5, store it and break."
}
```

```quiz
[
  {"question": "What does a function return if it has no return statement?", "options": ["0", "None", "False"], "answer": 1, "explanation": "Python returns None automatically."},
  {"question": "What is the best way to check that x has no value?", "options": ["x == 0", "x is None", "x == \"\""], "answer": 1, "explanation": "is None checks for exactly the None value."},
  {"question": "Is None the same as 0?", "options": ["Yes", "No"], "answer": 1, "explanation": "0 is a number; None means no value."}
]
```
