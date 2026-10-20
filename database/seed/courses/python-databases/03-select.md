---
title: Querying with SELECT
slug: select
summary: Read rows with WHERE, ORDER BY, LIMIT and aggregates, and get rows as dictionaries.
minutes: 10
---
## Sample data

Every example on this page starts with the same small table of movies.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE movies (title TEXT, year INTEGER, rating REAL, genre TEXT)")
db.executemany("INSERT INTO movies VALUES (?, ?, ?, ?)", [
    ("Spirited Away", 2001, 8.6, "animation"),
    ("Parasite", 2019, 8.5, "thriller"),
    ("Coco", 2017, 8.4, "animation"),
    ("Inception", 2010, 8.8, "sci-fi"),
    ("Arrival", 2016, 7.9, "sci-fi"),
])
for row in db.execute("SELECT * FROM movies"):
    print(row)
```

## Choosing columns and rows: WHERE

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE movies (title TEXT, year INTEGER, rating REAL, genre TEXT)")
db.executemany("INSERT INTO movies VALUES (?, ?, ?, ?)", [
    ("Spirited Away", 2001, 8.6, "animation"), ("Parasite", 2019, 8.5, "thriller"),
    ("Coco", 2017, 8.4, "animation"), ("Inception", 2010, 8.8, "sci-fi"),
    ("Arrival", 2016, 7.9, "sci-fi"),
])

print(db.execute("SELECT title FROM movies WHERE genre = ?", ("sci-fi",)).fetchall())
print(db.execute("SELECT title, year FROM movies WHERE year >= 2015 AND rating > 8").fetchall())
print(db.execute("SELECT title FROM movies WHERE title LIKE ?", ("%in%",)).fetchall())
print(db.execute("SELECT title FROM movies WHERE year BETWEEN 2000 AND 2012").fetchall())
```

`LIKE` matches patterns: `%` stands for any text. Values from variables always go through `?`.

## Sorting and limiting

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE movies (title TEXT, year INTEGER, rating REAL, genre TEXT)")
db.executemany("INSERT INTO movies VALUES (?, ?, ?, ?)", [
    ("Spirited Away", 2001, 8.6, "animation"), ("Parasite", 2019, 8.5, "thriller"),
    ("Coco", 2017, 8.4, "animation"), ("Inception", 2010, 8.8, "sci-fi"),
    ("Arrival", 2016, 7.9, "sci-fi"),
])

top = db.execute("SELECT title, rating FROM movies ORDER BY rating DESC LIMIT 3")
for title, rating in top:
    print(f"{rating}  {title}")
print(db.execute("SELECT title FROM movies ORDER BY year").fetchone())   # the oldest
```

`fetchone()` returns only the first row (or `None` if there is none).

## Counting and grouping

**Aggregate** functions summarise many rows: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. `GROUP BY` makes one summary per group.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE movies (title TEXT, year INTEGER, rating REAL, genre TEXT)")
db.executemany("INSERT INTO movies VALUES (?, ?, ?, ?)", [
    ("Spirited Away", 2001, 8.6, "animation"), ("Parasite", 2019, 8.5, "thriller"),
    ("Coco", 2017, 8.4, "animation"), ("Inception", 2010, 8.8, "sci-fi"),
    ("Arrival", 2016, 7.9, "sci-fi"),
])

count, best = db.execute("SELECT COUNT(*), MAX(rating) FROM movies").fetchone()
print(count, best)
query = "SELECT genre, COUNT(*), ROUND(AVG(rating), 2) FROM movies GROUP BY genre ORDER BY genre"
for genre, n, average in db.execute(query):
    print(f"{genre:<10} {n}  {average}")
```

## Rows as dictionaries

Set `row_factory = sqlite3.Row` and you can read columns by name.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row
db.execute("CREATE TABLE movies (title TEXT, year INTEGER)")
db.execute("INSERT INTO movies VALUES ('Coco', 2017)")

row = db.execute("SELECT * FROM movies").fetchone()
print(row["title"], row["year"])
print(dict(row))
```

## Summary

- `WHERE` filters rows (`=`, `>`, `AND`, `LIKE`, `BETWEEN`); `ORDER BY` sorts; `LIMIT` cuts.
- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` summarise; `GROUP BY` summarises per group.
- `fetchone()` gets one row; `sqlite3.Row` lets you use column names.

```exercise
{
  "title": "Best animation",
  "prompt_md": "Print the title of the highest-rated **animation** movie, using `WHERE`, `ORDER BY` and `LIMIT`. The output must be `Spirited Away`.",
  "starter_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\ndb.execute(\"CREATE TABLE movies (title TEXT, year INTEGER, rating REAL, genre TEXT)\")\ndb.executemany(\"INSERT INTO movies VALUES (?, ?, ?, ?)\", [\n    (\"Spirited Away\", 2001, 8.6, \"animation\"), (\"Parasite\", 2019, 8.5, \"thriller\"),\n    (\"Coco\", 2017, 8.4, \"animation\"), (\"Inception\", 2010, 8.8, \"sci-fi\"),\n])\n",
  "solution_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\ndb.execute(\"CREATE TABLE movies (title TEXT, year INTEGER, rating REAL, genre TEXT)\")\ndb.executemany(\"INSERT INTO movies VALUES (?, ?, ?, ?)\", [\n    (\"Spirited Away\", 2001, 8.6, \"animation\"), (\"Parasite\", 2019, 8.5, \"thriller\"),\n    (\"Coco\", 2017, 8.4, \"animation\"), (\"Inception\", 2010, 8.8, \"sci-fi\"),\n])\nrow = db.execute(\"SELECT title FROM movies WHERE genre = ? ORDER BY rating DESC LIMIT 1\", (\"animation\",)).fetchone()\nprint(row[0])",
  "check_type": "output",
  "expected_value": "Spirited Away",
  "hint": "SELECT title FROM movies WHERE genre = ? ORDER BY rating DESC LIMIT 1"
}
```

```quiz
[
  {"question": "Which clause filters rows?", "options": ["ORDER BY", "WHERE", "GROUP BY"], "answer": 1, "explanation": "WHERE keeps only matching rows."},
  {"question": "What does LIMIT 3 do?", "options": ["Returns at most 3 rows", "Skips 3 rows", "Returns rows with id 3"], "answer": 0, "explanation": "LIMIT caps the number of rows."},
  {"question": "Which function gives the average?", "options": ["MEAN()", "AVG()", "AVERAGE()"], "answer": 1, "explanation": "SQL uses AVG()."}
]
```
