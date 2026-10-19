---
title: Clustering
slug: clustering
summary: Find groups in unlabelled data with k-means and choose the number of clusters.
minutes: 8
---
## Learning without labels

In **unsupervised learning** there are no answers to learn from. **Clustering** finds groups of similar items: customer segments, similar documents, unusual transactions.

## k-means

k-means places `k` centres, assigns each point to the nearest centre, moves each centre to the middle of its points, and repeats until nothing changes.

```python tryit
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=300, centers=3, cluster_std=1.0, random_state=7)

kmeans = KMeans(n_clusters=3, n_init=10, random_state=0)
labels = kmeans.fit_predict(X)

plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis", s=15)
plt.scatter(*kmeans.cluster_centers_.T, c="red", marker="x", s=120)
plt.title("k-means found 3 groups")
plt.show()
```

## Choosing k

You must pick `k`. The **elbow method** plots the within-cluster spread (inertia) for several `k`; the bend in the curve is a good choice. The **silhouette score** (−1 to 1, higher is better) is another guide.

```python tryit
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

X, _ = make_blobs(n_samples=300, centers=4, random_state=3)
for k in range(2, 7):
    labels = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)
    print(k, "clusters -> silhouette", round(silhouette_score(X, labels), 3))
```

## Customer segments

```python tryit
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

customers = pd.DataFrame({
    "visits_per_month": [2, 3, 25, 30, 1, 28, 4, 22],
    "avg_spend": [80, 95, 15, 12, 120, 18, 70, 20],
})
model = make_pipeline(StandardScaler(), KMeans(n_clusters=2, n_init=10, random_state=0))
customers["segment"] = model.fit_predict(customers)
print(customers.groupby("segment").mean().round(1))
```

Two clear segments appear: frequent small spenders and rare big spenders. Naming and using the groups is the analyst's job.

## Summary

- Clustering groups unlabelled data.
- k-means needs `k`; use the elbow method or silhouette score.
- Scale features before clustering.

```exercise
{
  "title": "How many clusters?",
  "prompt_md": "Fit `KMeans(n_clusters=2, n_init=10, random_state=0)` on the points and print the **number of different labels** it found. The output must be exactly `2`",
  "starter_code": "from sklearn.cluster import KMeans\n\npoints = [[1, 1], [1.5, 2], [1, 1.5], [8, 8], [8.5, 9], [9, 8]]\n",
  "solution_code": "from sklearn.cluster import KMeans\n\npoints = [[1, 1], [1.5, 2], [1, 1.5], [8, 8], [8.5, 9], [9, 8]]\nlabels = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(points)\nprint(len(set(labels)))",
  "check_type": "output",
  "expected_value": "2",
  "hint": "labels = KMeans(...).fit_predict(points); print(len(set(labels)))"
}
```

```quiz
{
  "title": "Final quiz: Machine Learning with scikit-learn",
  "final": true,
  "questions": [
    {"question": "Which two methods does every scikit-learn model have?", "options": ["fit and predict", "load and save", "train and run"], "answer": 0, "explanation": "fit learns; predict applies."},
    {"question": "Predicting a price is...", "options": ["Regression", "Classification", "Clustering"], "answer": 0, "explanation": "Regression predicts numbers."},
    {"question": "Why split data into training and test sets?", "options": ["To measure performance on unseen data", "To train twice as fast", "Because scikit-learn requires two files"], "answer": 0, "explanation": "Testing on training data hides overfitting."},
    {"question": "A model that misses many real positives has low...", "options": ["Recall", "Precision", "Speed"], "answer": 0, "explanation": "Recall = found positives / all real positives."},
    {"question": "What problem does a Pipeline help avoid?", "options": ["Data leakage from the test set", "Slow downloads", "Missing labels"], "answer": 0, "explanation": "Preparation is fitted on training data only."},
    {"question": "k-means is an example of...", "options": ["Unsupervised learning", "Supervised learning", "Reinforcement learning"], "answer": 0, "explanation": "It finds groups without labels."}
  ]
}
```
