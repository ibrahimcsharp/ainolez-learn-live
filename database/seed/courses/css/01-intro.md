---
title: What Is CSS?
slug: intro
summary: Write your first CSS rules and learn the three ways to add CSS to a page.
minutes: 6
---
## Style for HTML

**CSS** (Cascading Style Sheets) says how HTML elements look: colours, fonts, sizes, spacing and layout. The same HTML can look completely different with different CSS.

## A CSS rule

```css
h1 {
  color: navy;
  font-size: 40px;
}
```

- `h1` is the **selector**: which elements the rule styles.
- `color` and `font-size` are **properties**.
- `navy` and `40px` are **values**.
- Each declaration ends with `;`, and the block sits in `{ }`.

## Adding CSS to a page

There are three ways. The `<style>` element in the `<head>` is the easiest for trying things out:

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    body { font-family: Arial, sans-serif; background: #F5F7FA; }
    h1 { color: #04AA6D; }
    p { color: #333; font-size: 18px; }
  </style>
</head>
<body>
  <h1>Styled with CSS</h1>
  <p>Change the colours in the style block and run again.</p>
</body>
</html>
```

1. **External file** (best for real sites): `<link rel="stylesheet" href="styles.css">` in the `<head>`. One file styles every page.
2. **`<style>` element**: CSS for one page.
3. **Inline**: `<p style="color: red">`. Hard to maintain; avoid it.

## The cascade

When two rules style the same element, the more **specific** selector wins, and if they are equally specific, the **later** rule wins. That is the "cascading" in CSS.

## Summary

- A rule is `selector { property: value; }`.
- Use an external stylesheet for real sites.
- When rules clash, the more specific or the later rule wins.

```exercise
{
  "title": "Colour the heading",
  "prompt_md": "Add a rule that makes every `h1` **red** (`color: red`).",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n\n  </style>\n</head>\n<body>\n  <h1>Hello</h1>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    h1 { color: red; }\n  </style>\n</head>\n<body>\n  <h1>Hello</h1>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "h1\\s*\\{[^}]*color\\s*:\\s*red",
  "hint": "h1 { color: red; }"
}
```

```quiz
[
  {"question": "In p { color: blue; }, what is p?", "options": ["The selector", "The property", "The value"], "answer": 0, "explanation": "The selector chooses which elements are styled."},
  {"question": "What is the best way to add CSS to a whole website?", "options": ["An external stylesheet with <link>", "Inline style attributes", "A <style> block on every page"], "answer": 0, "explanation": "One file styles every page and is easy to change."}
]
```
