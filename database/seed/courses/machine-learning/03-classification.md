---
title: Classification
slug: classification
summary: Predict categories with logistic regression and decision trees, and read their accuracy.
minutes: 9
---
## Predicting a category

**Classification** predicts a label: spam or not, which species, will the customer leave. Let's classify iris flowers.

```python tryit
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print("Accuracy:", round(model.score(X_test, y_test), 3))
print("First 5 predictions:", model.predict(X_test[:5]))
print("Real labels:        ", y_test[:5])
```

`stratify=y` keeps the same mix of classes in the training and test data. Despite its name, **logistic regression** is a classification model.

## Probabilities

Many classifiers also say how sure they are:

```python tryit
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

iris = load_iris()
model = LogisticRegression(max_iter=1000).fit(iris.data, iris.target)
flower = [[6.0, 2.9, 4.5, 1.5]]
for name, p in zip(iris.target_names, model.predict_proba(flower)[0]):
    print(f"{name:12} {p:.2f}")
```

## Decision trees

A **decision tree** learns a series of yes/no questions. Its rules can be read by people:

```python tryit
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text

iris = load_iris()
tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(iris.data, iris.target)
print(export_text(tree, feature_names=list(iris.feature_names)))
```

`max_depth` limits how many questions the tree may ask. A very deep tree can memorise the training data (**overfitting**).

## Summary

- Classification predicts categories.
- `LogisticRegression` and `DecisionTreeClassifier` share `fit`, `predict` and `score`.
- `predict_proba` gives the model's confidence.

```exercise
{
  "title": "A tree's accuracy",
  "prompt_md": "Train a `DecisionTreeClassifier(max_depth=3, random_state=0)` on the training data and print its accuracy on the **test** data rounded to 2 decimals. The output must be exactly `0.93`",
  "starter_code": "from sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier\n\nX, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n",
  "solution_code": "from sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier\n\nX, y = load_iris(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\ntree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_train, y_train)\nprint(round(tree.score(X_test, y_test), 2))",
  "check_type": "output",
  "expected_value": "0.93",
  "hint": "tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_train, y_train); round(tree.score(X_test, y_test), 2)"
}
```

```quiz
[
  {"question": "Logistic regression is used for...", "options": ["Classification", "Predicting prices", "Clustering"], "answer": 0, "explanation": "It predicts the probability of each class."},
  {"question": "What can a very deep decision tree do?", "options": ["Overfit by memorising the training data", "Never make mistakes", "Run faster than a shallow tree"], "answer": 0, "explanation": "Limit depth to keep it general."}
]
```
