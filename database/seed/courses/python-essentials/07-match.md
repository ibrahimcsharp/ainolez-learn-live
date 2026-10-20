---
title: Python match
slug: match
summary: Choose between many cases with match and case, including patterns and guards.
minutes: 9
---
## Many choices

When one value can be many things, a long chain of `if / elif` gets hard to read. `match` (Python 3.10+) compares a value against several **cases**.

```python tryit
day = 6

match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 6 | 7:
        print("Weekend!")
    case _:
        print("Another weekday")
```

- `case 6 | 7` matches either value (`|` means *or*).
- `case _` matches anything: it is the default, like `else`.
- Only the first matching case runs.

## Matching text

```python tryit
command = "stop"

match command:
    case "start":
        print("Starting the engine")
    case "stop" | "halt":
        print("Stopping")
    case _:
        print(f"Unknown command: {command}")
```

## Guards: extra conditions

Add `if` after a case to check a condition. The case only matches when the condition is true.

```python tryit
temperature = 34

match temperature:
    case t if t < 0:
        print("Freezing")
    case t if t < 25:
        print("Mild")
    case _:
        print("Hot")
```

`case t` stores the value in `t`, so the guard can use it.

## Matching shapes

`match` can look inside lists and tuples and pull out their parts.

```python tryit
points = [(0, 0), (3, 0), (0, 5), (2, 4)]

for point in points:
    match point:
        case (0, 0):
            print("origin")
        case (x, 0):
            print(f"on the x-axis at {x}")
        case (0, y):
            print(f"on the y-axis at {y}")
        case (x, y):
            print(f"at {x}, {y}")
```

## Summary

- `match value:` followed by `case pattern:` lines picks one branch.
- `|` joins alternatives; `_` is the default case.
- `case x if condition:` adds a guard; `case (x, y):` unpacks a tuple.

```exercise
{
  "title": "Traffic light",
  "prompt_md": "Use `match` on each colour in the list. Print `Go` for green, `Slow down` for yellow, `Stop` for red and `Broken light` for anything else. The output must be:\n\n```\nGo\nStop\nSlow down\nBroken light\n```",
  "starter_code": "for colour in [\"green\", \"red\", \"yellow\", \"blue\"]:\n    pass  # replace with match\n",
  "solution_code": "for colour in [\"green\", \"red\", \"yellow\", \"blue\"]:\n    match colour:\n        case \"green\":\n            print(\"Go\")\n        case \"yellow\":\n            print(\"Slow down\")\n        case \"red\":\n            print(\"Stop\")\n        case _:\n            print(\"Broken light\")",
  "check_type": "output",
  "expected_value": "Go\nStop\nSlow down\nBroken light",
  "hint": "Write match colour: inside the loop and one case per colour, then case _: for the rest."
}
```

```quiz
[
  {"question": "Which case works like else?", "options": ["case else:", "case _:", "case *:"], "answer": 1, "explanation": "_ matches any value."},
  {"question": "How do you match 1 or 2 in one case?", "options": ["case 1 or 2:", "case 1 | 2:", "case [1, 2]:"], "answer": 1, "explanation": "| joins alternative patterns."},
  {"question": "How many cases run when several could match?", "options": ["All of them", "Only the first", "Only the last"], "answer": 1, "explanation": "match stops at the first case that matches."}
]
```
