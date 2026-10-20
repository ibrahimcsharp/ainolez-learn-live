---
title: Python Regular Expressions
slug: regex
summary: Find, check and replace patterns in text with the re module.
minutes: 11
---
## Patterns, not exact text

A regular expression (regex) describes a **pattern** of text, such as "three digits" or "an email address". Python's `re` module searches with them.

```python tryit
import re

text = "Order 4521 shipped on 12 May, order 77 is waiting."
print(re.findall(r"\d+", text))   # every run of digits
```

`\d` means *a digit* and `+` means *one or more*. The `r` before the quotes makes a raw string, so backslashes are kept as they are.

## The building blocks

| Pattern | Matches |
|---|---|
| `.` | any character except a new line |
| `\d` / `\D` | a digit / not a digit |
| `\w` / `\W` | a word character (letter, digit, `_`) / not one |
| `\s` / `\S` | whitespace / not whitespace |
| `[aeiou]` | one of these characters |
| `[^0-9]` | any character **except** these |
| `^` / `$` | start / end of the text |
| `*` `+` `?` | 0 or more, 1 or more, 0 or 1 |
| `{3}` `{2,4}` | exactly 3, from 2 to 4 |
| `a|b` | a or b |

```python tryit
import re

print(re.findall(r"[aeiou]", "regular expression"))
print(re.findall(r"\b\w{5}\b", "these words have five chars maybe"))
print(re.findall(r"colou?r", "color and colour"))
```

## search() and match objects

`re.search()` finds the **first** match and returns a match object, or `None`.

```python tryit
import re

found = re.search(r"\d{4}", "Call room 12 or office 3307 today")
if found:
    print(found.group())   # the matched text
    print(found.start())   # where it starts
```

## Checking a whole value: fullmatch()

To validate input, the **whole** text must fit the pattern.

```python tryit
import re

for code in ["AB-1234", "ab-1234", "AB-12345"]:
    ok = re.fullmatch(r"[A-Z]{2}-\d{4}", code)
    print(code, "valid" if ok else "invalid")
```

## Groups: pulling out parts

Brackets `( )` capture parts of the match.

```python tryit
import re

line = "2026-10-20 ERROR Disk full"
m = re.search(r"(\d{4})-(\d{2})-(\d{2}) (\w+)", line)
year, month, day, level = m.groups()
print(year, level)

# named groups are easier to read
m = re.search(r"(?P<user>\w+)@(?P<domain>[\w.]+)", "mail ana@example.com now")
print(m["user"], m["domain"])
```

## Replacing and splitting

```python tryit
import re

print(re.sub(r"\s+", " ", "too    many     spaces"))
print(re.sub(r"\d", "#", "PIN 4821"))
print(re.split(r"[,;]\s*", "red, green;blue,  yellow"))
```

## Summary

- `re.findall` returns every match; `re.search` the first; `re.fullmatch` checks the whole text.
- `\d \w \s` are digit, word and space; `+ * ? {n}` say how many.
- `( )` captures groups; `re.sub` replaces; `re.split` splits.

```exercise
{
  "title": "Find the hashtags",
  "prompt_md": "Use `re.findall()` to print a list of every hashtag in `post` (a `#` followed by word characters). The output must be `['#python', '#learn', '#code2026']`.",
  "starter_code": "import re\n\npost = \"Loving #python today! #learn something new, #code2026 :)\"\n",
  "solution_code": "import re\n\npost = \"Loving #python today! #learn something new, #code2026 :)\"\nprint(re.findall(r\"#\\w+\", post))",
  "check_type": "output",
  "expected_value": "['#python', '#learn', '#code2026']",
  "hint": "The pattern is r\"#\\w+\": a # followed by one or more word characters."
}
```

```quiz
[
  {"question": "What does \\d+ match?", "options": ["one digit", "one or more digits", "the letter d"], "answer": 1, "explanation": "\\d is a digit and + means one or more."},
  {"question": "Which function checks that the whole text fits a pattern?", "options": ["re.search", "re.findall", "re.fullmatch"], "answer": 2, "explanation": "fullmatch only succeeds if the entire string matches."},
  {"question": "What does re.sub(r\"a\", \"o\", \"banana\") return?", "options": ["bonono", "bonana", "banana"], "answer": 0, "explanation": "sub replaces every match."},
  {"question": "Why write r\"\\d\" with an r?", "options": ["It makes the pattern faster", "It keeps the backslash as it is", "It is required by re"], "answer": 1, "explanation": "Raw strings do not treat backslashes as escape characters."}
]
```
