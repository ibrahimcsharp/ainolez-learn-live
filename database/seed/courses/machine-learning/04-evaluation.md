---
title: Evaluating Models
slug: evaluation
summary: Go beyond accuracy with the confusion matrix, precision, recall and cross-validation.
minutes: 9
---
## When accuracy lies

Imagine 100 patients, 5 of them ill. A model that always says "healthy" is **95% accurate** and completely useless. With unbalanced classes, look deeper.

## The confusion matrix

| | predicted no | predicted yes |
|---|---|---|
| **really no** | true negative | false positive |
| **really yes** | false negative | true positive |

```python tryit
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

model = LogisticRegression(max_iter=5000).fit(X_train, y_train)
predicted = model.predict(X_test)

print(confusion_matrix(y_test, predicted))
print(classification_report(y_test, predicted, target_names=["malignant", "benign"]))
```

## Precision and recall

- **Precision**: of everything predicted "yes", how much was right? (Few false alarms.)
- **Recall**: of all the real "yes" cases, how many did we find? (Few misses.)
- **F1**: one number that balances both.

Which matters more depends on the cost of mistakes. Missing a disease (low recall) is worse than an extra test (low precision). For a spam filter, losing a real email (low precision) is worse than letting one spam through.

## Cross-validation

One train/test split can be lucky or unlucky. **Cross-validation** splits the data into k parts, trains k times and tests on each part once:

```python tryit
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

X, y = load_iris(return_X_y=True)
scores = cross_val_score(KNeighborsClassifier(n_neighbors=5), X, y, cv=5)
print("Scores per fold:", scores.round(2))
print("Mean:", round(scores.mean(), 3), "+/-", round(scores.std(), 3))
```

## Summary

- Accuracy can mislead when classes are unbalanced.
- The confusion matrix, precision and recall show the kinds of mistakes.
- Cross-validation gives a more reliable score.

```exercise
{
  "title": "Precision by hand",
  "prompt_md": "A model flagged 8 emails as spam; 6 really were spam. Compute precision = true positives / everything predicted positive, and print it. The output must be exactly `0.75`",
  "starter_code": "true_positives = 6\nfalse_positives = 2\n",
  "solution_code": "true_positives = 6\nfalse_positives = 2\nprecision = true_positives / (true_positives + false_positives)\nprint(precision)",
  "check_type": "output",
  "expected_value": "0.75",
  "hint": "precision = true_positives / (true_positives + false_positives)"
}
```

```quiz
[
  {"question": "Recall answers which question?", "options": ["Of the real positives, how many did we find?", "Of our positive predictions, how many were right?", "How fast is the model?"], "answer": 0, "explanation": "Recall measures misses; precision measures false alarms."},
  {"question": "Why use cross-validation?", "options": ["A single split can be lucky or unlucky", "It trains the model faster", "It removes the need for test data"], "answer": 0, "explanation": "Averaging over several splits is more reliable."}
]
```
