---
title: Joining Tables
slug: joins
summary: Combine rows from two tables with keys, INNER JOIN and LEFT JOIN.
minutes: 9
---
## Why more than one table?

Instead of repeating a customer's name and city on every order, a database stores customers once and lets each order point to its customer with a **foreign key**:

- `customers.id` is the **primary key**: unique for each customer.
- `orders.customer_id` is a **foreign key**: it holds the id of a customer.

## INNER JOIN

`JOIN ... ON` matches rows from both tables. An inner join keeps only rows that have a match on both sides:

```sql tryit
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, item TEXT);
INSERT INTO customers (name) VALUES ('Amara'), ('Ben'), ('Chen');
INSERT INTO orders (customer_id, item) VALUES (1, 'Pen'), (1, 'Notebook'), (2, 'Backpack');

SELECT customers.name, orders.item
FROM orders
JOIN customers ON customers.id = orders.customer_id;
```

Chen has no orders, so Chen is not in the result.

## Table aliases

Short aliases keep joins readable:

```sql
SELECT c.name, o.item
FROM orders AS o
JOIN customers AS c ON c.id = o.customer_id;
```

## LEFT JOIN

A `LEFT JOIN` keeps **every** row from the left table, even without a match. Missing values become `NULL`. It is the way to find "customers with no orders":

```sql tryit
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, item TEXT);
INSERT INTO customers (name) VALUES ('Amara'), ('Ben'), ('Chen');
INSERT INTO orders (customer_id, item) VALUES (1, 'Pen'), (1, 'Notebook'), (2, 'Backpack');

SELECT c.name, COUNT(o.id) AS orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.id
GROUP BY c.name;
```

## Summary

- Primary keys identify rows; foreign keys point to rows in another table.
- `JOIN ... ON` combines matching rows.
- `LEFT JOIN` keeps every row of the first table.

```exercise
{
  "title": "Who bought what",
  "prompt_md": "Join the tables and select each order's customer `name` and `item`, sorted by `item`.",
  "starter_code": "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);\nCREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, item TEXT);\nINSERT INTO customers (name) VALUES ('Amara'), ('Ben');\nINSERT INTO orders (customer_id, item) VALUES (2, 'Lamp'), (1, 'Desk'), (2, 'Chair');\n\n",
  "solution_code": "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);\nCREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, item TEXT);\nINSERT INTO customers (name) VALUES ('Amara'), ('Ben');\nINSERT INTO orders (customer_id, item) VALUES (2, 'Lamp'), (1, 'Desk'), (2, 'Chair');\n\nSELECT c.name, o.item FROM orders AS o JOIN customers AS c ON c.id = o.customer_id ORDER BY o.item;",
  "check_type": "output",
  "expected_value": "name\titem\nBen\tChair\nAmara\tDesk\nBen\tLamp",
  "hint": "JOIN customers AS c ON c.id = o.customer_id ORDER BY o.item"
}
```

```quiz
[
  {"question": "Which join keeps customers who have no orders?", "options": ["customers LEFT JOIN orders", "customers INNER JOIN orders", "Neither"], "answer": 0, "explanation": "LEFT JOIN keeps every row of the left table."},
  {"question": "What is a foreign key?", "options": ["A column that holds the id of a row in another table", "A password for the table", "The first column"], "answer": 0, "explanation": "It links one table to another."}
]
```
