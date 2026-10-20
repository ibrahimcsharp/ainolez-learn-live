---
title: Your First Web Page
slug: intro
summary: Learn what HTML is, how elements and tags work, and the parts of every HTML page.
minutes: 6
---
## What is HTML?

**HTML** (HyperText Markup Language) describes the structure of a web page: this is a heading, this is a paragraph, this is a link. The browser reads the HTML and draws the page.

- **HTML** gives structure.
- **CSS** gives style (colours, layout).
- **JavaScript** gives behaviour (what happens when you click).

## Elements and tags

An **element** usually has an opening tag, content and a closing tag:

```html
<p>This is a paragraph.</p>
```

`<p>` opens the paragraph, `</p>` closes it. Some elements, such as `<br>` (line break) and `<img>`, have no content and no closing tag.

## A complete page

Every HTML page has the same skeleton. Press **Run**, then change the text and run again:

```html tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>My first page</title>
</head>
<body>
  <h1>Hello, web!</h1>
  <p>I wrote this page myself.</p>
</body>
</html>
```

- `<!DOCTYPE html>` tells the browser this is modern HTML.
- `<html lang="en">` wraps the whole page and names its language.
- `<head>` holds information **about** the page: the character set and the title shown in the browser tab.
- `<body>` holds everything visible.

## Attributes

Attributes add extra information inside the opening tag, as `name="value"`. `lang="en"` above is an attribute. You will meet many more, such as `href` for links.

## Summary

- HTML structures content with elements written as tags.
- Every page has `<!DOCTYPE html>`, `<html>`, `<head>` and `<body>`.
- Attributes go inside the opening tag.

```exercise
{
  "title": "Add a heading",
  "prompt_md": "Add an `<h1>` heading with the text `About me` at the top of the body.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <title>About</title>\n</head>\n<body>\n  <p>I am learning HTML.</p>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <title>About</title>\n</head>\n<body>\n  <h1>About me</h1>\n  <p>I am learning HTML.</p>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "<h1>\\s*About me\\s*</h1>",
  "hint": "<h1>About me</h1>"
}
```

```quiz
[
  {"question": "Which part of the page holds the visible content?", "options": ["<body>", "<head>", "<title>"], "answer": 0, "explanation": "The body holds everything the visitor sees."},
  {"question": "What does CSS add to a page?", "options": ["Style", "Structure", "A database"], "answer": 0, "explanation": "HTML is structure, CSS is style, JavaScript is behaviour."}
]
```
