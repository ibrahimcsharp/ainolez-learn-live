---
title: Python String Methods
slug: string-methods
summary: The string methods you use every day - change case, trim, search, replace, split, join, check and pad text.
minutes: 12
---
## Methods return a new string

A **method** is a function that belongs to a value; you call it with a dot: `text.upper()`. Because strings are immutable, string methods never change the original. They **return a new string**, so keep the result.

```python tryit
city = "lisbon"
city.upper()
print(city)          # still lisbon
city = city.upper()
print(city)          # LISBON
```

## Changing case

```python tryit
title = "the old man and THE sea"
print(title.upper())       # all capitals
print(title.lower())       # all small letters
print(title.capitalize())  # first letter only
print(title.title())       # Each Word Capitalised
print(title.swapcase())    # flips every letter
```

To compare text without caring about case, lower both sides first: `answer.lower() == "yes"`.

## Trimming spaces

`strip()` removes spaces (and new lines and tabs) from both ends. `lstrip()` and `rstrip()` do one side only. Give it characters to remove something else.

```python tryit
raw = "   hello there \n"
print("[" + raw.strip() + "]")
print("[" + raw.lstrip() + "]")
print("$$$42.00$$".strip("$"))
print("www.example.org".removeprefix("www."))
```

## Finding text

| Method | Gives |
|---|---|
| `find(x)` | the index of the first `x`, or `-1` if missing |
| `index(x)` | like `find`, but raises `ValueError` if missing |
| `count(x)` | how many times `x` appears |
| `startswith(x)` / `endswith(x)` | `True` or `False` |

```python tryit
sentence = "a banana and a mango"
print(sentence.find("an"))         # 3
print(sentence.find("kiwi"))       # -1
print(sentence.count("a"))         # 7
print(sentence.startswith("a b"))  # True
print("report.pdf".endswith((".pdf", ".doc")))  # a tuple checks several
```

## Replacing text

`replace(old, new)` swaps every match. A third number limits how many.

```python tryit
note = "red car, red door, red hat"
print(note.replace("red", "blue"))
print(note.replace("red", "blue", 1))
print(note.replace(" ", ""))   # remove every space
```

## Split and join

`split()` cuts a string into a **list**. With no argument it splits on any run of spaces. `join()` is the opposite: it glues a list of strings together, using the string you call it on as the glue.

```python tryit
line = "milk,eggs,flour,sugar"
items = line.split(",")
print(items)
print(" | ".join(items))

words = "  too   many    spaces  ".split()
print(words)
print(" ".join(words))   # tidy text

print("one\ntwo\nthree".splitlines())
```

## Checking what is inside

These methods return `True` or `False` and are useful for checking input.

```python tryit
for value in ["2024", "abc", "abc123", "   ", "Hello World"]:
    print(repr(value), value.isdigit(), value.isalpha(), value.isalnum(), value.isspace(), value.istitle())
```

`repr()` shows the value with its quotes, so you can see the spaces.

## Lining text up

`ljust`, `rjust` and `center` pad a string to a width. `zfill` pads a number string with zeros.

```python tryit
print("[" + "left".ljust(10) + "]")
print("[" + "right".rjust(10) + "]")
print("[" + "mid".center(9, "*") + "]")
print("7".zfill(3), "42".zfill(3))
```

## Chaining methods

Each method returns a string, so you can call the next method straight away. Python runs them left to right.

```python tryit
messy = "  mary-JANE watson "
clean = messy.strip().lower().replace("-", " ").title()
print(clean)
```

## Summary

- String methods return a **new** string; store the result.
- `upper`, `lower`, `title` change case; `strip` trims the ends.
- `find`, `count`, `startswith` search; `replace` swaps text.
- `split` makes a list; `"glue".join(list)` makes a string.
- `isdigit`, `isalpha` and friends check what the text contains.

```exercise
{
  "title": "Make a username",
  "prompt_md": "Turn the full name into a username: remove the spaces at the ends, make it lower case and replace the space between the words with a dot. Print `ada.lovelace`.",
  "starter_code": "full_name = \"   Ada Lovelace  \"\n",
  "solution_code": "full_name = \"   Ada Lovelace  \"\nusername = full_name.strip().lower().replace(\" \", \".\")\nprint(username)",
  "check_type": "output",
  "expected_value": "ada.lovelace",
  "hint": "Chain the methods: full_name.strip().lower().replace(\" \", \".\")"
}
```

```exercise
{
  "title": "Tags to hashtags",
  "prompt_md": "`tags` holds words separated by commas, with untidy spaces. Split it, strip each word, put `#` in front and join them with single spaces. Print `#python #coding #learning`.",
  "starter_code": "tags = \"python, coding ,learning\"\n",
  "solution_code": "tags = \"python, coding ,learning\"\nparts = [\"#\" + tag.strip() for tag in tags.split(\",\")]\nprint(\" \".join(parts))",
  "check_type": "output",
  "expected_value": "#python #coding #learning",
  "hint": "tags.split(\",\") gives the pieces; strip each one, add \"#\", then \" \".join(...)."
}
```

```quiz
[
  {"question": "name = \"sam\"; name.upper(). What is name now?", "options": ["SAM", "sam", "Sam"], "answer": 1, "explanation": "Methods return a new string; name itself does not change unless you assign the result."},
  {"question": "What does \"hello\".find(\"z\") return?", "options": ["None", "-1", "a ValueError"], "answer": 1, "explanation": "find returns -1 when the text is not there; index would raise ValueError."},
  {"question": "What does \"-\".join([\"a\", \"b\", \"c\"]) give?", "options": ["a-b-c", "-a-b-c-", "[a-b-c]"], "answer": 0, "explanation": "The glue goes only between the items."},
  {"question": "Which check is True for \"2024\"?", "options": ["isalpha()", "isdigit()", "isspace()"], "answer": 1, "explanation": "Every character is a digit."}
]
```
