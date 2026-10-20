---
title: Hash Tables
slug: hash-tables
summary: How dictionaries and sets find any key in one step - hash functions, buckets and collisions.
minutes: 10
---
## Finding things in one step

Searching a list checks item after item: O(n). A **hash table** finds a key in about one step, O(1). Python's `dict` and `set` are hash tables.

The trick: a **hash function** turns a key into a number, and that number says which slot (bucket) to look in.

```python tryit
for key in ["apple", "pear", 42, (1, 2)]:
    print(repr(key), hash(key) % 8)    # which of 8 buckets
```

The same key always gives the same hash (within one run of Python), so Python knows exactly where to look.

## A tiny hash table

Let's build one to see how it works. Each bucket holds a small list of `(key, value)` pairs.

```python tryit
class HashTable:
    def __init__(self, size=8):
        self.buckets = [[] for _ in range(size)]

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)    # update
                return
        bucket.append((key, value))         # new key

    def get(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        raise KeyError(key)

prices = HashTable()
prices.put("tea", 2.5)
prices.put("cake", 3.0)
prices.put("tea", 2.8)
print(prices.get("tea"), prices.get("cake"))
```

## Collisions

Two different keys can land in the same bucket. That is a **collision**. Our table handles it by keeping a short list per bucket (*chaining*). As long as the buckets stay short, lookups are still about one step. Real hash tables grow and spread the keys out when they get full.

```python tryit
buckets = {}
for word in ["red", "green", "blue", "cyan", "pink", "gold", "grey", "teal", "navy", "lime"]:
    buckets.setdefault(hash(word) % 4, []).append(word)
for number in sorted(buckets):
    print(number, buckets[number])
```

## Keys must be hashable

A key must not change, or it would end up in the wrong bucket. That is why strings, numbers and tuples can be keys, but lists cannot.

```python tryit
location = {(51.5, -0.12): "London"}   # tuple key: fine
print(location[(51.5, -0.12)])
try:
    bad = {[1, 2]: "list"}
except TypeError as error:
    print("Error:", error)
```

## Using hash tables to solve problems

Many problems become fast with a dict or set. *Two sum*: find two numbers that add up to a target.

```python tryit
def two_sum(numbers, target):
    seen = {}                        # value -> index
    for i, n in enumerate(numbers):
        if target - n in seen:       # O(1) lookup
            return seen[target - n], i
        seen[n] = i
    return None

print(two_sum([8, 3, 11, 5, 2], 13))   # (0, 3): 8 + 5
```

One pass, O(n), instead of checking every pair, O(n²).

## Summary

- A hash function turns a key into a bucket number; lookups are O(1) on average.
- Collisions are handled by keeping several pairs per bucket.
- Keys must be unchangeable (hashable): str, int, tuple - not list.

```exercise
{
  "title": "First repeated letter",
  "prompt_md": "Use a set to find the first letter that appears a second time in `text`, in one pass. Print it. The output must be `r`.",
  "starter_code": "text = \"programming\"\nseen = set()\n",
  "solution_code": "text = \"programming\"\nseen = set()\nfor letter in text:\n    if letter in seen:\n        print(letter)\n        break\n    seen.add(letter)",
  "check_type": "output",
  "expected_value": "r",
  "hint": "For each letter: if it is already in seen, print it and break; otherwise add it."
}
```

```quiz
[
  {"question": "What is the average Big O of a dict lookup?", "options": ["O(1)", "O(log n)", "O(n)"], "answer": 0, "explanation": "The hash tells Python where to look."},
  {"question": "What is a collision?", "options": ["Two keys in the same bucket", "A key that is too long", "A deleted key"], "answer": 0, "explanation": "Different keys can hash to the same bucket."},
  {"question": "Which can be a dict key?", "options": ["[1, 2]", "(1, 2)", "{1: 2}"], "answer": 1, "explanation": "Tuples are hashable; lists and dicts are not."}
]
```
