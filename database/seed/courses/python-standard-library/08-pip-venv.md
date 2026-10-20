---
title: Python pip and Virtual Environments
slug: pip-venv
summary: Install packages from PyPI with pip, keep each project separate with venv, and record requirements.
minutes: 9
---
## Packages beyond the standard library

The standard library is big, but most projects also use packages written by others: `requests` for the web, `pandas` for data, `django` for websites. They live on **PyPI**, the Python Package Index, and you install them with **pip**.

!!! note
    The commands in this lesson run in a terminal on your own computer (Command Prompt, PowerShell, or Terminal on macOS and Linux), not in the browser editor. In the browser editor, popular packages such as numpy and pandas load automatically when you import them.

## Step 1: make a virtual environment

A **virtual environment** is a private folder of packages for one project. Project A can use Django 4 while project B uses Django 5, without fights.

```bash
# inside your project folder
python -m venv .venv
```

This creates a `.venv` folder with its own Python and pip.

## Step 2: activate it

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. Anything you install goes into this project only. Type `deactivate` to leave.

## Step 3: install packages

```bash
pip install requests          # the latest version
pip install "django>=5.2,<6"  # a version range
pip list                      # what is installed
pip show requests             # details about one package
pip install --upgrade requests
pip uninstall requests
```

Then use it like any module:

```python
import requests

reply = requests.get("https://api.github.com")
print(reply.status_code)
```

## Step 4: record your requirements

Save the list of packages so others (or your server) can install the same ones.

```bash
pip freeze > requirements.txt     # write the list
pip install -r requirements.txt   # install everything on the list
```

A `requirements.txt` looks like this:

```text
Django==5.2.7
requests==2.32.5
```

## Good habits

- One virtual environment per project; never install project packages globally.
- Do not commit the `.venv` folder to Git - commit `requirements.txt` instead.
- Install only packages you trust: check their PyPI page, downloads and source code. Typos in names (`reqeusts`) can install fake packages.

## Check what is available

You can see which modules are already importable from Python itself:

```python tryit
import sys

print(sys.version)
print("json" in sys.stdlib_module_names)
print("requests" in sys.stdlib_module_names)   # False: it comes from PyPI
```

## Summary

- `python -m venv .venv` creates a virtual environment; activate it before installing.
- `pip install name`, `pip list`, `pip uninstall name`.
- `pip freeze > requirements.txt` and `pip install -r requirements.txt` share your setup.

```exercise
{
  "title": "Standard or not?",
  "prompt_md": "Loop over the module names and print each one with `standard` or `install with pip`, using `sys.stdlib_module_names`. The output must be:\n\n```\njson standard\nrequests install with pip\nre standard\npandas install with pip\n```",
  "starter_code": "import sys\n\nmodules = [\"json\", \"requests\", \"re\", \"pandas\"]\n",
  "solution_code": "import sys\n\nmodules = [\"json\", \"requests\", \"re\", \"pandas\"]\nfor name in modules:\n    if name in sys.stdlib_module_names:\n        print(name, \"standard\")\n    else:\n        print(name, \"install with pip\")",
  "check_type": "output",
  "expected_value": "json standard\nrequests install with pip\nre standard\npandas install with pip",
  "hint": "Use if name in sys.stdlib_module_names: inside the loop."
}
```

```quiz
{
  "title": "Final quiz: Python Standard Library",
  "final": true,
  "questions": [
    {"question": "Which module gives you sqrt and pi?", "options": ["math", "random", "numbers"], "answer": 0, "explanation": "math holds the maths functions and constants."},
    {"question": "What makes random results repeatable?", "options": ["random.repeat()", "random.seed(n)", "random.fixed()"], "answer": 1, "explanation": "The same seed gives the same sequence."},
    {"question": "What does date(2026, 3, 1) - date(2026, 2, 1) give?", "options": ["a timedelta of 28 days", "1", "an error"], "answer": 0, "explanation": "Subtracting dates gives a timedelta; February 2026 has 28 days."},
    {"question": "Which function turns a dict into JSON text?", "options": ["json.loads", "json.dumps", "json.read"], "answer": 1, "explanation": "dumps = dump to a string."},
    {"question": "What does re.findall(r\"\\d\", \"a1b22\") return?", "options": ["['1', '22']", "['1', '2', '2']", "3"], "answer": 1, "explanation": "\\d matches one digit at a time."},
    {"question": "Which mode adds to the end of a file?", "options": ["\"w\"", "\"a\"", "\"x\""], "answer": 1, "explanation": "\"a\" appends."},
    {"question": "Which class counts items for you?", "options": ["Counter", "deque", "namedtuple"], "answer": 0, "explanation": "Counter counts how often each item appears."},
    {"question": "Which command creates a virtual environment?", "options": ["pip install venv", "python -m venv .venv", "pip freeze"], "answer": 1, "explanation": "The venv module creates it."}
  ]
}
```
