---
title: Flexbox
slug: flexbox
summary: Lay out items in a row or column, space them and align them with Flexbox.
minutes: 8
---
## A flex container

`display: flex` on a parent lines up its children in a row:

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    .row { display: flex; gap: 12px; background: #F5F7FA; padding: 12px; }
    .item { background: #04AA6D; color: white; padding: 16px; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="row">
    <div class="item">One</div>
    <div class="item">Two</div>
    <div class="item">Three</div>
  </div>
</body>
</html>
```

`gap` sets the space between items.

## Direction, spacing and alignment

| Property (on the container) | Common values |
|---|---|
| `flex-direction` | `row`, `column` |
| `justify-content` (main axis) | `flex-start`, `center`, `space-between`, `space-around` |
| `align-items` (cross axis) | `stretch`, `center`, `flex-start`, `flex-end` |
| `flex-wrap` | `nowrap`, `wrap` |

A navigation bar with the logo left and links right:

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #05192D;
      color: white;
      padding: 12px 20px;
    }
    nav { display: flex; gap: 16px; }
    nav a { color: #03EF62; text-decoration: none; }
  </style>
</head>
<body>
  <header>
    <strong>ainolez</strong>
    <nav><a href="#">Courses</a><a href="#">Community</a><a href="#">Log in</a></nav>
  </header>
</body>
</html>
```

## Growing items

`flex: 1` on a child lets it take the free space. Centring something both ways is now easy:

```css
.page { display: flex; justify-content: center; align-items: center; min-height: 100vh; }
```

## Summary

- `display: flex` on the parent; the children become flex items.
- `justify-content` spaces along the row; `align-items` aligns across it.
- `gap`, `flex-wrap` and `flex: 1` handle spacing, wrapping and growing.

```exercise
{
  "title": "Centre the items",
  "prompt_md": "Make `.row` a flex container whose items are centred along the row (`justify-content: center`).",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    .row {\n\n    }\n  </style>\n</head>\n<body>\n  <div class=\"row\"><span>A</span><span>B</span></div>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    .row {\n      display: flex;\n      justify-content: center;\n    }\n  </style>\n</head>\n<body>\n  <div class=\"row\"><span>A</span><span>B</span></div>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "\\.row\\s*\\{(?=[^}]*display\\s*:\\s*flex)(?=[^}]*justify-content\\s*:\\s*center)[^}]*\\}",
  "hint": "display: flex; justify-content: center;"
}
```

```quiz
[
  {"question": "Where do you put display: flex?", "options": ["On the parent container", "On every child", "On the body only"], "answer": 0, "explanation": "The parent becomes the flex container."},
  {"question": "Which property puts space between items, pushing the first and last to the edges?", "options": ["justify-content: space-between", "align-items: center", "flex-wrap: wrap"], "answer": 0, "explanation": "space-between spreads items across the row."}
]
```
