---
title: Sorting and Limiting
slug: order-limit
summary: Sort results with ORDER BY and return only the top rows with LIMIT.
minutes: 5
---
## ORDER BY

Rows come back in no guaranteed order unless you sort them. `ORDER BY` sorts ascending (`ASC`, the default) or descending (`DESC`):

```sql tryit
CREATE TABLE players (id INTEGER PRIMARY KEY, name TEXT, team TEXT, points INTEGER);
INSERT INTO players (name, team, points) VALUES
  ('Mia', 'red', 340), ('Leo', 'blue', 410), ('Ava', 'red', 410), ('Sam', 'blue', 120);

SELECT name, points FROM players ORDER BY points DESC;
```

## Sorting by more than one column

When two rows tie on the first column, the second column decides:

```sql tryit
CREATE TABLE players (id INTEGER PRIMARY KEY, name TEXT, team TEXT, points INTEGER);
INSERT INTO players (name, team, points) VALUES
  ('Mia', 'red', 340), ('Leo', 'blue', 410), ('Ava', 'red', 410), ('Sam', 'blue', 120);

SELECT name, points FROM players ORDER BY points DESC, name ASC;
```

## LIMIT and OFFSET

`LIMIT n` returns only the first n rows: perfect for "top 3" lists. `OFFSET` skips rows first, which is how pages of results work.

```sql tryit
CREATE TABLE players (id INTEGER PRIMARY KEY, name TEXT, team TEXT, points INTEGER);
INSERT INTO players (name, team, points) VALUES
  ('Mia', 'red', 340), ('Leo', 'blue', 410), ('Ava', 'red', 410), ('Sam', 'blue', 120);

SELECT name FROM players ORDER BY points DESC, name LIMIT 2;
SELECT name FROM players ORDER BY points DESC, name LIMIT 2 OFFSET 2;
```

!!! note
    SQL Server writes `SELECT TOP 2 ...` instead of `LIMIT 2`. MySQL, PostgreSQL and SQLite use `LIMIT`.

## Summary

- `ORDER BY col DESC` sorts from largest to smallest.
- Add more columns to break ties.
- `LIMIT` and `OFFSET` return a slice of the result.

```exercise
{
  "title": "Lowest score",
  "prompt_md": "Return the `name` of the **one** player with the fewest points.",
  "starter_code": "CREATE TABLE players (id INTEGER PRIMARY KEY, name TEXT, points INTEGER);\nINSERT INTO players (name, points) VALUES ('Mia', 340), ('Leo', 410), ('Sam', 120), ('Ava', 290);\n\nSELECT name FROM players;",
  "solution_code": "CREATE TABLE players (id INTEGER PRIMARY KEY, name TEXT, points INTEGER);\nINSERT INTO players (name, points) VALUES ('Mia', 340), ('Leo', 410), ('Sam', 120), ('Ava', 290);\n\nSELECT name FROM players ORDER BY points LIMIT 1;",
  "check_type": "output",
  "expected_value": "name\nSam",
  "hint": "ORDER BY points LIMIT 1"
}
```

```quiz
[
  {"question": "What is the default sort direction of ORDER BY?", "options": ["Ascending", "Descending", "Random"], "answer": 0, "explanation": "ASC (smallest first) is the default."},
  {"question": "Which query returns rows 11 to 20?", "options": ["LIMIT 10 OFFSET 10", "LIMIT 20", "LIMIT 10 OFFSET 20"], "answer": 0, "explanation": "Skip 10 rows, then return 10."}
]
```
