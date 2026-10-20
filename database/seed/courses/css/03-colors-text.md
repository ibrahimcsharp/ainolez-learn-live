---
title: Colours, Fonts and Units
slug: colors-text
summary: Use colour formats, style text with fonts, and choose between px, rem and percent.
minutes: 7
---
## Colours

CSS accepts colours in several formats:

```css
color: tomato;               /* a name */
color: #04AA6D;              /* hex: red, green, blue */
color: rgb(4 170 109);       /* rgb */
color: rgb(4 170 109 / 50%); /* with transparency */
color: hsl(158 95% 34%);     /* hue, saturation, lightness */
```

`color` sets the text colour and `background` the background.

## Text and fonts

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    body {
      font-family: Georgia, "Times New Roman", serif;
      line-height: 1.6;
      color: #1F2933;
    }
    h1 {
      font-family: Arial, sans-serif;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: #05192D;
    }
    .center { text-align: center; }
    a { color: #04AA6D; text-decoration: underline dotted; }
  </style>
</head>
<body>
  <h1 class="center">Reading is fun</h1>
  <p>A good line height (about 1.5) makes long text easier to read. Here is <a href="#">a link</a>.</p>
</body>
</html>
```

`font-family` takes a list: if the first font is missing, the browser tries the next. End with a generic family such as `sans-serif`.

## Units

| Unit | Meaning |
|------|---------|
| `px` | pixels: fixed size |
| `rem` | times the root font size (usually 16px) |
| `em` | times the element's own font size |
| `%` | percent of the parent |
| `vw` / `vh` | percent of the window's width / height |

Use `rem` for font sizes: they grow when a visitor makes the browser's text bigger.

## Summary

- Colours: names, hex, `rgb()` and `hsl()`.
- Style text with `font-family`, `font-size`, `font-weight`, `line-height` and `text-align`.
- Prefer `rem` for text sizes.

```exercise
{
  "title": "Centre and enlarge",
  "prompt_md": "Make the `h1` centred (`text-align: center`) with a font size of `2rem`.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    h1 {\n\n    }\n  </style>\n</head>\n<body>\n  <h1>Welcome</h1>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    h1 {\n      text-align: center;\n      font-size: 2rem;\n    }\n  </style>\n</head>\n<body>\n  <h1>Welcome</h1>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "h1\\s*\\{(?=[^}]*text-align\\s*:\\s*center)(?=[^}]*font-size\\s*:\\s*2rem)[^}]*\\}",
  "hint": "Inside h1 { }: text-align: center; font-size: 2rem;"
}
```

```quiz
[
  {"question": "Which unit grows with the visitor's browser text size?", "options": ["rem", "px", "vh"], "answer": 0, "explanation": "rem is relative to the root font size."},
  {"question": "What does #FF0000 mean?", "options": ["Red", "Green", "Blue"], "answer": 0, "explanation": "Hex is red, green, blue: FF red, 00 green, 00 blue."}
]
```
