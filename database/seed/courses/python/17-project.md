---
title: "Project: Class Report"
slug: project
summary: Combine lists, dictionaries, loops, functions and f-strings in a small report program.
minutes: 12
---
## The task

A teacher has the test scores of a class. You will write a program that:

1. works out each student's average,
2. gives a grade,
3. prints a neat report and the best student.

Everything you need, you have already learned.

## Step 1: the data

A dictionary maps each name to a list of scores.

```python
scores = {
    "Amara": [88, 92, 79],
    "Ben": [65, 70, 58],
    "Chen": [95, 98, 100],
    "Dana": [72, 81, 77],
}
```

## Step 2: helper functions

```python
def average(numbers):
    return sum(numbers) / len(numbers)

def grade(value):
    if value >= 90:
        return "A"
    elif value >= 75:
        return "B"
    elif value >= 60:
        return "C"
    return "D"
```

## Step 3: the report

Run the whole program, then try changing scores or adding a student.

```python tryit
scores = {
    "Amara": [88, 92, 79],
    "Ben": [65, 70, 58],
    "Chen": [95, 98, 100],
    "Dana": [72, 81, 77],
}

def average(numbers):
    return sum(numbers) / len(numbers)

def grade(value):
    if value >= 90:
        return "A"
    elif value >= 75:
        return "B"
    elif value >= 60:
        return "C"
    return "D"

print("Name    Avg   Grade")
best_name, best_avg = "", 0
for name, marks in scores.items():
    avg = average(marks)
    print(f"{name:<7} {avg:5.1f}  {grade(avg)}")
    if avg > best_avg:
        best_name, best_avg = name, avg

print(f"Best student: {best_name} ({best_avg:.1f})")
```

`{name:<7}` pads the name to 7 characters; `{avg:5.1f}` shows the number with one decimal in 5 characters. This keeps the columns lined up.

## Ideas to go further

- Count how many students got each grade with a dictionary.
- Write the report to a file with `open("report.txt", "w")`.
- Ask the AI tutor how to sort the report by average.

Congratulations: you can now write real Python programs. Next, try **Intermediate Python** or **Python for Data Analysis**.

```exercise
{
  "title": "Class average",
  "prompt_md": "Print the average of **all** scores of the class (every number in every list), rounded to 1 decimal. The output must be exactly `81.2`.",
  "starter_code": "scores = {\n    \"Amara\": [88, 92, 79],\n    \"Ben\": [65, 70, 58],\n    \"Chen\": [95, 98, 100],\n    \"Dana\": [72, 81, 77],\n}\n",
  "solution_code": "scores = {\n    \"Amara\": [88, 92, 79],\n    \"Ben\": [65, 70, 58],\n    \"Chen\": [95, 98, 100],\n    \"Dana\": [72, 81, 77],\n}\nall_marks = []\nfor marks in scores.values():\n    all_marks += marks\nprint(round(sum(all_marks) / len(all_marks), 1))",
  "check_type": "output",
  "expected_value": "81.2",
  "hint": "Collect every score in one list (loop over scores.values()), then divide the sum by the count."
}
```

```quiz
{
  "title": "Final quiz: Python for Absolute Beginners",
  "final": true,
  "questions": [
    {"question": "What does len([4, 5, 6]) return?", "options": ["3", "6", "15"], "answer": 0, "explanation": "len() counts the items."},
    {"question": "Which line stores 10 in x?", "options": ["x == 10", "x = 10", "10 = x"], "answer": 1, "explanation": "A single = stores a value."},
    {"question": "What does \"code\"[1:3] give?", "options": ["co", "od", "ode"], "answer": 1, "explanation": "The slice runs from index 1 up to, not including, 3."},
    {"question": "Which collection maps keys to values?", "options": ["list", "tuple", "dictionary"], "answer": 2, "explanation": "Dictionaries store key-value pairs."},
    {"question": "How many times does for i in range(4): run?", "options": ["3", "4", "5"], "answer": 1, "explanation": "range(4) gives 0, 1, 2, 3."},
    {"question": "What does a function return when it has no return line?", "options": ["0", "an empty string", "None"], "answer": 2, "explanation": "Python returns None by default."},
    {"question": "Which keyword catches an error?", "options": ["catch", "except", "error"], "answer": 1, "explanation": "Python uses try / except."},
    {"question": "What is 17 % 5?", "options": ["2", "3", "3.4"], "answer": 0, "explanation": "17 = 3 * 5 + 2, so the remainder is 2."}
  ]
}
```
