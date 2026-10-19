---
title: Headings and Text
slug: text
summary: Structure text with headings, paragraphs, emphasis, line breaks and comments.
minutes: 6
---
## Headings

HTML has six heading levels, `<h1>` (most important) to `<h6>`. Use one `<h1>` per page for its main title, then `<h2>` for sections and `<h3>` inside them. Search engines and screen readers use headings to understand the page.

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <h1>Healthy Recipes</h1>
  <h2>Breakfast</h2>
  <h3>Overnight oats</h3>
  <h2>Lunch</h2>
</body>
</html>
```

## Paragraphs and line breaks

`<p>` makes a paragraph. The browser ignores extra spaces and new lines in your code, so use `<br>` when you really need a line break, for example in an address.

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <p>This paragraph
     is written on      two lines, but shows on one.</p>
  <p>12 Baker Street<br>London<br>NW1 6XE</p>
</body>
</html>
```

## Emphasis and other text tags

| Tag | Meaning |
|-----|---------|
| `<strong>` | important (bold) |
| `<em>` | stressed (italic) |
| `<mark>` | highlighted |
| `<code>` | computer code |
| `<blockquote>` | a quotation |

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <p><strong>Warning:</strong> the oven is <em>very</em> hot.</p>
  <p>Type <code>print("hi")</code> to say hello in Python.</p>
  <p>Remember to <mark>save your work</mark>.</p>
  <!-- This is a comment: the browser does not show it -->
</body>
</html>
```

Choose tags for their **meaning**, not their look. The look is the job of CSS.

## Summary

- Use `<h1>` once, then `<h2>`–`<h6>` in order.
- `<p>` for paragraphs, `<br>` for a line break inside one.
- `<strong>` and `<em>` add meaning; `<!-- -->` writes comments.

```exercise
{
  "title": "Make it important",
  "prompt_md": "Wrap the word `free` in a `<strong>` element.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <p>Every course on this site is free.</p>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <p>Every course on this site is <strong>free</strong>.</p>\n</body>\n</html>",
  "check_type": "contains",
  "expected_value": "<strong>free</strong>",
  "hint": "<strong>free</strong>"
}
```

```quiz
[
  {"question": "How many <h1> headings should a page usually have?", "options": ["One", "Six", "As many as possible"], "answer": 0, "explanation": "One h1 names the page; sections use h2 and below."},
  {"question": "Which tag marks text as important?", "options": ["<strong>", "<br>", "<title>"], "answer": 0, "explanation": "strong means important; browsers show it in bold."}
]
```
