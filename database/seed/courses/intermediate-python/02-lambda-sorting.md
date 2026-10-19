---
title: Lambda, Sorting and Built-in Helpers
slug: lambda-sorting
summary: Sort by any rule with key functions and use lambda, map, filter, zip and any.
minutes: 8
---
## Small functions with lambda

A `lambda` is a tiny function without a name, written in one expression.

```python tryit
double = lambda x: x * 2
print(double(21))
```

You rarely store lambdas in variables. They shine when another function needs a short rule, especially for sorting.

## Sorting by a key

`sorted()` and `list.sort()` take a `key`: a function that says what to sort by.

```python tryit
words = ["banana", "kiwi", "apple", "fig"]
print(sorted(words))               # alphabetical
print(sorted(words, key=len))      # by length

students = [("Mia", 88), ("Leo", 95), ("Ava", 79)]
by_score = sorted(students, key=lambda s: s[1], reverse=True)
print(by_score)
```

## Sorting dictionaries

```python tryit
stock = {"pens": 40, "books": 12, "bags": 25}
for item, count in sorted(stock.items(), key=lambda pair: pair[1]):
    print(item, count)
print(max(stock, key=stock.get))   # the key with the largest value
```

## zip, map, filter, any and all

```python tryit
names = ["Ana", "Ben", "Cy"]
ages = [31, 25, 40]
for name, age in zip(names, ages):     # walk two lists together
    print(name, age)

print(list(map(str.upper, names)))
print(list(filter(lambda a: a > 30, ages)))
print(any(a > 35 for a in ages), all(a > 18 for a in ages))
```

`map()` and `filter()` work, but a comprehension is often clearer: `[n.upper() for n in names]`.

## Summary

- `lambda args: expression` makes a small function.
- `key=` tells `sorted()`, `min()` and `max()` what to compare.
- `zip()` pairs items; `any()` and `all()` test many conditions at once.

```exercise
{
  "title": "Sort by last letter",
  "prompt_md": "Sort the list by the **last letter** of each word using `sorted()` with a `key`. The output must be exactly `['banana', 'kiwi', 'melon', 'cherry']`",
  "starter_code": "fruits = [\"kiwi\", \"melon\", \"banana\", \"cherry\"]\n",
  "solution_code": "fruits = [\"kiwi\", \"melon\", \"banana\", \"cherry\"]\nprint(sorted(fruits, key=lambda f: f[-1]))",
  "check_type": "output",
  "expected_value": "['banana', 'kiwi', 'melon', 'cherry']",
  "hint": "key=lambda f: f[-1]"
}
```

```quiz
[
  {"question": "What does sorted([\"bb\", \"a\", \"ccc\"], key=len) return?", "options": ["[\"a\", \"bb\", \"ccc\"]", "[\"ccc\", \"bb\", \"a\"]", "[\"bb\", \"a\", \"ccc\"]"], "answer": 0, "explanation": "key=len sorts by length, shortest first."},
  {"question": "What does zip([1, 2], [\"a\", \"b\"]) pair up?", "options": ["(1, 2) and (\"a\", \"b\")", "(1, \"a\") and (2, \"b\")", "Nothing"], "answer": 1, "explanation": "zip takes one item from each list at a time."}
]
```
