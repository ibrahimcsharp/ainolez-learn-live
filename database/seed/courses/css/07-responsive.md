---
title: Responsive Design
slug: responsive
summary: Make pages work on phones with the viewport tag, fluid images and media queries.
minutes: 7
---
## One page, every screen

More than half of all web visits are on phones. A **responsive** page adapts its layout to the screen width.

## The viewport tag

Without this line in the `<head>`, phones pretend to be a wide desktop and shrink the page:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

## Fluid images

```css
img { max-width: 100%; height: auto; }
```

The image never becomes wider than its container.

## Media queries

A media query applies rules only when a condition is true. Design for small screens first, then add rules for larger ones (**mobile first**):

```css tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    .layout { display: grid; gap: 12px; }
    .layout div { background: #E7F0FF; padding: 20px; }

    /* screens 600px and wider: two columns */
    @media (min-width: 600px) {
      .layout { grid-template-columns: 2fr 1fr; }
      .layout div { background: #FFF4A3; }
    }
  </style>
</head>
<body>
  <div class="layout">
    <div>Main content</div>
    <div>Sidebar</div>
  </div>
</body>
</html>
```

Make the result area narrower and wider to see the layout change at 600px.

## Responsive habits

- Use `rem`, `%` and `fr` more than fixed `px` widths.
- Make buttons and links large enough to tap (about 44px high).
- Test on a real phone, or with your browser's device mode (F12).

## Summary

- Always add the viewport meta tag.
- `max-width: 100%` keeps images inside their box.
- `@media (min-width: ...)` adds rules for larger screens.

```exercise
{
  "title": "Bigger text on big screens",
  "prompt_md": "Add a media query for screens of **at least 800px** that sets the `h1` font size to `3rem`.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    h1 { font-size: 2rem; }\n\n  </style>\n</head>\n<body>\n  <h1>Hello</h1>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <style>\n    h1 { font-size: 2rem; }\n    @media (min-width: 800px) {\n      h1 { font-size: 3rem; }\n    }\n  </style>\n</head>\n<body>\n  <h1>Hello</h1>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "@media\\s*\\(\\s*min-width\\s*:\\s*800px\\s*\\)\\s*\\{\\s*h1\\s*\\{[^}]*font-size\\s*:\\s*3rem",
  "hint": "@media (min-width: 800px) { h1 { font-size: 3rem; } }"
}
```

```quiz
{
  "title": "Final quiz: CSS for Beginners",
  "final": true,
  "questions": [
    {"question": "Which selector matches class=\"note\"?", "options": [".note", "#note", "note"], "answer": 0, "explanation": "A dot selects a class."},
    {"question": "Which part of the box model is outside the border?", "options": ["margin", "padding", "content"], "answer": 0, "explanation": "Margin is the space outside."},
    {"question": "Which property spaces flex items along the row?", "options": ["justify-content", "align-items", "font-size"], "answer": 0, "explanation": "justify-content works on the main axis."},
    {"question": "What does grid-template-columns: repeat(3, 1fr) make?", "options": ["Three equal columns", "Three rows", "One column 3px wide"], "answer": 0, "explanation": "repeat(3, 1fr) = 1fr 1fr 1fr."},
    {"question": "Which tag stops phones shrinking your page?", "options": ["The viewport meta tag", "The title tag", "The charset meta tag"], "answer": 0, "explanation": "width=device-width uses the phone's real width."},
    {"question": "What does mobile first mean?", "options": ["Write styles for small screens, then add media queries for larger ones", "Build an app before a website", "Hide content on phones"], "answer": 0, "explanation": "Start simple and add layout as space grows."}
  ]
}
```
