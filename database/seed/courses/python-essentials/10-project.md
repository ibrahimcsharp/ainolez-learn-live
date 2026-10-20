---
title: "Project: A Shop Receipt"
slug: project
summary: Combine casting, operators, match, range and formatting to print a neat receipt.
minutes: 12
---
## The plan

A small shop sends its orders as text, one item per line: `name,quantity,price`. We will turn that text into a tidy receipt with a discount code. Every step uses something from this course.

## Step 1: read the lines

```python tryit
order = """Pencil,3,0.80
Notebook,2,2.50
Backpack,1,24.99"""

for line in order.splitlines():
    name, qty, price = line.split(",")
    print(name, int(qty), float(price))
```

`split(",")` gives three strings; casting turns two of them into numbers.

## Step 2: line totals in columns

```python tryit
order = """Pencil,3,0.80
Notebook,2,2.50
Backpack,1,24.99"""

subtotal = 0
for line in order.splitlines():
    name, qty, price = line.split(",")
    line_total = int(qty) * float(price)
    subtotal += line_total
    print(f"{name:<10}{qty:>3} x {float(price):>6.2f} = {line_total:>7.2f}")
print(f"{'Subtotal':<24}{subtotal:>7.2f}")
```

## Step 3: a discount with match

```python tryit
def discount_rate(code):
    match code.strip().upper():
        case "SCHOOL":
            return 0.10
        case "VIP" | "STAFF":
            return 0.20
        case _:
            return 0.0

for code in ["school", "Staff ", "free"]:
    print(code, discount_rate(code))
```

## Step 4: the whole receipt

```python tryit
order = """Pencil,3,0.80
Notebook,2,2.50
Backpack,1,24.99"""
code = "school"

def discount_rate(code):
    match code.strip().upper():
        case "SCHOOL":
            return 0.10
        case "VIP" | "STAFF":
            return 0.20
        case _:
            return 0.0

print(f"{'AINOLEZ SHOP':^31}")
print("-" * 31)
subtotal = 0
for line in order.splitlines():
    name, qty, price = line.split(",")
    line_total = int(qty) * float(price)
    subtotal += line_total
    print(f"{name:<10}{qty:>3} x {float(price):>6.2f} = {line_total:>7.2f}")
rate = discount_rate(code)
discount = subtotal * rate
print("-" * 31)
print(f"{'Subtotal':<24}{subtotal:>7.2f}")
print(f"{f'Discount {rate:.0%}':<24}{-discount:>7.2f}")
print(f"{'TOTAL':<24}{subtotal - discount:>7.2f}")
```

## Ideas to try

- Add a 5% tax line.
- Number the lines with `enumerate()`.
- Skip lines whose quantity is not a number, using `isdigit()`.

```exercise
{
  "title": "Order total",
  "prompt_md": "Read every line of `order`, add up quantity x price and print the total with 2 decimals: `Total: 32.39`.",
  "starter_code": "order = \"\"\"Pencil,3,0.80\nNotebook,2,2.50\nBackpack,1,24.99\"\"\"\n",
  "solution_code": "order = \"\"\"Pencil,3,0.80\nNotebook,2,2.50\nBackpack,1,24.99\"\"\"\ntotal = 0\nfor line in order.splitlines():\n    name, qty, price = line.split(\",\")\n    total += int(qty) * float(price)\nprint(f\"Total: {total:.2f}\")",
  "check_type": "output",
  "expected_value": "Total: 32.39",
  "hint": "Loop over order.splitlines(), split each line on commas, cast quantity and price, and add."
}
```

```quiz
{
  "title": "Final quiz: Python Essentials",
  "final": true,
  "questions": [
    {"question": "What does a colon at the end of a line mean?", "options": ["The line is a comment", "An indented block follows", "The program ends"], "answer": 1, "explanation": "if, for, def and others are followed by an indented block."},
    {"question": "What is int(\"8\") + 2?", "options": ["10", "\"82\"", "an error"], "answer": 0, "explanation": "int() turns the text into the number 8."},
    {"question": "How do you test that x has no value?", "options": ["x == 0", "x is None", "not x"], "answer": 1, "explanation": "is None checks for exactly None."},
    {"question": "What is 23 % 10?", "options": ["2", "3", "2.3"], "answer": 1, "explanation": "% gives the remainder: 23 = 2 * 10 + 3."},
    {"question": "What does f\"{3.14159:.1f}\" show?", "options": ["3.1", "3.14", "3"], "answer": 0, "explanation": ".1f shows one decimal."},
    {"question": "What type does input() return?", "options": ["int", "str", "float"], "answer": 1, "explanation": "input() always returns text."},
    {"question": "Which case catches everything else in match?", "options": ["case _:", "case else:", "default:"], "answer": 0, "explanation": "_ matches any value."},
    {"question": "What is list(range(1, 4))?", "options": ["[1, 2, 3, 4]", "[1, 2, 3]", "[0, 1, 2, 3]"], "answer": 1, "explanation": "range stops before 4."},
    {"question": "What does next() raise when an iterator is empty?", "options": ["StopIteration", "ValueError", "None"], "answer": 0, "explanation": "StopIteration ends a for loop."}
  ]
}
```
