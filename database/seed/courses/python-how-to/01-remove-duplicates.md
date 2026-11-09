---
title: How to Remove Duplicates from a List
slug: remove-duplicates
summary: Drop repeated items from a list, with or without keeping the original order, and remove duplicates that differ only in capitals.
minutes: 7
---
## The problem

You have a list with repeats, such as email sign-ups or tags, and you want each value only once.

```python tryit
tags = ["python", "web", "python", "data", "web", "ai"]
print(tags)
```

## Way 1: a set (order is lost)

A set cannot hold duplicates, so `set()` removes them instantly. But sets have no order, so the result may come back in a different order.

```python tryit
tags = ["python", "web", "python", "data", "web", "ai"]
unique = list(set(tags))
print(sorted(unique))   # sort it if you need a fixed order
```

Use this when order does not matter, or when you want the result sorted anyway.

## Way 2: dict.fromkeys (order is kept)

Dictionary keys are unique too, and dictionaries **remember the order** keys were added. `dict.fromkeys(items)` makes a key for each item; turning it back into a list gives the items in first-seen order.

```python tryit
tags = ["python", "web", "python", "data", "web", "ai"]
unique = list(dict.fromkeys(tags))
print(unique)   # ['python', 'web', 'data', 'ai']
```

This is the shortest way to keep the order, and it is fast even for long lists.

## Way 3: a loop with a "seen" set

Writing the loop yourself lets you decide what counts as a duplicate. Here, `"Web"` and `"web"` count as the same tag, but the first spelling is kept.

```python tryit
tags = ["Python", "web", "python", "Data", "Web", "AI"]

seen = set()
unique = []
for tag in tags:
    key = tag.lower()          # what makes two items "the same"
    if key not in seen:
        seen.add(key)
        unique.append(tag)
print(unique)
```

Checking `in` on a set is very fast. Checking `in` on a list gets slower as the list grows, so keep the "seen" values in a set.

## Lists you cannot put in a set

Sets and dictionary keys need values that cannot change. A list of lists cannot go into a set, but you can turn each inner list into a tuple first.

```python tryit
points = [[1, 2], [3, 4], [1, 2], [5, 6]]
unique = [list(p) for p in dict.fromkeys(tuple(p) for p in points)]
print(unique)
```

## Which one to use

| Need | Use |
|---|---|
| Just the unique values, any order | `set(items)` |
| Keep the original order | `list(dict.fromkeys(items))` |
| Your own rule for "the same" | a loop with a `seen` set |

```exercise
{
  "title": "Unique visitors in order",
  "prompt_md": "Remove the duplicate names from `visitors`, keeping the order in which each name **first** appeared, and print the list. The output must be `['Ola', 'Sam', 'Kit', 'Ana']`.",
  "starter_code": "visitors = [\"Ola\", \"Sam\", \"Ola\", \"Kit\", \"Sam\", \"Ana\", \"Ola\"]\n",
  "solution_code": "visitors = [\"Ola\", \"Sam\", \"Ola\", \"Kit\", \"Sam\", \"Ana\", \"Ola\"]\nprint(list(dict.fromkeys(visitors)))",
  "check_type": "output",
  "expected_value": "['Ola', 'Sam', 'Kit', 'Ana']",
  "hint": "list(dict.fromkeys(visitors)) keeps the first-seen order."
}
```

```exercise
{
  "title": "Unique emails, any capitals",
  "prompt_md": "Email addresses are not case sensitive. Keep the **first** spelling of each address and drop later ones that differ only in capitals. Print the list. The output must be `['Mia@Mail.com', 'leo@mail.com', 'zoe@mail.com']`.",
  "starter_code": "emails = [\"Mia@Mail.com\", \"leo@mail.com\", \"mia@mail.com\", \"zoe@mail.com\", \"LEO@MAIL.COM\"]\n",
  "solution_code": "emails = [\"Mia@Mail.com\", \"leo@mail.com\", \"mia@mail.com\", \"zoe@mail.com\", \"LEO@MAIL.COM\"]\nseen = set()\nunique = []\nfor email in emails:\n    if email.lower() not in seen:\n        seen.add(email.lower())\n        unique.append(email)\nprint(unique)",
  "check_type": "output",
  "expected_value": "['Mia@Mail.com', 'leo@mail.com', 'zoe@mail.com']",
  "hint": "Keep a set of email.lower() values you have seen; only append when the lower-case form is new."
}
```

```quiz
[
  {"question": "Which way keeps the original order?", "options": ["list(set(items))", "list(dict.fromkeys(items))", "sorted(items)"], "answer": 1, "explanation": "Dictionaries keep keys in the order they were added."},
  {"question": "Why keep the 'seen' values in a set rather than a list?", "options": ["Sets are sorted", "Checking in on a set is much faster", "Lists cannot hold strings"], "answer": 1, "explanation": "A set lookup takes about the same time however big the set is."}
]
```
