---
title: Python Operators
slug: operators
summary: Arithmetic, assignment, comparison, logical, identity and membership operators.
minutes: 10
---
## Arithmetic

```python tryit
a, b = 17, 5
print(a + b)   # 22  add
print(a - b)   # 12  subtract
print(a * b)   # 85  multiply
print(a / b)   # 3.4 divide (always a float)
print(a // b)  # 3   floor division (whole part)
print(a % b)   # 2   remainder (modulo)
print(a ** 2)  # 289 power
```

`%` is great for "every n-th" checks: `n % 2 == 0` means `n` is even.

## Order of operations

`**` first, then `* / // %`, then `+ -`. Use brackets when in doubt.

```python tryit
print(2 + 3 * 4)     # 14
print((2 + 3) * 4)   # 20
print(-2 ** 2)       # -4: the power happens before the minus
```

## Assignment shortcuts

`x += 1` means `x = x + 1`. There is one for every arithmetic operator.

```python tryit
points = 10
points += 5    # 15
points *= 2    # 30
points -= 4    # 26
points //= 3   # 8
print(points)
```

## Comparison

Comparisons give `True` or `False`. They can be chained.

```python tryit
age = 16
print(age == 16, age != 16)
print(age > 18, age <= 16)
print(13 <= age < 20)   # teenager?
print("apple" < "banana")  # alphabetical
```

## Logical: and, or, not

```python tryit
has_ticket = True
age = 15
print(has_ticket and age >= 18)   # both must be True
print(has_ticket or age >= 18)    # one is enough
print(not has_ticket)
```

## Identity: is

`is` checks whether two names point to the **same object**; `==` checks whether the **values are equal**.

```python tryit
a = [1, 2]
b = [1, 2]
c = a
print(a == b, a is b)   # True False: equal, but two lists
print(a is c)           # True: the same list
```

## Membership: in

```python tryit
print("py" in "python")
print(3 in [1, 2, 3])
print("z" not in "python")
print("name" in {"name": "Sam"})  # checks keys
```

## Summary

- `/` always gives a float; `//` the whole part; `%` the remainder.
- `+=`, `-=` and friends update a variable.
- `and`, `or`, `not` combine conditions; `in` checks membership; `is` checks identity.

```exercise
{
  "title": "Minutes and seconds",
  "prompt_md": "Use `//` and `%` to split `seconds` into minutes and the seconds left over. Print them as `7 min 25 s`.",
  "starter_code": "seconds = 445\n",
  "solution_code": "seconds = 445\nprint(seconds // 60, \"min\", seconds % 60, \"s\")",
  "check_type": "output",
  "expected_value": "7 min 25 s",
  "hint": "seconds // 60 gives the minutes, seconds % 60 the rest."
}
```

```quiz
[
  {"question": "What is 7 // 2?", "options": ["3.5", "3", "4"], "answer": 1, "explanation": "// keeps only the whole part."},
  {"question": "What does x *= 3 do?", "options": ["x = x * 3", "x = 3", "checks if x is 3"], "answer": 0, "explanation": "It multiplies x by 3 and stores the result."},
  {"question": "a = [1]; b = [1]. What is a is b?", "options": ["True", "False"], "answer": 1, "explanation": "They are equal but are two different list objects."},
  {"question": "What does not (5 > 3) give?", "options": ["True", "False"], "answer": 1, "explanation": "5 > 3 is True, and not flips it."}
]
```
