---
title: Python Dictionaries
slug: dictionaries
summary: Store data as key-value pairs and read, change and loop over dictionaries.
minutes: 9
---
## Keys and values

A dictionary (`dict`) stores pairs: a **key** and its **value**. You look values up by key, like words in a real dictionary.

```python tryit
student = {
    "name": "Kofi",
    "age": 19,
    "courses": ["Python", "SQL"],
}
print(student["name"])
print(student["courses"][0])
print(len(student))
```

## Adding and changing

```python tryit
student = {"name": "Kofi", "age": 19}
student["age"] = 20          # change
student["city"] = "Accra"    # add
del student["name"]          # remove
print(student)
```

## Safe lookups

Reading a key that does not exist raises a `KeyError`. Use `get()` to give a default instead.

```python tryit
prices = {"tea": 2.5, "coffee": 3.0}
print(prices.get("tea"))
print(prices.get("juice", "not on the menu"))
print("coffee" in prices)
```

## Looping over a dictionary

```python tryit
prices = {"tea": 2.5, "coffee": 3.0, "cake": 4.25}
for item, price in prices.items():
    print(f"{item}: ${price}")
print(list(prices.keys()))
```

## Counting with a dictionary

A very common pattern: count how often each value appears.

```python tryit
words = ["red", "blue", "red", "green", "red"]
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)
```

## Summary

- A dictionary maps keys to values: `{"key": value}`.
- `d[key]` reads or sets a value; `get()` gives a default.
- `items()` gives the pairs for a loop.

```exercise
{
  "title": "Stock check",
  "prompt_md": "The shop sold 2 apples. Lower the apple count by 2, then print the dictionary. The output must be exactly `{'apples': 3, 'pears': 4}`",
  "starter_code": "stock = {\"apples\": 5, \"pears\": 4}\n",
  "solution_code": "stock = {\"apples\": 5, \"pears\": 4}\nstock[\"apples\"] = stock[\"apples\"] - 2\nprint(stock)",
  "check_type": "output",
  "expected_value": "{'apples': 3, 'pears': 4}",
  "hint": "stock[\"apples\"] reads the count; assign a new value to the same key."
}
```

```quiz
[
  {"question": "How do you read the value of key \"age\" from d?", "options": ["d.age", "d[\"age\"]", "d(age)"], "answer": 1, "explanation": "Square brackets with the key read the value."},
  {"question": "What does d.get(\"x\", 0) return if \"x\" is missing?", "options": ["0", "an error", "None always"], "answer": 0, "explanation": "get() returns the default you give when the key is missing."},
  {"question": "What does d.items() give?", "options": ["Only keys", "Only values", "Key-value pairs"], "answer": 2, "explanation": "items() yields (key, value) pairs."}
]
```
