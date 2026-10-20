---
title: Features, Pipelines and Tuning
slug: pipelines
summary: Scale and encode features, chain steps in a Pipeline, and tune settings with grid search.
minutes: 9
---
## Preparing features

Models need numbers on comparable scales:

- **Scaling**: `StandardScaler` gives each column mean 0 and spread 1, so a feature measured in thousands does not drown one measured in fractions.
- **Encoding**: `OneHotEncoder` turns a category ("red", "blue") into 0/1 columns.

## Pipelines

A `Pipeline` chains preparation and model into one object. It prevents a classic mistake: learning the scaling from the test data (**data leakage**).

```python tryit
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, stratify=y)

plain = KNeighborsClassifier().fit(X_train, y_train)
scaled = make_pipeline(StandardScaler(), KNeighborsClassifier()).fit(X_train, y_train)

print("without scaling:", round(plain.score(X_test, y_test), 3))
print("with scaling:   ", round(scaled.score(X_test, y_test), 3))
```

k-nearest neighbours measures distances, so scaling helps it a lot.

## Mixed columns

`ColumnTransformer` applies different steps to different columns:

```python tryit
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

data = pd.DataFrame({
    "plan": ["free", "pro", "free", "team", "pro", "free", "team", "free"],
    "months": [1, 14, 3, 30, 8, 2, 22, 5],
    "left": [1, 0, 1, 0, 0, 1, 0, 1],
})
prepare = make_column_transformer(
    (OneHotEncoder(), ["plan"]),
    (StandardScaler(), ["months"]),
)
model = make_pipeline(prepare, LogisticRegression())
model.fit(data[["plan", "months"]], data["left"])

new = pd.DataFrame({"plan": ["free", "team"], "months": [2, 24]})
print(model.predict(new))
```

## Tuning hyperparameters

Settings such as `n_neighbors` are **hyperparameters**: chosen by you, not learned. `GridSearchCV` tries each combination with cross-validation:

```python tryit
from sklearn.datasets import load_wine
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_wine(return_X_y=True)
pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier())
search = GridSearchCV(pipeline, {"kneighborsclassifier__n_neighbors": [1, 3, 5, 9, 15]}, cv=5)
search.fit(X, y)
print("best:", search.best_params_, "score:", round(search.best_score_, 3))
```

## Summary

- Scale numbers, one-hot encode categories.
- Pipelines keep preparation and model together and avoid leakage.
- `GridSearchCV` tunes hyperparameters with cross-validation.

```exercise
{
  "title": "Scale a column",
  "prompt_md": "Use `StandardScaler` to scale the values and print the **mean** of the scaled column, rounded to 1 decimal. The output must be exactly `0.0`",
  "starter_code": "from sklearn.preprocessing import StandardScaler\n\nvalues = [[10], [20], [30], [40]]\n",
  "solution_code": "from sklearn.preprocessing import StandardScaler\n\nvalues = [[10], [20], [30], [40]]\nscaled = StandardScaler().fit_transform(values)\nprint(abs(round(scaled.mean(), 1)))",
  "check_type": "output",
  "expected_value": "0.0",
  "hint": "scaled = StandardScaler().fit_transform(values); print(abs(round(scaled.mean(), 1)))"
}
```

```quiz
[
  {"question": "Why use a Pipeline?", "options": ["It keeps preparation and model together and avoids data leakage", "It makes models more complex", "It replaces the test set"], "answer": 0, "explanation": "Preparation is learned only from training data."},
  {"question": "What is a hyperparameter?", "options": ["A setting you choose, such as n_neighbors", "A weight the model learns", "A feature column"], "answer": 0, "explanation": "Hyperparameters are set before training."}
]
```
