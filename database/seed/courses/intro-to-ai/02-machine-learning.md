---
title: How Machines Learn
slug: how-machines-learn
summary: Learn the ideas of training data, features, labels and models, and train a tiny model yourself.
minutes: 9
---
## Learning from examples

Machine learning starts with **data**: examples where we already know the answer.

| hours studied (feature) | passed? (label) |
|---|---|
| 1 | no |
| 2 | no |
| 4 | yes |
| 6 | yes |

- **Features** are the inputs (hours studied).
- The **label** is the answer we want to predict (passed or not).
- **Training** finds a rule that maps features to labels.
- The result is a **model**, which then predicts labels for new examples.

## A model you can see

The simplest possible learner tries every threshold and keeps the one that makes the fewest mistakes:

```python tryit
hours = [1, 2, 3, 4, 5, 6, 7]
passed = [False, False, False, True, True, True, True]

def train(xs, ys):
    best, fewest = None, len(xs) + 1
    for threshold in xs:
        mistakes = sum((x >= threshold) != y for x, y in zip(xs, ys))
        if mistakes < fewest:
            best, fewest = threshold, mistakes
    return best

threshold = train(hours, passed)
print("Learned rule: pass if hours >=", threshold)

for new in [2.5, 4.5, 8]:
    print(new, "hours ->", "pass" if new >= threshold else "fail")
```

Nobody wrote "4 hours" into the program: it was **learned** from the data. Real models learn millions of numbers instead of one, but the idea is the same.

## Kinds of machine learning

- **Supervised learning**: examples have labels (spam/not spam, house price). Most business ML is this.
- **Unsupervised learning**: no labels; find structure, such as groups of similar customers.
- **Reinforcement learning**: learn by trial and reward, as in game-playing AI and robot control.

## Testing a model honestly

A model can memorise its training examples and still fail on new ones (**overfitting**). So we keep some labelled data aside, the **test set**, and measure the model only on data it never saw.

## Data quality matters most

"Garbage in, garbage out." A model learns whatever patterns the data holds, including mistakes and unfair biases. Collecting good, representative data is often the hardest part of an AI project.

## Summary

- Features go in, labels come out; training produces a model.
- Supervised, unsupervised and reinforcement learning solve different problems.
- Always test on data the model has not seen.

```exercise
{
  "title": "Count the mistakes",
  "prompt_md": "Complete `mistakes` so it counts how many examples the rule `x >= threshold` gets wrong. With threshold `3` the program must print exactly `1`",
  "starter_code": "hours = [1, 2, 3, 4, 5]\npassed = [False, False, False, True, True]\n\ndef mistakes(threshold):\n    pass\n\nprint(mistakes(3))",
  "solution_code": "hours = [1, 2, 3, 4, 5]\npassed = [False, False, False, True, True]\n\ndef mistakes(threshold):\n    return sum((x >= threshold) != y for x, y in zip(hours, passed))\n\nprint(mistakes(3))",
  "check_type": "output",
  "expected_value": "1",
  "hint": "sum((x >= threshold) != y for x, y in zip(hours, passed))"
}
```

```quiz
[
  {"question": "In supervised learning, what is the label?", "options": ["The answer we want to predict", "The input data", "The name of the model"], "answer": 0, "explanation": "Features go in; the label is the target."},
  {"question": "Why keep a test set aside?", "options": ["To measure the model on data it never saw", "To train faster", "To store backups"], "answer": 0, "explanation": "Testing on training data hides overfitting."}
]
```
