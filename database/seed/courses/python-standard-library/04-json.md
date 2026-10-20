---
title: Python JSON
slug: json
summary: Read and write JSON, the text format web APIs use, with json.loads and json.dumps.
minutes: 8
---
## What is JSON?

JSON (JavaScript Object Notation) is a text format for data. Web APIs, settings files and many apps use it. It looks very much like Python dictionaries and lists:

```json
{"name": "Ana", "age": 29, "skills": ["python", "sql"], "admin": false}
```

## JSON text to Python: loads()

`json.loads()` (*load string*) turns JSON text into Python values.

```python tryit
import json

text = '{"name": "Ana", "age": 29, "skills": ["python", "sql"], "admin": false}'
user = json.loads(text)
print(type(user))
print(user["name"], user["skills"][0], user["admin"])
```

| JSON | Python |
|---|---|
| object `{}` | dict |
| array `[]` | list |
| string | str |
| number | int / float |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

## Python to JSON text: dumps()

`json.dumps()` (*dump string*) does the opposite.

```python tryit
import json

order = {"id": 17, "items": ["tea", "cake"], "paid": True, "note": None}
print(json.dumps(order))
print(json.dumps(order, indent=2))          # pretty
print(json.dumps(order, sort_keys=True))    # keys in order
```

Notice how `True` became `true` and `None` became `null`.

## Files: load() and dump()

Without the *s*, the functions read from and write to files.

```python tryit
import json

settings = {"theme": "dark", "font_size": 14}
with open("settings.json", "w") as file:
    json.dump(settings, file, indent=2)

with open("settings.json") as file:
    loaded = json.load(file)
print(loaded["theme"], loaded["font_size"] + 2)
```

## Bad JSON

JSON is stricter than Python: keys need double quotes, and there are no trailing commas. Invalid text raises `json.JSONDecodeError`.

```python tryit
import json

try:
    json.loads("{'name': 'Ana'}")     # single quotes are not JSON
except json.JSONDecodeError as error:
    print("Invalid JSON:", error.msg)
```

## Summary

- `json.loads(text)` -> Python; `json.dumps(value)` -> text.
- `json.load(file)` and `json.dump(value, file)` work with files.
- `indent=2` makes JSON easy to read.

```exercise
{
  "title": "Total from an API",
  "prompt_md": "`response` is JSON text from a shop API. Load it and print the sum of the `price` of every item. The output must be `27.5`.",
  "starter_code": "import json\n\nresponse = '{\"items\": [{\"name\": \"cap\", \"price\": 12.5}, {\"name\": \"socks\", \"price\": 4.0}, {\"name\": \"scarf\", \"price\": 11.0}]}'\n",
  "solution_code": "import json\n\nresponse = '{\"items\": [{\"name\": \"cap\", \"price\": 12.5}, {\"name\": \"socks\", \"price\": 4.0}, {\"name\": \"scarf\", \"price\": 11.0}]}'\ndata = json.loads(response)\nprint(sum(item[\"price\"] for item in data[\"items\"]))",
  "check_type": "output",
  "expected_value": "27.5",
  "hint": "data = json.loads(response); the list is data[\"items\"]."
}
```

```quiz
[
  {"question": "Which function turns JSON text into a dict?", "options": ["json.dumps()", "json.loads()", "json.dict()"], "answer": 1, "explanation": "loads = load from a string."},
  {"question": "What does Python None become in JSON?", "options": ["None", "null", "\"\""], "answer": 1, "explanation": "JSON writes it as null."},
  {"question": "Is {'a': 1} valid JSON?", "options": ["Yes", "No, keys need double quotes"], "answer": 1, "explanation": "JSON strings always use double quotes."}
]
```
