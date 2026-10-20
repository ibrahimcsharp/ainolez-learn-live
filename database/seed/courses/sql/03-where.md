---
title: Filtering with WHERE
slug: where
summary: Keep only the rows you need with WHERE, AND, OR, IN, BETWEEN and LIKE.
minutes: 8
---
## WHERE

`WHERE` keeps only the rows that match a condition:

```sql tryit
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products (name, category, price) VALUES
  ('Pen', 'stationery', 2),
  ('Notebook', 'stationery', 5),
  ('Backpack', 'bags', 35),
  ('Laptop sleeve', 'bags', 20),
  ('Desk lamp', 'home', 25);

SELECT name, price FROM products WHERE price > 10;
```

Comparison operators: `=`, `<>` (not equal), `<`, `>`, `<=`, `>=`.

## AND, OR and NOT

```sql tryit
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products (name, category, price) VALUES
  ('Pen', 'stationery', 2),
  ('Notebook', 'stationery', 5),
  ('Backpack', 'bags', 35),
  ('Laptop sleeve', 'bags', 20),
  ('Desk lamp', 'home', 25);

SELECT name FROM products WHERE category = 'bags' AND price < 30;
SELECT name FROM products WHERE category = 'home' OR price < 3;
```

## IN, BETWEEN and LIKE

- `IN (...)` matches any value in a list.
- `BETWEEN a AND b` matches a range, including both ends.
- `LIKE` matches text patterns: `%` means "any characters", `_` means "one character".

```sql tryit
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products (name, category, price) VALUES
  ('Pen', 'stationery', 2),
  ('Notebook', 'stationery', 5),
  ('Backpack', 'bags', 35),
  ('Laptop sleeve', 'bags', 20),
  ('Desk lamp', 'home', 25);

SELECT name FROM products WHERE category IN ('home', 'bags');
SELECT name FROM products WHERE price BETWEEN 5 AND 25;
SELECT name FROM products WHERE name LIKE '%lamp%';
```

## Missing values: NULL

An empty value is `NULL`. Test for it with `IS NULL` or `IS NOT NULL`, never with `= NULL`.

## Summary

- `WHERE` filters rows; combine conditions with `AND`, `OR` and `NOT`.
- `IN`, `BETWEEN` and `LIKE` make common filters shorter.

```exercise
{
  "title": "Cheap stationery",
  "prompt_md": "Select the `name` of products in the `stationery` category that cost **less than 4**.",
  "starter_code": "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);\nINSERT INTO products (name, category, price) VALUES\n  ('Pen', 'stationery', 2),\n  ('Notebook', 'stationery', 5),\n  ('Eraser', 'stationery', 1),\n  ('Backpack', 'bags', 35);\n\nSELECT name FROM products;",
  "solution_code": "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);\nINSERT INTO products (name, category, price) VALUES\n  ('Pen', 'stationery', 2),\n  ('Notebook', 'stationery', 5),\n  ('Eraser', 'stationery', 1),\n  ('Backpack', 'bags', 35);\n\nSELECT name FROM products WHERE category = 'stationery' AND price < 4;",
  "check_type": "output",
  "expected_value": "name\nPen\nEraser",
  "hint": "WHERE category = 'stationery' AND price < 4"
}
```

```quiz
[
  {"question": "Which pattern matches every name that starts with 'Note'?", "options": ["LIKE 'Note%'", "LIKE '%Note'", "= 'Note'"], "answer": 0, "explanation": "% after the text means anything may follow."},
  {"question": "How do you find rows where email is empty (NULL)?", "options": ["WHERE email IS NULL", "WHERE email = NULL", "WHERE email = ''"], "answer": 0, "explanation": "NULL is not equal to anything, so use IS NULL."}
]
```
