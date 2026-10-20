---
title: The Machine Learning Workflow
slug: workflow
summary: Learn the fit / predict pattern of scikit-learn and the steps of every ML project.
minutes: 7
---
## Steps of an ML project

1. **Define the question**: what do we predict, and how will we use it?
2. **Get and explore data**.
3. **Prepare features**: clean, encode, scale.
4. **Split** into training and test data.
5. **Train** a model on the training data.
6. **Evaluate** on the test data.
7. **Improve** and repeat, then deploy and monitor.

## scikit-learn's pattern

Every scikit-learn model works the same way, which makes models easy to swap:

```python
model = SomeModel(settings)
model.fit(X_train, y_train)        # learn from examples
predictions = model.predict(X_new) # use what was learned
```

- `X` is a table of **features** (one row per example).
- `y` is the **target**: the labels or values to predict.

## Your first model

The first run downloads scikit-learn into your browser, which takes a few seconds.

```python tryit
from sklearn.neighbors import KNeighborsClassifier

# features: [weight in grams, smoothness 0-10]; labels: fruit
X = [[150, 8], [170, 9], [140, 7], [130, 2], [120, 3], [110, 1]]
y = ["apple", "apple", "apple", "orange", "orange", "orange"]

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

print(model.predict([[160, 8], [115, 2]]))
```

**k-nearest neighbours** predicts the label most common among the k most similar training examples. Simple, and often surprisingly good.

## A real dataset

scikit-learn includes small practice datasets. The famous **iris** dataset has measurements of 150 flowers of three species:

```python tryit
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame
print(df.head())
print(df.shape)
print(iris.target_names)
```

## Summary

- ML projects: question → data → features → split → train → evaluate → improve.
- scikit-learn models all use `fit()` and `predict()`.
- `X` holds features, `y` holds the target.

```exercise
{
  "title": "Predict a fruit",
  "prompt_md": "Train the `KNeighborsClassifier` with `fit(X, y)` and print the prediction for `[[145, 8]]`. The output must be exactly `['apple']`",
  "starter_code": "from sklearn.neighbors import KNeighborsClassifier\n\nX = [[150, 8], [170, 9], [140, 7], [130, 2], [120, 3], [110, 1]]\ny = [\"apple\", \"apple\", \"apple\", \"orange\", \"orange\", \"orange\"]\nmodel = KNeighborsClassifier(n_neighbors=3)\n",
  "solution_code": "from sklearn.neighbors import KNeighborsClassifier\n\nX = [[150, 8], [170, 9], [140, 7], [130, 2], [120, 3], [110, 1]]\ny = [\"apple\", \"apple\", \"apple\", \"orange\", \"orange\", \"orange\"]\nmodel = KNeighborsClassifier(n_neighbors=3)\nmodel.fit(X, y)\nprint(model.predict([[145, 8]]).tolist())",
  "check_type": "output",
  "expected_value": "['apple']",
  "hint": "model.fit(X, y), then print(model.predict([[145, 8]]).tolist())"
}
```

```quiz
[
  {"question": "Which method trains a scikit-learn model?", "options": ["fit()", "predict()", "train_model()"], "answer": 0, "explanation": "fit learns from X and y; predict uses the result."},
  {"question": "In scikit-learn, what is y?", "options": ["The target to predict", "The features", "The model's settings"], "answer": 0, "explanation": "X = features, y = target."}
]
```
