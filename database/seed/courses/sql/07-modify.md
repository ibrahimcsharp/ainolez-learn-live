---
title: Changing Data
slug: update-delete
summary: Change and remove rows safely with UPDATE and DELETE, and add constraints.
minutes: 8
---
## UPDATE

`UPDATE` changes existing rows. The `WHERE` decides **which** rows:

```sql tryit
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER);
INSERT INTO products (name, price) VALUES ('Pen', 2), ('Notebook', 5), ('Backpack', 35);

UPDATE products SET price = 30 WHERE name = 'Backpack';
UPDATE products SET price = price + 1 WHERE price < 10;

SELECT * FROM products;
```

!!! warning
    An `UPDATE` or `DELETE` without `WHERE` changes **every** row. Run the same `WHERE` as a `SELECT` first to see which rows you will touch.

## DELETE

```sql tryit
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER);
INSERT INTO products (name, price) VALUES ('Pen', 2), ('Notebook', 5), ('Backpack', 35);

DELETE FROM products WHERE price > 20;

SELECT * FROM products;
```

## Constraints protect your data

Constraints let the database refuse bad data:

- `NOT NULL`: the value is required.
- `UNIQUE`: no two rows may share the value.
- `CHECK (...)`: the value must pass a test.
- `DEFAULT`: the value used when none is given.

```sql tryit
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  age INTEGER CHECK (age >= 13),
  country TEXT DEFAULT 'unknown'
);
INSERT INTO users (email, age) VALUES ('amara@example.com', 21);
SELECT * FROM users;

-- Remove the dashes below to see the database refuse a duplicate email:
-- INSERT INTO users (email, age) VALUES ('amara@example.com', 30);
```

## Summary

- `UPDATE ... SET ... WHERE` changes rows; `DELETE FROM ... WHERE` removes them.
- Always check your `WHERE` first.
- Constraints such as `NOT NULL`, `UNIQUE` and `CHECK` keep data valid.

```exercise
{
  "title": "Restock",
  "prompt_md": "Set the `stock` of every product with a stock **below 10** to `50`, then select `name` and `stock` of all products.",
  "starter_code": "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, stock INTEGER);\nINSERT INTO products (name, stock) VALUES ('Pen', 120), ('Lamp', 3), ('Mug', 7);\n\n\nSELECT name, stock FROM products;",
  "solution_code": "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, stock INTEGER);\nINSERT INTO products (name, stock) VALUES ('Pen', 120), ('Lamp', 3), ('Mug', 7);\n\nUPDATE products SET stock = 50 WHERE stock < 10;\nSELECT name, stock FROM products;",
  "check_type": "output",
  "expected_value": "name\tstock\nPen\t120\nLamp\t50\nMug\t50",
  "hint": "UPDATE products SET stock = 50 WHERE stock < 10;"
}
```

```quiz
{
  "title": "Final quiz: SQL for Beginners",
  "final": true,
  "questions": [
    {"question": "Which statement reads data?", "options": ["SELECT", "INSERT", "UPDATE"], "answer": 0, "explanation": "SELECT reads; INSERT adds; UPDATE changes."},
    {"question": "Which clause filters rows?", "options": ["WHERE", "ORDER BY", "GROUP BY"], "answer": 0, "explanation": "WHERE keeps matching rows."},
    {"question": "What does ORDER BY points DESC LIMIT 3 return?", "options": ["The 3 highest scores", "The 3 lowest scores", "3 random rows"], "answer": 0, "explanation": "Sort largest first, then keep 3."},
    {"question": "Which clause filters groups?", "options": ["HAVING", "WHERE", "DISTINCT"], "answer": 0, "explanation": "HAVING runs after GROUP BY."},
    {"question": "What happens with DELETE FROM products; (no WHERE)?", "options": ["Every row is deleted", "Nothing", "Only the first row is deleted"], "answer": 0, "explanation": "Without WHERE, every row matches."},
    {"question": "Which join keeps every row of the first table?", "options": ["LEFT JOIN", "INNER JOIN", "CROSS JOIN"], "answer": 0, "explanation": "Unmatched rows get NULLs."}
  ]
}
```
