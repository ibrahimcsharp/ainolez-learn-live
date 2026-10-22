---
title: How to Check a Password's Strength
slug: password-check
summary: Check text against several rules with any(), string methods and a list of problems, then give clear feedback and a simple score.
minutes: 9
---
## The rules

A sign-up form often asks for a password that:

1. has at least 8 characters,
2. has at least one capital letter and one small letter,
3. has at least one digit,
4. has at least one symbol, such as `!` or `#`,
5. has no spaces.

Each rule is a yes-or-no check on the text.

## One check at a time with any()

`any(test for ch in text)` is `True` when at least one character passes the test.

```python tryit
password = "Sunny day7"
print(len(password) >= 8)
print(any(ch.isupper() for ch in password))
print(any(ch.islower() for ch in password))
print(any(ch.isdigit() for ch in password))
print(any(not ch.isalnum() and not ch.isspace() for ch in password))   # a symbol?
print(" " not in password)
```

## Collect the problems, not just True or False

"Invalid password" is not helpful. Return a **list of problems** so the user knows what to fix. An empty list means the password is fine.

```python tryit
def password_problems(password):
    problems = []
    if len(password) < 8:
        problems.append("use at least 8 characters")
    if not any(ch.isupper() for ch in password):
        problems.append("add a capital letter")
    if not any(ch.islower() for ch in password):
        problems.append("add a small letter")
    if not any(ch.isdigit() for ch in password):
        problems.append("add a digit")
    if not any(not ch.isalnum() and not ch.isspace() for ch in password):
        problems.append("add a symbol such as ! or #")
    if " " in password:
        problems.append("remove the spaces")
    return problems

for attempt in ["cat", "Sunny day7", "Tr1cky#Fox"]:
    problems = password_problems(attempt)
    if problems:
        print(f"{attempt!r}: " + "; ".join(problems))
    else:
        print(f"{attempt!r}: looks good")
```

## A rules table

When rules pile up, store each one as a pair of message and test function. Adding a rule is then one new line.

```python tryit
RULES = [
    ("at least 8 characters", lambda p: len(p) >= 8),
    ("a capital letter", lambda p: any(ch.isupper() for ch in p)),
    ("a digit", lambda p: any(ch.isdigit() for ch in p)),
    ("a symbol", lambda p: any(not ch.isalnum() and not ch.isspace() for ch in p)),
]

def score(password):
    passed = [message for message, test in RULES if test(password)]
    return len(passed), len(RULES)

for attempt in ["hello", "Hello2024", "Hello-2024"]:
    got, out_of = score(attempt)
    print(f"{attempt:<11}{'#' * got}{'.' * (out_of - got)} {got}/{out_of}")
```

## Common passwords

Long lists of leaked passwords exist, and attackers try them first. Checking against a set is quick.

```python tryit
COMMON = {"password", "123456", "qwerty", "letmein", "iloveyou"}
for attempt in ["Qwerty", "blue-Harbor-81"]:
    print(attempt, "is too common" if attempt.lower() in COMMON else "is not on the list")
```

On a real website, never store passwords as plain text: save only a slow, salted hash made by a library built for that, and let a password manager create long random passwords.

```exercise
{
  "title": "Explain what is missing",
  "prompt_md": "Write `password_problems(password)` that returns a list of messages for these rules, in this order: `too short` (fewer than 8 characters), `no digit`, `no capital`. Then print the result for each password. The output must be:\n\n```\n['too short', 'no digit']\n['no capital']\n[]\n```",
  "starter_code": "def password_problems(password):\n    problems = []\n    return problems\n\nfor p in [\"Kiwi\", \"mango2024\", \"Papaya77\"]:\n    print(password_problems(p))",
  "solution_code": "def password_problems(password):\n    problems = []\n    if len(password) < 8:\n        problems.append(\"too short\")\n    if not any(ch.isdigit() for ch in password):\n        problems.append(\"no digit\")\n    if not any(ch.isupper() for ch in password):\n        problems.append(\"no capital\")\n    return problems\n\nfor p in [\"Kiwi\", \"mango2024\", \"Papaya77\"]:\n    print(password_problems(p))",
  "check_type": "output",
  "expected_value": "['too short', 'no digit']\n['no capital']\n[]",
  "hint": "Three if statements, each appending a message; use any(ch.isdigit() for ch in password) and any(ch.isupper() ...)."
}
```

```quiz
[
  {"question": "What does any(ch.isdigit() for ch in \"abc\") give?", "options": ["True", "False"], "answer": 1, "explanation": "No character is a digit."},
  {"question": "Why return a list of problems instead of False?", "options": ["Lists are faster", "The user learns what to fix", "False is not allowed"], "answer": 1, "explanation": "Specific messages help the user fix the password in one go."}
]
```
