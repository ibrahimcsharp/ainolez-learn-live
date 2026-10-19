---
title: CSS Grid
slug: grid
summary: Build two-dimensional layouts with grid-template-columns, fr units and gap.
minutes: 7
---
## Rows and columns

Flexbox lays out in one direction. **Grid** handles rows and columns together:

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 12px;
    }
    .grid div { background: #E7F0FF; padding: 20px; text-align: center; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="grid">
    <div>1</div><div>2</div><div>3</div>
    <div>4</div><div>5</div><div>6</div>
  </div>
</body>
</html>
```

`fr` means "a fraction of the free space". `1fr 2fr` makes the second column twice as wide. `repeat(3, 1fr)` is short for `1fr 1fr 1fr`.

## A responsive card grid without media queries

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    .cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 16px;
    }
    .card { background: #04AA6D; color: white; padding: 24px; border-radius: 8px; }
  </style>
</head>
<body>
  <div class="cards">
    <div class="card">HTML</div><div class="card">CSS</div><div class="card">JavaScript</div>
    <div class="card">Python</div><div class="card">SQL</div>
  </div>
</body>
</html>
```

Make the result window narrower: the cards wrap onto new rows by themselves.

## Spanning cells

An item can cover several columns or rows:

```css
.wide { grid-column: span 2; }
.header { grid-column: 1 / -1; }  /* from the first to the last line */
```

## Flexbox or Grid?

- **Flexbox**: a row or a column of things (a menu, buttons, a toolbar).
- **Grid**: a layout with rows **and** columns (a page, a gallery).

## Summary

- `display: grid` with `grid-template-columns` defines columns.
- `fr`, `repeat()` and `minmax()` make flexible grids.
- `grid-column: span 2` lets an item take more space.

```exercise
{
  "title": "Two columns",
  "prompt_md": "Make `.layout` a grid with **two equal columns** (`grid-template-columns: 1fr 1fr` or `repeat(2, 1fr)`).",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    .layout {\n\n    }\n  </style>\n</head>\n<body>\n  <div class=\"layout\"><div>Left</div><div>Right</div></div>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    .layout {\n      display: grid;\n      grid-template-columns: 1fr 1fr;\n    }\n  </style>\n</head>\n<body>\n  <div class=\"layout\"><div>Left</div><div>Right</div></div>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "\\.layout\\s*\\{(?=[^}]*display\\s*:\\s*grid)(?=[^}]*grid-template-columns\\s*:\\s*(1fr\\s+1fr|repeat\\(\\s*2\\s*,\\s*1fr\\s*\\)))[^}]*\\}",
  "hint": "display: grid; grid-template-columns: 1fr 1fr;"
}
```

```quiz
[
  {"question": "What does 1fr 2fr create?", "options": ["Two columns, the second twice as wide", "Two rows", "Columns of 1px and 2px"], "answer": 0, "explanation": "fr shares out the free space."},
  {"question": "Which is best for a photo gallery with rows and columns?", "options": ["Grid", "Flexbox", "Tables"], "answer": 0, "explanation": "Grid is built for two-dimensional layouts."}
]
```
