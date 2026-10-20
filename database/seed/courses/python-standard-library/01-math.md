---
title: Python Math
slug: math
summary: Built-in number functions and the math module - rounding, roots, powers, pi and more.
minutes: 8
---
## Built-in helpers

Some maths functions need no import at all.

```python tryit
values = [4, -9, 15, 2.5]
print(min(values), max(values))
print(sum(values))
print(abs(-9))          # distance from zero
print(round(2.567, 2))  # 2.57
print(pow(2, 10))       # same as 2 ** 10
print(divmod(17, 5))    # (3, 2): whole part and remainder
```

!!! note
    `round()` rounds halves to the nearest **even** number: `round(2.5)` is `2` and `round(3.5)` is `4`. This avoids a bias when you round many numbers.

## The math module

For more, import the `math` module.

```python tryit
import math

print(math.sqrt(81))      # square root: 9.0
print(math.pi)            # 3.14159...
print(math.ceil(4.1))     # round up: 5
print(math.floor(4.9))    # round down: 4
print(math.factorial(5))  # 5*4*3*2*1 = 120
print(math.gcd(24, 36))   # greatest common divisor: 12
```

## Geometry

```python tryit
import math

radius = 3
area = math.pi * radius ** 2
print(f"Circle area: {area:.2f}")

# distance between two points
print(math.dist((0, 0), (3, 4)))   # 5.0
print(math.hypot(3, 4))            # also 5.0
```

## Angles

The trigonometry functions use **radians**. Convert degrees with `math.radians()`.

```python tryit
import math

angle = math.radians(30)
print(round(math.sin(angle), 3))   # 0.5
print(math.degrees(math.pi))       # 180.0
```

## Comparing floats

Decimal numbers are stored approximately, so `0.1 + 0.2` is not exactly `0.3`. Use `math.isclose()`.

```python tryit
import math

print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
```

## Summary

- `min`, `max`, `sum`, `abs`, `round` and `pow` are built in.
- `import math` for `sqrt`, `pi`, `ceil`, `floor`, `factorial`, `gcd`, `dist`.
- Compare floats with `math.isclose()`.

```exercise
{
  "title": "Pizza slices",
  "prompt_md": "A pizza has a radius of 15 cm and is cut into 8 slices. Print the area of one slice, rounded **up** to a whole number with `math.ceil()`. The output must be `89`.",
  "starter_code": "import math\n\nradius = 15\nslices = 8\n",
  "solution_code": "import math\n\nradius = 15\nslices = 8\nprint(math.ceil(math.pi * radius ** 2 / slices))",
  "check_type": "output",
  "expected_value": "89",
  "hint": "Area of the pizza is math.pi * radius ** 2. Divide by slices, then math.ceil()."
}
```

```quiz
[
  {"question": "What does math.floor(7.8) give?", "options": ["8", "7", "7.8"], "answer": 1, "explanation": "floor rounds down."},
  {"question": "Which needs import math?", "options": ["abs()", "round()", "sqrt()"], "answer": 2, "explanation": "sqrt lives in the math module."},
  {"question": "What does round(2.5) give?", "options": ["2", "3", "2.5"], "answer": 0, "explanation": "Python rounds halves to the nearest even number."}
]
```
