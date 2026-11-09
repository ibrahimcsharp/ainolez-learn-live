---
title: How to Convert Units - Temperature, Distance and Time
slug: unit-conversion
summary: Convert Celsius and Fahrenheit, kilometres and miles, and seconds into hours and minutes, with neat rounding and a reusable conversion table.
minutes: 8
---
## Temperature

The formulas are `F = C × 9/5 + 32` and `C = (F − 32) × 5/9`. Write each as a small function.

```python tryit
def c_to_f(celsius):
    return celsius * 9 / 5 + 32

def f_to_c(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

print(c_to_f(100))            # water boils
print(f_to_c(98.6))           # body temperature
print(f_to_c(70))             # a long float
print(round(f_to_c(70), 1))   # rounded for people
```

Keep full precision while calculating and round only when you **show** the result.

## A conversion table

A loop with a format specifier prints a tidy table.

```python tryit
def c_to_f(celsius):
    return celsius * 9 / 5 + 32

print("   C      F")
for c in range(-10, 41, 10):
    print(f"{c:>4} {c_to_f(c):>6.1f}")
```

`>4` right-aligns in 4 characters; `.1f` shows one decimal.

## Distance and weight with a dictionary

When there are many units, store the factors in a dictionary instead of writing a function for each one. Convert everything to one base unit (here metres), then to the target.

```python tryit
TO_METRES = {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000, "in": 0.0254, "ft": 0.3048, "mi": 1609.344}

def convert(value, source, target):
    metres = value * TO_METRES[source]
    return metres / TO_METRES[target]

print(round(convert(10, "km", "mi"), 2))
print(round(convert(6, "ft", "cm"), 1))
print(round(convert(1, "mi", "ft")))
```

Adding a new unit is one new entry in the dictionary, not a new function.

## Seconds into hours, minutes and seconds

`divmod(a, b)` gives the whole part and the remainder in one step.

```python tryit
def split_time(total_seconds):
    hours, rest = divmod(total_seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    return hours, minutes, seconds

h, m, s = split_time(9_754)
print(f"{h}h {m}m {s}s")
print(f"{h:02}:{m:02}:{s:02}")   # clock style with leading zeros
```

The standard library can do the same with `datetime.timedelta`:

```python tryit
from datetime import timedelta
print(timedelta(seconds=9_754))
```

```exercise
{
  "title": "Weather report in Fahrenheit",
  "prompt_md": "Convert each Celsius temperature to Fahrenheit and print it with one decimal, like `22.5 C = 72.5 F`. The output must be:\n\n```\n22.5 C = 72.5 F\n-4.0 C = 24.8 F\n31.0 C = 87.8 F\n```",
  "starter_code": "temps = [22.5, -4.0, 31.0]\n",
  "solution_code": "temps = [22.5, -4.0, 31.0]\nfor c in temps:\n    f = c * 9 / 5 + 32\n    print(f\"{c:.1f} C = {f:.1f} F\")",
  "check_type": "output",
  "expected_value": "22.5 C = 72.5 F\n-4.0 C = 24.8 F\n31.0 C = 87.8 F",
  "hint": "f = c * 9 / 5 + 32, then print with f\"{c:.1f} C = {f:.1f} F\"."
}
```

```exercise
{
  "title": "Film length",
  "prompt_md": "A film lasts `minutes` minutes. Use `divmod` to print it as hours and minutes: `2 h 49 min`.",
  "starter_code": "minutes = 169\n",
  "solution_code": "minutes = 169\nhours, rest = divmod(minutes, 60)\nprint(hours, \"h\", rest, \"min\")",
  "check_type": "output",
  "expected_value": "2 h 49 min",
  "hint": "hours, rest = divmod(minutes, 60)"
}
```

```quiz
[
  {"question": "What does divmod(125, 60) return?", "options": ["(2, 5)", "2.08", "(5, 2)"], "answer": 0, "explanation": "125 // 60 is 2 and 125 % 60 is 5."},
  {"question": "When should you round a converted value?", "options": ["After every step", "Only when showing it", "Never"], "answer": 1, "explanation": "Rounding early adds small errors; round for display."}
]
```
