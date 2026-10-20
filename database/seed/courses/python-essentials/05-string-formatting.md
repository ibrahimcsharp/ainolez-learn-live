---
title: Python String Formatting
slug: string-formatting
summary: Control decimals, width, alignment and thousands separators in f-strings.
minutes: 9
---
## f-strings recap

An f-string puts values inside text with `{ }`. Anything that gives a value can go inside: variables, sums, function calls.

```python tryit
item = "notebook"
price = 2.5
count = 4
print(f"{count} x {item} = {price * count}")
print(f"{item.upper()} has {len(item)} letters")
```

## Format specifiers

After the value, add a colon and a **format specifier** to control how it looks.

```python tryit
pi = 3.14159265
print(f"{pi:.2f}")      # 2 decimals: 3.14
print(f"{pi:.0f}")      # no decimals: 3
print(f"{1234567:,}")   # thousands: 1,234,567
print(f"{0.256:.1%}")   # percent: 25.6%
```

## Width and alignment

A number before the type sets the width. `<` aligns left, `>` right, `^` centre. This makes neat tables.

```python tryit
rows = [("Apples", 3, 0.5), ("Bread", 1, 2.25), ("Cheese", 2, 4.1)]
for name, qty, price in rows:
    print(f"{name:<8}{qty:>3}{price:>8.2f}")
print(f"{'END':^19}")
print(f"{'END':*^19}")   # fill with *
```

## Padding numbers

```python tryit
for n in [7, 42, 315]:
    print(f"#{n:04d}")   # pad with zeros to 4 digits
```

## Debugging with =

Put `=` after a name to print both the name and its value. It is a quick way to check variables.

```python tryit
width = 12
height = 5
print(f"{width=} {height=} {width * height=}")
```

## format() and %

Older code uses `str.format()` or `%`. You will see them, but f-strings are easier to read.

```python tryit
print("{} scored {:.1f}".format("Ana", 87.456))
print("%s scored %.1f" % ("Ana", 87.456))
```

## Summary

- `{value:.2f}` shows 2 decimals, `{value:,}` adds thousands separators.
- `{text:<10}`, `{text:>10}`, `{text:^10}` align in a column of 10.
- `{name=}` prints the name and value - handy for debugging.

```exercise
{
  "title": "Price label",
  "prompt_md": "Print the price with a thousands separator and exactly 2 decimals, so the output is `Total: $12,499.50`.",
  "starter_code": "total = 12499.5\n",
  "solution_code": "total = 12499.5\nprint(f\"Total: ${total:,.2f}\")",
  "check_type": "output",
  "expected_value": "Total: $12,499.50",
  "hint": "Combine both: {total:,.2f}"
}
```

```quiz
[
  {"question": "What does f\"{2/3:.2f}\" show?", "options": ["0.67", "0.66", "0.6667"], "answer": 0, "explanation": ".2f rounds to 2 decimals."},
  {"question": "Which specifier right-aligns in 6 characters?", "options": [":<6", ":>6", ":^6"], "answer": 1, "explanation": "> aligns to the right."},
  {"question": "What does f\"{5:03d}\" show?", "options": ["005", "5.000", "  5"], "answer": 0, "explanation": "03d pads with zeros to 3 digits."}
]
```
