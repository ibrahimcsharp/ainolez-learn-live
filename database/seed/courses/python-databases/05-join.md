---
title: Joining Tables
slug: join
summary: Link tables with foreign keys and combine them with INNER JOIN and LEFT JOIN.
minutes: 10
---
## Why several tables?

Storing a customer's name and address on every order repeats it many times - and when they move, you would have to change every order. Instead, keep customers in one table and orders in another, and **link** them with an id.

```text
customers                orders
id | name                id | customer_id | total
 1 | Ana        <---      1 |      1      | 30.0
 2 | Ben        <---      2 |      1      | 12.5
 3 | Cy         <---      3 |      2      | 48.0
```

`orders.customer_id` is a **foreign key**: it points to a row in `customers`.

## Creating related tables

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")      # SQLite checks foreign keys only when asked
db.executescript("""
    CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL REFERENCES customers(id),
        total REAL
    );
    INSERT INTO customers (name) VALUES ('Ana'), ('Ben'), ('Cy');
    INSERT INTO orders (customer_id, total) VALUES (1, 30.0), (1, 12.5), (2, 48.0);
""")
try:
    db.execute("INSERT INTO orders (customer_id, total) VALUES (99, 5.0)")
except sqlite3.IntegrityError as error:
    print("Refused:", error)
```

`executescript()` runs several statements separated by `;` in one go. The foreign key stops orders for customers that do not exist.

## INNER JOIN

`JOIN ... ON` combines rows from two tables where the condition is true. An **inner join** keeps only rows that have a match on both sides.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
    CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL);
    INSERT INTO customers (name) VALUES ('Ana'), ('Ben'), ('Cy');
    INSERT INTO orders (customer_id, total) VALUES (1, 30.0), (1, 12.5), (2, 48.0);
""")
query = """
    SELECT customers.name, orders.total
    FROM orders
    JOIN customers ON customers.id = orders.customer_id
    ORDER BY orders.id
"""
for name, total in db.execute(query):
    print(name, total)
```

Cy has no orders, so Cy does not appear.

## LEFT JOIN

A **left join** keeps every row of the left table, even without a match. Missing values become `NULL` (`None` in Python).

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
    CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL);
    INSERT INTO customers (name) VALUES ('Ana'), ('Ben'), ('Cy');
    INSERT INTO orders (customer_id, total) VALUES (1, 30.0), (1, 12.5), (2, 48.0);
""")
query = """
    SELECT c.name, COUNT(o.id) AS orders, COALESCE(SUM(o.total), 0) AS spent
    FROM customers AS c
    LEFT JOIN orders AS o ON o.customer_id = c.id
    GROUP BY c.id
    ORDER BY spent DESC
"""
for name, orders, spent in db.execute(query):
    print(f"{name:<4} {orders} orders  {spent:6.2f}")
```

- `AS c` gives a table a short alias.
- `COALESCE(x, 0)` uses 0 when `x` is `NULL`.

## Summary

- Split data into tables and link them with foreign keys.
- `JOIN ... ON` (inner) keeps only matching rows.
- `LEFT JOIN` keeps every row of the first table; missing values are `NULL`.

```exercise
{
  "title": "Who wrote what?",
  "prompt_md": "Join `books` with `authors` and print each book title with its author's name, ordered by title, one per line as `title - author`. The output must be:\n\n```\nBeloved - Toni Morrison\nEmma - Jane Austen\nPersuasion - Jane Austen\n```",
  "starter_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\ndb.executescript(\"\"\"\n    CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT);\n    CREATE TABLE books (title TEXT, author_id INTEGER);\n    INSERT INTO authors (name) VALUES ('Jane Austen'), ('Toni Morrison');\n    INSERT INTO books VALUES ('Emma', 1), ('Beloved', 2), ('Persuasion', 1);\n\"\"\")\n",
  "solution_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\ndb.executescript(\"\"\"\n    CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT);\n    CREATE TABLE books (title TEXT, author_id INTEGER);\n    INSERT INTO authors (name) VALUES ('Jane Austen'), ('Toni Morrison');\n    INSERT INTO books VALUES ('Emma', 1), ('Beloved', 2), ('Persuasion', 1);\n\"\"\")\nquery = \"SELECT books.title, authors.name FROM books JOIN authors ON authors.id = books.author_id ORDER BY books.title\"\nfor title, name in db.execute(query):\n    print(f\"{title} - {name}\")",
  "check_type": "output",
  "expected_value": "Beloved - Toni Morrison\nEmma - Jane Austen\nPersuasion - Jane Austen",
  "hint": "SELECT books.title, authors.name FROM books JOIN authors ON authors.id = books.author_id ORDER BY books.title"
}
```

```quiz
[
  {"question": "What is a foreign key?", "options": ["A column that points to a row in another table", "An encrypted column", "The first column of a table"], "answer": 0, "explanation": "It links related tables."},
  {"question": "Which join keeps customers who have no orders?", "options": ["INNER JOIN", "LEFT JOIN (customers on the left)"], "answer": 1, "explanation": "A left join keeps every row of the left table."},
  {"question": "What does a missing value from a LEFT JOIN become in Python?", "options": ["0", "\"\"", "None"], "answer": 2, "explanation": "SQL NULL becomes None."}
]
```
