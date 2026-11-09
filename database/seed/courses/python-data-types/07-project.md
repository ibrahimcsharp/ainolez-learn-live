---
title: "Project: A Contact Book"
slug: project
summary: Clean messy contact text with string methods, store it in dictionaries, group it with sets and print a tidy list.
minutes: 12
---
## The plan

A sign-up form saved its contacts as one block of text. Names have odd capitals, phone numbers have spaces and dashes, and some people signed up twice. We will turn it into a clean contact book. Each step uses one lesson of this course.

## Step 1: split the text into fields

```python tryit
raw = """  ana TORRES ; 0612-345-678 ; Madrid
Ben okafor;0701 222 333;Lagos
  ana torres ; 0612 345 678 ; madrid
chloe DUBOIS ; 06-55-44-33-22 ; Lyon"""

for line in raw.splitlines():
    fields = [part.strip() for part in line.split(";")]
    print(fields)
```

`splitlines()` gives one string per line, `split(";")` cuts each line into fields, and `strip()` removes the spaces around them.

## Step 2: clean each field

Names get `title()`, cities too, and phone numbers keep only their digits.

```python tryit
def clean_phone(text):
    return "".join(ch for ch in text if ch.isdigit())

def clean_line(line):
    name, phone, city = [part.strip() for part in line.split(";")]
    return name.title(), clean_phone(phone), city.title()

print(clean_line("  ana TORRES ; 0612-345-678 ; Madrid"))
print(clean_line("chloe DUBOIS ; 06-55-44-33-22 ; Lyon"))
```

`clean_line` returns a tuple, so the caller can unpack it.

## Step 3: a dictionary of contacts

Using the name as the key removes the double sign-up for free: the second one just overwrites the first.

```python tryit
def clean_phone(text):
    return "".join(ch for ch in text if ch.isdigit())

def clean_line(line):
    name, phone, city = [part.strip() for part in line.split(";")]
    return name.title(), clean_phone(phone), city.title()

raw = """  ana TORRES ; 0612-345-678 ; Madrid
Ben okafor;0701 222 333;Lagos
  ana torres ; 0612 345 678 ; madrid
chloe DUBOIS ; 06-55-44-33-22 ; Lyon"""

contacts = {}
for line in raw.splitlines():
    name, phone, city = clean_line(line)
    contacts[name] = {"phone": phone, "city": city}

print(len(contacts), "contacts")
print(contacts["Ana Torres"])
```

## Step 4: questions with sets and sorting

```python tryit
contacts = {
    "Ana Torres": {"phone": "0612345678", "city": "Madrid"},
    "Ben Okafor": {"phone": "0701222333", "city": "Lagos"},
    "Chloe Dubois": {"phone": "0655443322", "city": "Lyon"},
}

cities = {info["city"] for info in contacts.values()}
print("cities:", sorted(cities))

surnames = sorted(contacts, key=lambda name: name.split()[-1])
print("by surname:", surnames)

for name in surnames:
    phone = contacts[name]["phone"]
    pretty = " ".join(phone[i:i + 2] for i in range(0, len(phone), 2))
    print(f"{name:<14}{pretty}")
```

The last loop uses **slices** to put a space after every two digits.

## Ideas to try next

- Add an `email` field and check that it contains exactly one `@`.
- Print how many contacts live in each city with a dictionary and `get()`.
- Let a contact have several phone numbers in a list.

```exercise
{
  "title": "Clean a contact line",
  "prompt_md": "Write `clean_line(line)` that takes text like `\" dara SMITH ; 07-11 22 ; Cork\"` and returns a tuple `(name, phone, city)` with the name and city in title case and only the digits of the phone. Then print the result for `sample`. The output must be `('Dara Smith', '071122', 'Cork')`.",
  "starter_code": "def clean_line(line):\n    # your code here\n    pass\n\nsample = \" dara SMITH ; 07-11 22 ; cork\"\nprint(clean_line(sample))",
  "solution_code": "def clean_line(line):\n    name, phone, city = [part.strip() for part in line.split(\";\")]\n    digits = \"\".join(ch for ch in phone if ch.isdigit())\n    return name.title(), digits, city.title()\n\nsample = \" dara SMITH ; 07-11 22 ; cork\"\nprint(clean_line(sample))",
  "check_type": "output",
  "expected_value": "('Dara Smith', '071122', 'Cork')",
  "hint": "Split on \";\", strip each part, keep characters where ch.isdigit() is True, and return the three values."
}
```

```exercise
{
  "title": "Contacts per city",
  "prompt_md": "Count the contacts in each city and print the cities in A to Z order with their count, one per line:\n\n```\nLagos 1\nLyon 2\nMadrid 1\n```",
  "starter_code": "contacts = {\n    \"Ana Torres\": {\"city\": \"Madrid\"},\n    \"Ben Okafor\": {\"city\": \"Lagos\"},\n    \"Chloe Dubois\": {\"city\": \"Lyon\"},\n    \"Remi Blanc\": {\"city\": \"Lyon\"},\n}\n",
  "solution_code": "contacts = {\n    \"Ana Torres\": {\"city\": \"Madrid\"},\n    \"Ben Okafor\": {\"city\": \"Lagos\"},\n    \"Chloe Dubois\": {\"city\": \"Lyon\"},\n    \"Remi Blanc\": {\"city\": \"Lyon\"},\n}\nper_city = {}\nfor info in contacts.values():\n    per_city[info[\"city\"]] = per_city.get(info[\"city\"], 0) + 1\nfor city in sorted(per_city):\n    print(city, per_city[city])",
  "check_type": "output",
  "expected_value": "Lagos 1\nLyon 2\nMadrid 1",
  "hint": "Use a dictionary with get(city, 0) + 1, then loop over sorted(per_city)."
}
```
