---
title: Regression
slug: regression
summary: Predict numbers with linear regression and measure the error with MAE and R².
minutes: 8
---
## Predicting a number

**Regression** predicts a quantity: a house price, tomorrow's temperature, delivery time. **Linear regression** fits a straight line (or a flat surface, with several features) through the data.

```python tryit
from sklearn.linear_model import LinearRegression

size_m2 = [[50], [70], [80], [100], [120], [150]]
price_k = [150, 200, 230, 280, 330, 410]

model = LinearRegression()
model.fit(size_m2, price_k)

print("price per extra m2:", round(model.coef_[0], 2), "k")
print("base price:", round(model.intercept_, 1), "k")
print("predicted price for 90 m2:", round(model.predict([[90]])[0]), "k")
```

`coef_` is the slope (how much the price rises per m²) and `intercept_` the value at zero.

## Train and test

To know how well a model works on new houses, hold some data back:

```python tryit
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

model = LinearRegression().fit(X_train, y_train)
predicted = model.predict(X_test)

print("Mean absolute error:", round(mean_absolute_error(y_test, predicted), 1))
print("R2 score:", round(r2_score(y_test, predicted), 2))
```

## Reading the metrics

- **MAE** (mean absolute error): on average, how far off the predictions are, in the target's own units.
- **R²**: how much of the variation the model explains. 1 is perfect, 0 is no better than always guessing the average.

`random_state=0` makes the random split repeatable, so you get the same numbers every run.

## Summary

- Regression predicts numbers; `LinearRegression` fits a line.
- `train_test_split` keeps test data aside.
- MAE and R² measure regression quality.

```exercise
{
  "title": "Predict a score",
  "prompt_md": "Fit a `LinearRegression` on hours studied → score, then print the predicted score for **6 hours**, rounded to a whole number. The output must be exactly `80`",
  "starter_code": "from sklearn.linear_model import LinearRegression\n\nhours = [[1], [2], [3], [4], [5]]\nscore = [30, 40, 50, 60, 70]\n",
  "solution_code": "from sklearn.linear_model import LinearRegression\n\nhours = [[1], [2], [3], [4], [5]]\nscore = [30, 40, 50, 60, 70]\nmodel = LinearRegression().fit(hours, score)\nprint(round(model.predict([[6]])[0]))",
  "check_type": "output",
  "expected_value": "80",
  "hint": "LinearRegression().fit(hours, score), then round(model.predict([[6]])[0])"
}
```

```quiz
[
  {"question": "Which problem is regression?", "options": ["Predicting a house price", "Spam or not spam", "Grouping customers without labels"], "answer": 0, "explanation": "Regression predicts a number."},
  {"question": "An R² of 1.0 means...", "options": ["Perfect predictions", "The model is useless", "One mistake"], "answer": 0, "explanation": "R² of 1 explains all the variation."}
]
```
