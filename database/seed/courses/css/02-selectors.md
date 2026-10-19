---
title: Selectors
slug: selectors
summary: Target elements by tag, class and id, combine selectors, and style states like hover.
minutes: 7
---
## Type, class and id

| Selector | Matches |
|----------|---------|
| `p` | every `<p>` |
| `.card` | every element with `class="card"` |
| `#logo` | the one element with `id="logo"` |
| `*` | every element |

Classes are the workhorse of CSS: an element can have several (`class="card featured"`), and many elements can share one.

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    p { color: #555; }
    .highlight { background: #FFF4A3; }
    .big { font-size: 24px; }
    #intro { font-weight: bold; }
  </style>
</head>
<body>
  <p id="intro">An introduction.</p>
  <p class="highlight">A highlighted note.</p>
  <p class="highlight big">Highlighted and big.</p>
</body>
</html>
```

## Combining selectors

- `h1, h2` — a **group**: both headings.
- `nav a` — a **descendant**: links inside a `nav`.
- `ul > li` — a **child**: `li` directly inside a `ul`.
- `a.button` — a link that also has the class `button`.

## Pseudo-classes

A pseudo-class selects an element in a **state**:

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    nav a { color: #04AA6D; text-decoration: none; padding: 4px; }
    nav a:hover { background: #04AA6D; color: white; }
    li:first-child { font-weight: bold; }
    li:nth-child(even) { color: gray; }
    input:focus { outline: 3px solid #03EF62; }
  </style>
</head>
<body>
  <nav><a href="#">Home</a> <a href="#">Courses</a> <a href="#">About</a></nav>
  <ul><li>First</li><li>Second</li><li>Third</li><li>Fourth</li></ul>
  <input placeholder="Click me">
</body>
</html>
```

## Specificity

From weakest to strongest: type (`p`) → class (`.note`) → id (`#main`) → inline style. Prefer classes: they are strong enough and easy to reuse.

## Summary

- Use `.class` for most styling, `#id` rarely.
- Spaces mean "inside"; commas mean "and".
- `:hover`, `:focus` and `:nth-child()` style states and positions.

```exercise
{
  "title": "A button class",
  "prompt_md": "Write a rule for the class `.btn` that sets `background: green`.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n\n  </style>\n</head>\n<body>\n  <a class=\"btn\" href=\"#\">Start</a>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    .btn { background: green; color: white; }\n  </style>\n</head>\n<body>\n  <a class=\"btn\" href=\"#\">Start</a>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "\\.btn\\s*\\{[^}]*background(-color)?\\s*:\\s*green",
  "hint": ".btn { background: green; }"
}
```

```quiz
[
  {"question": "Which selector matches class=\"card\"?", "options": [".card", "#card", "card"], "answer": 0, "explanation": "A dot selects a class; # selects an id."},
  {"question": "What does nav a select?", "options": ["Links inside a nav", "Both nav and a elements", "A nav inside a link"], "answer": 0, "explanation": "A space means descendant: a inside nav."}
]
```
