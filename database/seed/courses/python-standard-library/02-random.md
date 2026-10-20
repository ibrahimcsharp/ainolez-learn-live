---
title: Python Random Numbers
slug: random
summary: Roll dice, pick and shuffle items, and make random results repeatable with a seed.
minutes: 7
---
## Random whole numbers

The `random` module makes pseudo-random numbers: they look random, but come from a formula.

```python tryit
import random

print(random.randint(1, 6))      # a dice roll: 1 to 6, both included
print(random.randrange(0, 100, 10))  # 0, 10, ..., 90
print(random.random())           # a float from 0.0 up to 1.0
print(random.uniform(1.5, 2.5))  # a float in a range
```

Run it a few times: the numbers change.

## Picking from a list

```python tryit
import random

prizes = ["pen", "mug", "t-shirt", "sticker"]
print(random.choice(prizes))            # one item
print(random.sample(prizes, 2))         # two different items
print(random.choices(prizes, k=5))      # five picks, repeats allowed
```

## Shuffling

`shuffle()` mixes a list **in place**: it changes the list and returns `None`.

```python tryit
import random

cards = list(range(1, 11))
random.shuffle(cards)
print(cards)
```

## Repeatable results with seed()

Give the generator a starting point with `seed()` and it produces the same sequence every time. That makes tests and demos repeatable.

```python tryit
import random

random.seed(42)
print([random.randint(1, 6) for _ in range(5)])
random.seed(42)
print([random.randint(1, 6) for _ in range(5)])   # the same list again
```

## A simulation

Random numbers let you estimate things by trying many times.

```python tryit
import random

rolls = 10_000
sixes = sum(1 for _ in range(rolls) if random.randint(1, 6) == 6)
print(f"Sixes: {sixes / rolls:.1%} (expected about 16.7%)")
```

!!! warning
    `random` is fine for games and simulations but not for passwords or security tokens. Use the `secrets` module for those: `secrets.token_hex(16)`.

## Summary

- `randint(a, b)` includes both ends; `random()` gives a float below 1.
- `choice`, `sample` and `shuffle` work with lists.
- `seed(n)` makes the results repeatable; `secrets` is for security.

```exercise
{
  "title": "Fair dice?",
  "prompt_md": "Roll a dice 600 times with `random.randint(1, 6)` and count how often each face comes up in a dictionary. Then print the number of different faces you saw - it must be `6`.",
  "starter_code": "import random\n\ncounts = {}\n",
  "solution_code": "import random\n\ncounts = {}\nfor _ in range(600):\n    face = random.randint(1, 6)\n    counts[face] = counts.get(face, 0) + 1\nprint(len(counts))",
  "check_type": "output",
  "expected_value": "6",
  "hint": "counts[face] = counts.get(face, 0) + 1 adds one to the right face."
}
```

```quiz
[
  {"question": "Which values can random.randint(1, 3) return?", "options": ["1 and 2", "1, 2 and 3", "0, 1, 2 and 3"], "answer": 1, "explanation": "randint includes both ends."},
  {"question": "What does random.shuffle(cards) return?", "options": ["the shuffled list", "None", "a new list"], "answer": 1, "explanation": "shuffle changes the list in place and returns None."},
  {"question": "Which module should create a password reset token?", "options": ["random", "secrets", "math"], "answer": 1, "explanation": "secrets uses a secure source of randomness."}
]
```
