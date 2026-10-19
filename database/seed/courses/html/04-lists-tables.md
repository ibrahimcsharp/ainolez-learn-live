---
title: Lists and Tables
slug: lists-tables
summary: Show items in bulleted and numbered lists, and data in tables with headers.
minutes: 7
---
## Lists

- `<ul>` is an unordered (bulleted) list.
- `<ol>` is an ordered (numbered) list.
- Each item is an `<li>`.

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <h2>Shopping</h2>
  <ul>
    <li>Bread</li>
    <li>Milk</li>
    <li>Apples</li>
  </ul>

  <h2>Make tea</h2>
  <ol>
    <li>Boil water</li>
    <li>Add the tea bag</li>
    <li>Wait three minutes</li>
  </ol>
</body>
</html>
```

Lists can be nested: put a new `<ul>` inside an `<li>`. Website menus are usually lists of links.

## Tables

Tables are for **data** with rows and columns, not for page layout.

| Tag | Meaning |
|-----|---------|
| `<table>` | the table |
| `<tr>` | a row |
| `<th>` | a header cell |
| `<td>` | a data cell |
| `<caption>` | the table's title |

```html tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>td, th { border: 1px solid #999; padding: 4px 8px; }</style>
</head>
<body>
  <table>
    <caption>Exam results</caption>
    <thead>
      <tr><th>Name</th><th>Score</th></tr>
    </thead>
    <tbody>
      <tr><td>Amara</td><td>92</td></tr>
      <tr><td>Ben</td><td>78</td></tr>
    </tbody>
  </table>
</body>
</html>
```

`<thead>` and `<tbody>` group the header rows and the data rows, which helps screen readers and styling.

## Summary

- `<ul>` and `<ol>` hold `<li>` items.
- Tables use `<tr>` rows of `<th>` and `<td>` cells.

```exercise
{
  "title": "Three favourite foods",
  "prompt_md": "Write an **ordered** list (`<ol>`) with three `<li>` items: your three favourite foods.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <h2>My favourite foods</h2>\n\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <h2>My favourite foods</h2>\n  <ol>\n    <li>Jollof rice</li>\n    <li>Pizza</li>\n    <li>Mango</li>\n  </ol>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "<ol>\\s*(<li>[^<]+</li>\\s*){3}</ol>",
  "hint": "<ol> then three <li>...</li> items, then </ol>"
}
```

```quiz
[
  {"question": "Which tag makes a numbered list?", "options": ["<ol>", "<ul>", "<li>"], "answer": 0, "explanation": "ol = ordered list; ul = unordered list."},
  {"question": "Which tag is a header cell in a table?", "options": ["<th>", "<td>", "<tr>"], "answer": 0, "explanation": "th = table header; td = table data; tr = table row."}
]
```
