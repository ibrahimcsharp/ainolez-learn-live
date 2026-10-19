---
title: Python While Loops
slug: while-loops
summary: Repeat code as long as a condition stays true, and avoid endless loops.
minutes: 6
---
## The while loop

A `while` loop repeats while its condition is `True`. Use it when you do not know in advance how many rounds you need.

```python tryit
count = 1
while count <= 5:
    print("Round", count)
    count = count + 1
print("Finished")
```

## Watch out for endless loops

If the condition never becomes `False`, the loop never stops. In the example above, forgetting `count = count + 1` would loop forever.

!!! warning
    If your code seems frozen, it is probably stuck in an endless loop. Reload the page and check that something inside the loop changes the condition.

## A real use: saving money

How many months until savings reach 1000, if you save 150 each month and get 1% interest?

```python tryit
savings = 0
months = 0
while savings < 1000:
    savings = savings * 1.01 + 150
    months += 1
print(months, "months, savings:", round(savings, 2))
```

`months += 1` is short for `months = months + 1`. The same works with `-=`, `*=` and `/=`.

## while True with break

Sometimes it is clearer to loop "forever" and `break` when you are done:

```python tryit
number = 100
while True:
    number = number // 2
    print(number)
    if number < 5:
        break
```

## Summary

- `while condition:` repeats while the condition is true.
- Something in the loop must change the condition, or it never ends.
- `+=` adds to a variable; `break` leaves the loop.

```exercise
{
  "title": "Countdown",
  "prompt_md": "Use a `while` loop to count down from `5` to `1`, then print `Go!`. The output must be:\n\n```\n5\n4\n3\n2\n1\nGo!\n```",
  "starter_code": "n = 5\n",
  "solution_code": "n = 5\nwhile n > 0:\n    print(n)\n    n -= 1\nprint(\"Go!\")",
  "check_type": "output",
  "expected_value": "5\n4\n3\n2\n1\nGo!",
  "hint": "Loop while n > 0, print n, then lower it with n -= 1."
}
```

```quiz
[
  {"question": "When does a while loop stop?", "options": ["After 10 rounds", "When its condition is False", "Never"], "answer": 1, "explanation": "The condition is checked before every round."},
  {"question": "What does x += 2 mean?", "options": ["x = 2", "x = x + 2", "x == x + 2"], "answer": 1, "explanation": "+= adds to the current value."}
]
```
