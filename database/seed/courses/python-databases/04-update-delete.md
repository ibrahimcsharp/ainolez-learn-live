---
title: Update and Delete Rows
slug: update-delete
summary: Change and remove rows safely, check how many rows changed, and drop tables.
minutes: 8
---
## UPDATE: change rows

`UPDATE` changes the columns you name, in every row that matches `WHERE`.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE stock (item TEXT, qty INTEGER, price REAL)")
db.executemany("INSERT INTO stock VALUES (?, ?, ?)",
               [("apple", 50, 0.4), ("pear", 0, 0.5), ("plum", 12, 0.3)])

with db:
    db.execute("UPDATE stock SET price = ? WHERE item = ?", (0.45, "apple"))
    db.execute("UPDATE stock SET qty = qty + 20 WHERE item = 'pear'")
print(db.execute("SELECT * FROM stock").fetchall())
```

You can use the current value in the new one: `qty = qty + 20`.

!!! warning
    An `UPDATE` or `DELETE` without `WHERE` changes **every row** in the table. Always write the `WHERE` first, and test it with a `SELECT` before you run the change.

## How many rows changed?

`rowcount` tells you how many rows the last statement changed - useful to check that the right row was found.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE stock (item TEXT, qty INTEGER)")
db.executemany("INSERT INTO stock VALUES (?, ?)", [("apple", 50), ("pear", 3), ("plum", 2)])

cursor = db.execute("UPDATE stock SET qty = 0 WHERE qty < ?", (5,))
print(cursor.rowcount, "rows set to 0")

cursor = db.execute("UPDATE stock SET qty = 1 WHERE item = ?", ("mango",))
if cursor.rowcount == 0:
    print("No such item")
```

## DELETE: remove rows

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE sessions (user TEXT, expired INTEGER)")
db.executemany("INSERT INTO sessions VALUES (?, ?)",
               [("ana", 0), ("ben", 1), ("cy", 1), ("dee", 0)])

with db:
    cursor = db.execute("DELETE FROM sessions WHERE expired = 1")
print("removed", cursor.rowcount)
print(db.execute("SELECT user FROM sessions").fetchall())
```

Many apps do not really delete important data. They set a column such as `deleted_at` instead (a **soft delete**), so it can be restored later.

## Dropping a table

`DROP TABLE` removes the whole table and its data. `IF EXISTS` avoids an error when it is already gone.

```python tryit
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE temp_data (x INTEGER)")
db.execute("DROP TABLE IF EXISTS temp_data")
db.execute("DROP TABLE IF EXISTS temp_data")   # no error the second time
print(db.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall())
```

## Summary

- `UPDATE table SET col = ? WHERE ...` changes matching rows.
- `DELETE FROM table WHERE ...` removes matching rows; never forget `WHERE`.
- `cursor.rowcount` tells you how many rows changed; `DROP TABLE IF EXISTS` removes a table.

```exercise
{
  "title": "Price rise",
  "prompt_md": "Raise the price of every **drink** by 10% with one `UPDATE`, then print the number of rows changed and the new total of all prices rounded to 2 decimals. The output must be `2 6.95`.",
  "starter_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\ndb.execute(\"CREATE TABLE menu (name TEXT, kind TEXT, price REAL)\")\ndb.executemany(\"INSERT INTO menu VALUES (?, ?, ?)\", [\n    (\"tea\", \"drink\", 2.0), (\"juice\", \"drink\", 2.5), (\"bun\", \"food\", 2.0),\n])\n",
  "solution_code": "import sqlite3\n\ndb = sqlite3.connect(\":memory:\")\ndb.execute(\"CREATE TABLE menu (name TEXT, kind TEXT, price REAL)\")\ndb.executemany(\"INSERT INTO menu VALUES (?, ?, ?)\", [\n    (\"tea\", \"drink\", 2.0), (\"juice\", \"drink\", 2.5), (\"bun\", \"food\", 2.0),\n])\ncursor = db.execute(\"UPDATE menu SET price = price * 1.1 WHERE kind = ?\", (\"drink\",))\ntotal = db.execute(\"SELECT SUM(price) FROM menu\").fetchone()[0]\nprint(cursor.rowcount, round(total, 2))",
  "check_type": "output",
  "expected_value": "2 6.95",
  "hint": "UPDATE menu SET price = price * 1.1 WHERE kind = ? - then SELECT SUM(price)."
}
```

```quiz
[
  {"question": "What happens with UPDATE stock SET qty = 0 (no WHERE)?", "options": ["Nothing", "Every row gets qty = 0", "Only the first row changes"], "answer": 1, "explanation": "Without WHERE, every row matches."},
  {"question": "What does cursor.rowcount tell you after a DELETE?", "options": ["Rows left in the table", "Rows deleted", "Columns in the table"], "answer": 1, "explanation": "It counts the rows the statement changed."},
  {"question": "What is a soft delete?", "options": ["Deleting slowly", "Marking a row as deleted instead of removing it", "DROP TABLE"], "answer": 1, "explanation": "The row stays and can be restored."}
]
```
