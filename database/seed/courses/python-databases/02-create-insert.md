---
title: Create Tables and Insert Rows
slug: create-insert
summary: Design a table with types and constraints, insert rows safely with placeholders, and avoid SQL injection.
minutes: 10
---
## Creating a table

A table has a name and columns. Each column has a type and optional rules (**constraints**).

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("""
    CREATE TABLE students (
        id      INTEGER PRIMARY KEY,
        name    TEXT NOT NULL,
        email   TEXT UNIQUE,
        age     INTEGER CHECK (age >= 0),
        joined  TEXT DEFAULT CURRENT_DATE
    )
""")
for column in db.execute("PRAGMA table_info(students)"):
    print(column[1], column[2])
```

- `PRIMARY KEY` - a unique id for each row; SQLite fills it in for you.
- `NOT NULL` - the value is required.
- `UNIQUE` - no two rows may share the value.
- `CHECK` - the value must pass a test.
- `DEFAULT` - used when no value is given.

## Inserting with placeholders

**Never** build SQL by pasting values into the text. Use `?` placeholders and pass the values separately. The library inserts them safely.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER)")

name, age = "Ana", 19
cursor = db.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
print("new id:", cursor.lastrowid)

db.execute("INSERT INTO students (name, age) VALUES (:name, :age)", {"name": "Ben", "age": 22})
db.commit()
print(db.execute("SELECT * FROM students").fetchall())
```

You can use `?` with a tuple, or named placeholders like `:name` with a dict.

## Why placeholders? SQL injection

If you paste user input into SQL, a user can type SQL of their own. This is called **SQL injection** and it is one of the most common security holes on the web.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE users (name TEXT, is_admin INTEGER)")
db.executemany("INSERT INTO users VALUES (?, ?)", [("ana", 0), ("root", 1)])

typed = "nobody' OR '1'='1"              # what an attacker types

unsafe = f"SELECT name FROM users WHERE name = '{typed}'"
print("unsafe:", db.execute(unsafe).fetchall())      # returns every user!

safe = db.execute("SELECT name FROM users WHERE name = ?", (typed,)).fetchall()
print("safe:  ", safe)                                 # no match, as it should be
```

## Inserting many rows

`executemany()` runs the same statement for every item in a list. Wrap related changes in `with db:` - it commits if everything worked, and undoes everything (rolls back) if an error happens.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE products (name TEXT UNIQUE, price REAL)")
products = [("pen", 1.2), ("notebook", 3.5), ("ruler", 0.9)]

with db:
    db.executemany("INSERT INTO products VALUES (?, ?)", products)
print(db.execute("SELECT COUNT(*) FROM products").fetchone())

try:
    with db:
        db.execute("INSERT INTO products VALUES ('glue', 2.0)")
        db.execute("INSERT INTO products VALUES ('pen', 9.9)")   # breaks UNIQUE
except sqlite3.IntegrityError as error:
    print("Rolled back:", error)
print(db.execute("SELECT COUNT(*) FROM products").fetchone())    # glue was undone too
```

## Summary

- `CREATE TABLE` with types and constraints (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`).
- Always insert values with `?` placeholders, never with f-strings.
- `executemany()` inserts lists; `with db:` commits or rolls back as one unit.

```exercise
{
  "title": "Safe insert",
  "prompt_md": "Insert every book from `books` into the table with `executemany()` and `?` placeholders, then print the title of the most expensive book using `ORDER BY price DESC LIMIT 1`. The output must be `Dune`.",
  "starter_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\ndb.execute(\"CREATE TABLE books (title TEXT, price REAL)\")\nbooks = [(\"Emma\", 7.5), (\"Dune\", 12.0), (\"Ulysses\", 9.25)]\n",
  "solution_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\ndb.execute(\"CREATE TABLE books (title TEXT, price REAL)\")\nbooks = [(\"Emma\", 7.5), (\"Dune\", 12.0), (\"Ulysses\", 9.25)]\ndb.executemany(\"INSERT INTO books VALUES (?, ?)\", books)\nprint(db.execute(\"SELECT title FROM books ORDER BY price DESC LIMIT 1\").fetchone()[0])",
  "check_type": "output",
  "expected_value": "Dune",
  "hint": "db.executemany(\"INSERT INTO books VALUES (?, ?)\", books)"
}
```

```quiz
[
  {"question": "How should you put a user's input into SQL?", "options": ["With an f-string", "With ? placeholders", "With + to join strings"], "answer": 1, "explanation": "Placeholders prevent SQL injection."},
  {"question": "What does a PRIMARY KEY do?", "options": ["Sorts the table", "Uniquely identifies each row", "Encrypts the row"], "answer": 1, "explanation": "Each row has its own key."},
  {"question": "What happens inside with db: when an error occurs?", "options": ["The changes so far are kept", "All changes in the block are rolled back", "Python ignores the error"], "answer": 1, "explanation": "The block commits only if everything succeeds."}
]
```
