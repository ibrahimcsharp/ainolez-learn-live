---
title: Databases and Python
slug: intro
summary: What a database is, why we use SQL, and your first connection with sqlite3.
minutes: 7
---
## Why a database?

Lists and files are fine for small amounts of data. When you have thousands of users, orders or messages - and several people changing them at once - you need a **database**. A database stores data safely, finds it fast, and keeps it consistent.

Most databases are **relational**: data lives in **tables** of rows and columns, a bit like spreadsheets.

| id | name | city |
|---|---|---|
| 1 | Ana | Lima |
| 2 | Ben | Oslo |

You talk to them in **SQL** (Structured Query Language): `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`. If you have not seen SQL before, the *SQL* course on this site teaches it from scratch.

## SQLite: a database in a file

Python comes with `sqlite3`, a full SQL database stored in a single file - or in memory. It needs no server, so it runs right here in the browser. Phones, browsers and many apps use SQLite every day.

## Connect, execute, fetch

Every database library for Python follows the same pattern (it is a standard called **DB-API**):

1. **connect** to the database,
2. **execute** SQL,
3. **fetch** the results,
4. **commit** changes and **close** the connection.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")       # a temporary database in memory
db.execute("CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT, city TEXT)")
db.execute("INSERT INTO people (name, city) VALUES ('Ana', 'Lima')")
db.execute("INSERT INTO people (name, city) VALUES ('Ben', 'Oslo')")
db.commit()

rows = db.execute("SELECT id, name, city FROM people").fetchall()
print(rows)
for id, name, city in rows:
    print(id, name, city)
db.close()
```

Each row comes back as a tuple.

## A database in a file

Give `connect()` a file name and the data is saved there. Next time you connect, it is still there.

```python tryit
import sqlite3

db = sqlite3.connect("shop.db")
db.execute("CREATE TABLE IF NOT EXISTS visits (page TEXT)")
db.execute("INSERT INTO visits VALUES ('home')")
db.commit()
print(db.execute("SELECT COUNT(*) FROM visits").fetchone()[0], "visits so far")
db.close()
```

Run it several times: the count goes up, because the file keeps the data.

!!! note
    In the browser the file lives in temporary memory and disappears when you reload the page. On your own computer it is a real `shop.db` file.

## Summary

- Relational databases store data in tables and are queried with SQL.
- `sqlite3` is built in: `connect`, `execute`, `fetchall` / `fetchone`, `commit`, `close`.
- `":memory:"` gives a temporary database; a file name saves it.

```exercise
{
  "title": "Your first table",
  "prompt_md": "Create an in-memory database with a table `cities (name TEXT)`, insert `Paris` and `Tokyo`, and print the number of rows with `SELECT COUNT(*)`. The output must be `2`.",
  "starter_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\n",
  "solution_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\ndb.execute(\"CREATE TABLE cities (name TEXT)\")\ndb.execute(\"INSERT INTO cities VALUES ('Paris')\")\ndb.execute(\"INSERT INTO cities VALUES ('Tokyo')\")\nprint(db.execute(\"SELECT COUNT(*) FROM cities\").fetchone()[0])",
  "check_type": "output",
  "expected_value": "2",
  "hint": "fetchone() returns a tuple like (2,). Use [0] to get the number."
}
```

```quiz
[
  {"question": "Where does a relational database keep data?", "options": ["In tables of rows and columns", "In Python lists", "In JSON only"], "answer": 0, "explanation": "Tables hold rows (records) with columns (fields)."},
  {"question": "What does sqlite3.connect(\":memory:\") create?", "options": ["A file called :memory:", "A temporary database in memory", "A MySQL connection"], "answer": 1, "explanation": "It disappears when the connection closes."},
  {"question": "What does fetchall() return?", "options": ["One row", "A list of row tuples", "The number of rows"], "answer": 1, "explanation": "Each row is a tuple."}
]
```
