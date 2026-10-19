---
title: What Is SQL?
slug: intro
summary: Learn what databases and tables are, and create your first table with SQL.
minutes: 6
---
## Databases and tables

A **database** stores data so it can be searched and changed safely. A relational database keeps data in **tables**: rows and columns, like a spreadsheet.

| id | name  | city   |
|----|-------|--------|
| 1  | Amara | Lagos  |
| 2  | Ben   | London |

Each **row** is one record (one customer). Each **column** is one piece of information (name, city).

## SQL

**SQL** (Structured Query Language) is how you talk to a relational database. MySQL, PostgreSQL, SQLite and SQL Server all understand it, with small differences. Here you use **SQLite**, running inside your browser.

## Your first table

`CREATE TABLE` makes a table, `INSERT` adds rows and `SELECT` reads them. Press **Run**:

```sql tryit
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT,
  city TEXT
);

INSERT INTO customers (name, city) VALUES ('Amara', 'Lagos');
INSERT INTO customers (name, city) VALUES ('Ben', 'London');

SELECT * FROM customers;
```

- Every statement ends with `;`.
- `INTEGER PRIMARY KEY` gives each row a unique number automatically.
- Text values go in single quotes: `'Lagos'`.
- SQL keywords are not case sensitive, but writing them in capitals makes queries easier to read.

Each example on this site starts with an empty database, so the examples create their own tables.

## Summary

- A table has rows (records) and columns (fields).
- `CREATE TABLE`, `INSERT INTO` and `SELECT` create, fill and read a table.

```exercise
{
  "title": "Add a third customer",
  "prompt_md": "Insert a customer named `Chen` from `Beijing`, then select all rows. The result must be exactly the three customers shown in the hint.",
  "starter_code": "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);\nINSERT INTO customers (name, city) VALUES ('Amara', 'Lagos');\nINSERT INTO customers (name, city) VALUES ('Ben', 'London');\n-- add Chen here\n\nSELECT * FROM customers;",
  "solution_code": "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);\nINSERT INTO customers (name, city) VALUES ('Amara', 'Lagos');\nINSERT INTO customers (name, city) VALUES ('Ben', 'London');\nINSERT INTO customers (name, city) VALUES ('Chen', 'Beijing');\n\nSELECT * FROM customers;",
  "check_type": "output",
  "expected_value": "id\tname\tcity\n1\tAmara\tLagos\n2\tBen\tLondon\n3\tChen\tBeijing",
  "hint": "INSERT INTO customers (name, city) VALUES ('Chen', 'Beijing');"
}
```

```quiz
[
  {"question": "In a table, what is one row?", "options": ["One record", "One column name", "The whole database"], "answer": 0, "explanation": "Each row is one record, for example one customer."},
  {"question": "How do you write a text value in SQL?", "options": ["In single quotes: 'Lagos'", "Without quotes: Lagos", "In brackets: (Lagos)"], "answer": 0, "explanation": "Text values (strings) go in single quotes."}
]
```
