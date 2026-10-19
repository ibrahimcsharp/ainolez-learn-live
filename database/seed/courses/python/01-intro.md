---
title: Python Introduction
slug: intro
summary: Learn what Python is, what people build with it, and run your first line of code.
minutes: 5
---
## What is Python?

Python is a programming language: a way to give a computer exact instructions. It was created by Guido van Rossum and first released in 1991. Today it is one of the most used languages in the world.

People use Python to:

- build websites and web APIs
- analyse data and draw charts
- train machine learning and AI models
- automate boring tasks, like renaming hundreds of files

## Why learn Python first?

Python code is short and easy to read. Compare it with plain English:

```python
if temperature > 30:
    print("It is hot today")
```

Even if you have never programmed, you can guess what this does. That makes Python a great first language, and it stays useful when you are an expert.

## Your first program

Press **Run** below. The computer reads the line and shows the text in the output box.

```python tryit
print("Hello, World!")
```

Now change the text between the quotes, for example to your name, and run it again. You just edited and ran a Python program.

!!! tip
    You do not need to install anything for this course. Every example runs in your browser.

## Summary

- Python is a popular, readable programming language.
- It is used for the web, data, AI and automation.
- `print()` shows text on the screen.

```exercise
{
  "title": "Say hello",
  "prompt_md": "Change the program so it prints exactly `Hello, Python!`",
  "starter_code": "print(\"Hello, World!\")",
  "solution_code": "print(\"Hello, Python!\")",
  "check_type": "output",
  "expected_value": "Hello, Python!",
  "hint": "Keep print( ) and the quotes. Only change the words inside the quotes."
}
```

```quiz
[
  {"question": "What does print() do?", "options": ["Sends the code to a printer", "Shows a value on the screen", "Saves a file"], "answer": 1, "explanation": "print() writes text (or any value) to the output."},
  {"question": "Which of these is a common use of Python?", "options": ["Data analysis and AI", "Only games for old phones", "Only styling web pages"], "answer": 0, "explanation": "Python is especially popular for data, AI, automation and web back ends."}
]
```
