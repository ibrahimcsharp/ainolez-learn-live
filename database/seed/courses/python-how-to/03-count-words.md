---
title: How to Count Words and Letters
slug: count-words
summary: Count the words in a text, how often each word appears, and the most common letters, using split, dictionaries and collections.Counter.
minutes: 8
---
## How many words?

`split()` with no argument splits on any run of spaces, tabs or new lines, so `len(text.split())` counts the words.

```python tryit
text = """The quick brown fox
jumps over   the lazy dog."""
words = text.split()
print(len(words), "words")
print(len(text), "characters,", len(text.replace(" ", "").replace("\n", "")), "without spaces")
```

## Cleaning before counting

To count "The" and "the" as the same word, and to ignore punctuation, clean the text first.

```python tryit
import string

text = "Rain, rain, go away! Come again another day, rain."
clean = text.lower().translate(str.maketrans("", "", string.punctuation))
print(clean)
print(clean.split())
```

`string.punctuation` holds all the usual punctuation marks; `translate` with `maketrans("", "", ...)` deletes them.

## How often does each word appear?

With a dictionary: start each word at 0 and add 1 every time you see it.

```python tryit
words = "rain rain go away come again another day rain".split()
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)
```

## The shortcut: collections.Counter

`Counter` does the counting for you and can list the most common items.

```python tryit
from collections import Counter

words = "rain rain go away come again another day rain".split()
counts = Counter(words)
print(counts["rain"])
print(counts["snow"])            # missing words count as 0
print(counts.most_common(2))
```

## Counting letters

A string is a sequence of characters, so `Counter` can count letters directly.

```python tryit
from collections import Counter

text = "Mississippi river"
letters = Counter(ch for ch in text.lower() if ch.isalpha())
for letter, number in letters.most_common(3):
    print(letter, "*" * number)
print("vowels:", sum(letters[v] for v in "aeiou"))
```

## A small word report

```python tryit
from collections import Counter
import string

def word_report(text, top=3):
    clean = text.lower().translate(str.maketrans("", "", string.punctuation))
    words = clean.split()
    print("words:", len(words), "| different:", len(set(words)))
    for word, number in Counter(words).most_common(top):
        print(f"  {word:<6}{number}")

word_report("To be, or not to be: that is the question. To be sure!")
```

```exercise
{
  "title": "Word frequencies",
  "prompt_md": "Count the words in `text` **ignoring capitals**, and print the two most common ones with their counts, one per line, most common first. The output must be:\n\n```\nthe 3\ncat 2\n```",
  "starter_code": "text = \"The cat and the hat saw The other cat\"\n",
  "solution_code": "from collections import Counter\n\ntext = \"The cat and the hat saw The other cat\"\ncounts = Counter(text.lower().split())\nfor word, number in counts.most_common(2):\n    print(word, number)",
  "check_type": "output",
  "expected_value": "the 3\ncat 2",
  "hint": "Counter(text.lower().split()).most_common(2) gives a list of (word, count) pairs."
}
```

```quiz
[
  {"question": "What does len(\"one  two\\nthree\".split()) give?", "options": ["2", "3", "4"], "answer": 1, "explanation": "split() with no argument splits on any whitespace, including new lines."},
  {"question": "What does Counter([\"a\", \"b\", \"a\"])[\"z\"] return?", "options": ["None", "0", "a KeyError"], "answer": 1, "explanation": "A Counter returns 0 for missing items."}
]
```
