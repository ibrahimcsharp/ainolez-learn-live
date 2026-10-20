---
title: COUNT, SUM and GROUP BY
slug: group-by
summary: Summarise many rows into totals with aggregate functions, GROUP BY and HAVING.
minutes: 8
---
## Aggregate functions

An aggregate function turns many rows into one value:

| Function | Result |
|----------|--------|
| `COUNT(*)` | number of rows |
| `SUM(col)` | total |
| `AVG(col)` | average |
| `MIN(col)` / `MAX(col)` | smallest / largest |

```sql tryit
CREATE TABLE sales (id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO sales (region, amount) VALUES
  ('north', 100), ('south', 250), ('north', 300), ('east', 50), ('south', 150);

SELECT COUNT(*) AS orders, SUM(amount) AS total, MAX(amount) AS biggest FROM sales;
```

## GROUP BY

`GROUP BY` makes one group per value and runs the aggregate for each group:

```sql tryit
CREATE TABLE sales (id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO sales (region, amount) VALUES
  ('north', 100), ('south', 250), ('north', 300), ('east', 50), ('south', 150);

SELECT region, COUNT(*) AS orders, SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY total DESC;
```

Every column in the `SELECT` must either be in the `GROUP BY` or inside an aggregate function.

## HAVING

`WHERE` filters rows **before** grouping. `HAVING` filters groups **after** grouping:

```sql tryit
CREATE TABLE sales (id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO sales (region, amount) VALUES
  ('north', 100), ('south', 250), ('north', 300), ('east', 50), ('south', 150);

SELECT region, SUM(amount) AS total
FROM sales
GROUP BY region
HAVING SUM(amount) > 200;
```

## Summary

- `COUNT`, `SUM`, `AVG`, `MIN` and `MAX` summarise rows.
- `GROUP BY` computes them per group.
- `HAVING` filters groups; `WHERE` filters rows.

```exercise
{
  "title": "Orders per customer",
  "prompt_md": "For each `customer`, show the number of orders as `orders`. Sort by customer name.",
  "starter_code": "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT, amount INTEGER);\nINSERT INTO orders (customer, amount) VALUES ('Ben', 20), ('Amara', 35), ('Ben', 10), ('Chen', 60), ('Ben', 5);\n\nSELECT customer FROM orders;",
  "solution_code": "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT, amount INTEGER);\nINSERT INTO orders (customer, amount) VALUES ('Ben', 20), ('Amara', 35), ('Ben', 10), ('Chen', 60), ('Ben', 5);\n\nSELECT customer, COUNT(*) AS orders FROM orders GROUP BY customer ORDER BY customer;",
  "check_type": "output",
  "expected_value": "customer\torders\nAmara\t1\nBen\t3\nChen\t1",
  "hint": "SELECT customer, COUNT(*) AS orders FROM orders GROUP BY customer ORDER BY customer;"
}
```

```quiz
[
  {"question": "Which clause filters groups after GROUP BY?", "options": ["HAVING", "WHERE", "LIMIT"], "answer": 0, "explanation": "HAVING works on the grouped results."},
  {"question": "What does COUNT(*) return?", "options": ["The number of rows", "The sum of a column", "The first row"], "answer": 0, "explanation": "COUNT(*) counts rows."}
]
```
