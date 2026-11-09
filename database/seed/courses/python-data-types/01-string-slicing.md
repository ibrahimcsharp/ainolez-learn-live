---
title: Python String Slicing and Special Characters
slug: string-slicing
summary: Pick characters and pieces out of text with indexes and slices, and write quotes, new lines and tabs inside strings.
minutes: 10
---
## A string is a row of characters

Every character in a string has a position, called its **index**. Counting starts at `0`. Negative indexes count from the end: `-1` is the last character.

```python tryit
word = "keyboard"
print(word[0])    # k
print(word[3])    # b
print(word[-1])   # d
print(word[-3])   # a
print(len(word))  # 8 characters
```

Asking for a position that does not exist, like `word[20]`, gives an `IndexError`.

## Slices: a piece of the string

`text[start:stop]` gives the characters from `start` up to, **but not including**, `stop`. Leave out `start` to begin at the start; leave out `stop` to go to the end.

```python tryit
code = "GB-LON-2041"
print(code[0:2])    # GB
print(code[3:6])    # LON
print(code[7:])     # 2041  (from 7 to the end)
print(code[:6])     # GB-LON (from the start to 6)
print(code[-4:])    # 2041  (the last four)
```

A useful way to think about it: the numbers point to the **gaps between** characters, and the slice takes everything between two gaps.

## A step: every second character

A third number is the **step**. A step of `2` takes every second character; a step of `-1` walks backwards, which reverses the text.

```python tryit
letters = "abcdefghij"
print(letters[::2])    # acegi
print(letters[1::2])   # bdfhj
print(letters[::-1])   # jihgfedcba
print(letters[2:8:3])  # cf
```

Slices never raise an error: a slice that runs past the end just stops there.

## Strings cannot be changed in place

Strings are **immutable**. `word[0] = "K"` is an error. Build a new string instead.

```python tryit
word = "python"
word = "P" + word[1:]
print(word)   # Python
```

## Special characters with a backslash

Some characters are hard to type inside quotes. A backslash `\` starts an **escape sequence**:

| Write | You get |
|---|---|
| `\n` | a new line |
| `\t` | a tab |
| `\'` and `\"` | a quote that does not end the string |
| `\\` | one backslash |

```python tryit
print("Name:\tAisha\nCity:\tLagos")
print("She said \"hi\" and left.")
print('It\'s raining.')
print("C:\\games\\save.txt")
```

## Raw strings and triple quotes

Put `r` before the quotes and backslashes are kept as plain characters. This is handy for Windows paths and regular expressions.

Triple quotes (`"""` or `'''`) let a string run over several lines.

```python tryit
path = r"C:\new\table.csv"
print(path)

poem = """Roses are red,
code can be too,
when tests fail
in the morning dew."""
print(poem)
print(poem.count("\n"), "line breaks")
```

## Summary

- `text[i]` is one character; `-1` is the last one.
- `text[start:stop:step]` is a slice; `stop` is not included.
- `text[::-1]` reverses a string.
- `\n`, `\t`, `\"` and `\\` are escape sequences; `r"..."` turns them off.
- Triple quotes make multi-line strings.

```exercise
{
  "title": "Cut up a product code",
  "prompt_md": "The code `SHOE-0042-BLK` has three parts: a category, a number and a colour. Use **slices** (not `split`) to print the three parts, one per line:\n\n```\nSHOE\n0042\nBLK\n```",
  "starter_code": "code = \"SHOE-0042-BLK\"\n",
  "solution_code": "code = \"SHOE-0042-BLK\"\nprint(code[:4])\nprint(code[5:9])\nprint(code[-3:])",
  "check_type": "output",
  "expected_value": "SHOE\n0042\nBLK",
  "hint": "The dashes are at index 4 and 9. code[:4] is the first part; code[-3:] is the last three characters."
}
```

```exercise
{
  "title": "Hidden word",
  "prompt_md": "A word is hidden in `secret`: read it **backwards**, taking every second character and starting from the last one. Use one slice and print the word. The output must be `python`.",
  "starter_code": "secret = \"n4o7h1t9y2p\"\n",
  "solution_code": "secret = \"n4o7h1t9y2p\"\nprint(secret[::-2])",
  "check_type": "output",
  "expected_value": "python",
  "hint": "A negative step walks backwards: secret[::-2]."
}
```

```quiz
[
  {"question": "What is \"planet\"[1:4]?", "options": ["pla", "lan", "lane"], "answer": 1, "explanation": "Index 1 is l, and the slice stops before index 4."},
  {"question": "What does \"abc\"[::-1] give?", "options": ["abc", "cba", "an error"], "answer": 1, "explanation": "A step of -1 walks backwards through the string."},
  {"question": "Which escape sequence starts a new line?", "options": ["\\t", "\\n", "\\\\"], "answer": 1, "explanation": "\\n is a new line; \\t is a tab."},
  {"question": "What happens with word[0] = \"X\" when word is a string?", "options": ["The first letter changes", "A TypeError, strings are immutable", "A new string is added"], "answer": 1, "explanation": "Strings cannot be changed in place; build a new one instead."}
]
```
