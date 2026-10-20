---
title: SELECT
slug: select
summary: Choose which columns to read, rename them and calculate new values.
minutes: 6
---
## Choosing columns

`SELECT *` returns every column. Name the columns you want instead, separated by commas:

```sql tryit
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, stock INTEGER);
INSERT INTO products (name, price, stock) VALUES
  ('Pen', 2, 120),
  ('Notebook', 5, 40),
  ('Backpack', 35, 8);

SELECT name, price FROM products;
```

Selecting only what you need makes results easier to read and queries faster on big tables.

## Calculations and aliases

A column can be a calculation. `AS` gives it a readable name (an **alias**):

```sql tryit
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, stock INTEGER);
INSERT INTO products (name, price, stock) VALUES
  ('Pen', 2, 120),
  ('Notebook', 5, 40),
  ('Backpack', 35, 8);

SELECT name, price * stock AS stock_value FROM products;
```

## DISTINCT

`DISTINCT` removes duplicate rows from the result:

```sql tryit
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT);
INSERT INTO orders (customer) VALUES ('Amara'), ('Ben'), ('Amara'), ('Chen'), ('Ben');

SELECT DISTINCT customer FROM orders;
```

## Summary

- `SELECT col1, col2 FROM table` reads only those columns.
- Columns can be calculations; `AS` names them.
- `SELECT DISTINCT` removes duplicates.

```exercise
{
  "title": "Price with tax",
  "prompt_md": "Select each product's `name` and its price multiplied by 2, named `double_price`.",
  "starter_code": "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER);\nINSERT INTO products (name, price) VALUES ('Pen', 2), ('Notebook', 5), ('Backpack', 35);\n\nSELECT name FROM products;",
  "solution_code": "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER);\nINSERT INTO products (name, price) VALUES ('Pen', 2), ('Notebook', 5), ('Backpack', 35);\n\nSELECT name, price * 2 AS double_price FROM products;",
  "check_type": "output",
  "expected_value": "name\tdouble_price\nPen\t4\nNotebook\t10\nBackpack\t70",
  "hint": "SELECT name, price * 2 AS double_price FROM products;"
}
```

```quiz
[
  {"question": "What does AS do in SELECT price * 2 AS doubled?", "options": ["Names the result column", "Creates a new table", "Filters rows"], "answer": 0, "explanation": "AS gives a column (or table) an alias."},
  {"question": "What does SELECT DISTINCT city FROM customers return?", "options": ["Every city once", "Every row", "The number of cities"], "answer": 0, "explanation": "DISTINCT removes repeated values."}
]
```
