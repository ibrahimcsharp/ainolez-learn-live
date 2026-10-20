---
title: Connecting to MySQL
slug: mysql
summary: Use the same DB-API pattern with a MySQL server through mysql-connector-python, and keep credentials safe.
minutes: 9
---
## From SQLite to a server

SQLite is perfect for learning, small apps and phones. Websites with many users usually run a database **server** such as **MySQL**, MariaDB or PostgreSQL. The server runs separately, many programs can use it at once, and it handles large amounts of data.

The good news: Python's database libraries all follow the same DB-API pattern. What you learned with `sqlite3` carries over almost unchanged.

!!! note
    This lesson needs a MySQL server and runs on your own computer, not in the browser editor. The last section has a runnable example that shows the same pattern with SQLite.

## Install the driver

In a terminal, inside your project's virtual environment:

```bash
pip install mysql-connector-python
```

## Connect and query

```python
import os
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="shop_app",
    password=os.environ["DB_PASSWORD"],   # never write passwords in code
    database="shop",
)
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        city VARCHAR(100)
    )
""")
cursor.execute("INSERT INTO customers (name, city) VALUES (%s, %s)", ("Ana", "Lima"))
db.commit()
print("new id:", cursor.lastrowid)

cursor.execute("SELECT id, name, city FROM customers WHERE city = %s", ("Lima",))
for id, name, city in cursor.fetchall():
    print(id, name, city)

cursor.close()
db.close()
```

## What is different from sqlite3?

| | sqlite3 | mysql-connector |
|---|---|---|
| Connect | `sqlite3.connect("file.db")` | `connect(host=, user=, password=, database=)` |
| Placeholder | `?` | `%s` |
| Auto id | `INTEGER PRIMARY KEY` | `INT AUTO_INCREMENT PRIMARY KEY` |
| Text type | `TEXT` | `VARCHAR(n)` or `TEXT` |
| Run SQL | `db.execute(...)` works | use a `cursor` |

The placeholder `%s` looks like old string formatting, but it is **not**: the driver still sends the value safely. Never use `%` or f-strings to put values into SQL yourself.

## Keep credentials out of code

A password written in your code ends up in Git, in screenshots and in chat messages. Read it from an environment variable or a `.env` file that is **not** committed, and give the app its own database user with only the permissions it needs.

## Same pattern, runnable here

This function works with any DB-API connection. Here it runs on SQLite; with MySQL you would only change the connection and use `%s`.

```python tryit
import sqlite3

def top_customers(db, limit, placeholder="?"):
    cursor = db.cursor()
    cursor.execute(
        f"SELECT name, SUM(total) FROM orders GROUP BY name ORDER BY SUM(total) DESC LIMIT {placeholder}",
        (limit,),
    )
    return cursor.fetchall()

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE orders (name TEXT, total REAL)")
db.executemany("INSERT INTO orders VALUES (?, ?)",
               [("Ana", 30), ("Ben", 48), ("Ana", 25), ("Cy", 10)])
print(top_customers(db, 2))
```

The f-string here only inserts the placeholder symbol (`?` or `%s`), never a value - the value still goes through the driver.

## Where next?

- **ORMs** such as Django's models or SQLAlchemy let you work with tables as Python classes and write less SQL.
- Learn **indexes** to make large queries fast.
- Back up your database regularly.

```exercise
{
  "title": "Placeholder style",
  "prompt_md": "Write a parameterised MySQL query string for finding a customer by email. Assign it to `query` and print it. The output must be exactly `SELECT id, name FROM customers WHERE email = %s`.",
  "starter_code": "query = \"\"\nprint(query)\n",
  "solution_code": "query = \"SELECT id, name FROM customers WHERE email = %s\"\nprint(query)\n",
  "check_type": "output",
  "expected_value": "SELECT id, name FROM customers WHERE email = %s",
  "hint": "mysql-connector uses %s as the placeholder."
}
```

```quiz
{
  "title": "Final quiz: Python and Databases",
  "final": true,
  "questions": [
    {"question": "Which module gives Python a built-in SQL database?", "options": ["sqlite3", "mysql", "sqlserver"], "answer": 0, "explanation": "sqlite3 is in the standard library."},
    {"question": "What is the safe way to put a value into SQL?", "options": ["f-strings", "placeholders such as ? or %s", "string concatenation"], "answer": 1, "explanation": "Placeholders prevent SQL injection."},
    {"question": "Which statement reads rows?", "options": ["INSERT", "SELECT", "UPDATE"], "answer": 1, "explanation": "SELECT queries data."},
    {"question": "What does db.commit() do?", "options": ["Saves the changes", "Closes the connection", "Deletes the table"], "answer": 0, "explanation": "commit makes the changes permanent."},
    {"question": "What does DELETE FROM users with no WHERE do?", "options": ["Nothing", "Deletes every row", "Deletes the table structure"], "answer": 1, "explanation": "Without WHERE every row matches."},
    {"question": "Which join keeps rows of the left table without a match?", "options": ["INNER JOIN", "LEFT JOIN"], "answer": 1, "explanation": "LEFT JOIN fills missing values with NULL."},
    {"question": "Which placeholder does mysql-connector use?", "options": ["?", "%s", ":value"], "answer": 1, "explanation": "MySQL drivers use %s."},
    {"question": "Where should a database password live?", "options": ["In the Python code", "In an environment variable or uncommitted .env file", "In a code comment"], "answer": 1, "explanation": "Keep secrets out of code and Git."}
  ]
}
```
