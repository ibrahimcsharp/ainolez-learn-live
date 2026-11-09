---
title: How to Reverse a String
slug: reverse-string
summary: Reverse text with a slice, with reversed() and join, or with a loop, then use it to check for palindromes and reverse word order.
minutes: 7
---
## Way 1: a slice with step -1

A slice with a step of `-1` walks from the end to the start. This is the usual Python way.

```python tryit
word = "stressed"
print(word[::-1])   # desserts
```

Read `[::-1]` as "from the start, to the end, going backwards one at a time".

## Way 2: reversed() and join

`reversed()` gives the characters from last to first, one at a time. `"".join()` glues them back into a string.

```python tryit
word = "drawer"
backwards = "".join(reversed(word))
print(backwards)
```

This version reads more like English, and `reversed()` also works on lists and other sequences.

## Way 3: a loop

Building the result yourself shows what is going on: each new character goes in **front** of what you have so far.

```python tryit
word = "live"
result = ""
for ch in word:
    result = ch + result
    print(result)
print("final:", result)
```

## Make it a function

```python tryit
def reverse(text):
    return text[::-1]

for sample in ["level", "python", "12345", ""]:
    print(repr(sample), "->", repr(reverse(sample)))
```

## Use: is it a palindrome?

A **palindrome** reads the same backwards. For sentences, ignore spaces, punctuation and capitals first.

```python tryit
def is_palindrome(text):
    letters = "".join(ch.lower() for ch in text if ch.isalnum())
    return letters == letters[::-1]

for phrase in ["racecar", "Never odd or even", "hello", "Was it a car or a cat I saw?"]:
    print(f"{phrase!r}: {is_palindrome(phrase)}")
```

## Reversing the words, not the letters

Split into words, reverse the list, join again.

```python tryit
sentence = "practice makes progress"
print(" ".join(sentence.split()[::-1]))
print(" ".join(word[::-1] for word in sentence.split()))   # each word backwards
```

```exercise
{
  "title": "Reverse each name",
  "prompt_md": "Print each name in `names` reversed, one per line. The output must be:\n\n```\nanna\nnoel\nnomis\n```",
  "starter_code": "names = [\"anna\", \"leon\", \"simon\"]\n",
  "solution_code": "names = [\"anna\", \"leon\", \"simon\"]\nfor name in names:\n    print(name[::-1])",
  "check_type": "output",
  "expected_value": "anna\nnoel\nnomis",
  "hint": "name[::-1] reverses one name."
}
```

```exercise
{
  "title": "Find the palindromes",
  "prompt_md": "Write `is_palindrome(text)` that ignores capitals, spaces and punctuation. Print the phrases from `phrases` that are palindromes, one per line. The output must be:\n\n```\nStep on no pets\nA Santa at NASA\n```",
  "starter_code": "phrases = [\"Step on no pets\", \"Python rocks\", \"A Santa at NASA\"]\n",
  "solution_code": "def is_palindrome(text):\n    letters = \"\".join(ch.lower() for ch in text if ch.isalnum())\n    return letters == letters[::-1]\n\nphrases = [\"Step on no pets\", \"Python rocks\", \"A Santa at NASA\"]\nfor phrase in phrases:\n    if is_palindrome(phrase):\n        print(phrase)",
  "check_type": "output",
  "expected_value": "Step on no pets\nA Santa at NASA",
  "hint": "Keep only the characters where ch.isalnum() is True, lower them, and compare with the reversed version."
}
```

```quiz
[
  {"question": "What does \"abc\"[::-1] give?", "options": ["abc", "cba", "c"], "answer": 1, "explanation": "A step of -1 walks backwards."},
  {"question": "What type does reversed(\"abc\") return?", "options": ["the string \"cba\"", "an iterator you must join", "a list"], "answer": 1, "explanation": "reversed gives an iterator; \"\".join(...) turns it into a string."}
]
```
