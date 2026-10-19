---
title: Semantic Layout
slug: semantic
summary: Structure a page with header, nav, main, section, article and footer.
minutes: 6
---
## div and span

`<div>` is a block container with no meaning: it groups things so CSS can style them. `<span>` is the same for a few words inside a line.

## Semantic elements

**Semantic** elements say what their content **is**. They look like `<div>` but help screen readers, search engines and other developers:

| Element | Use it for |
|---------|------------|
| `<header>` | the page or section intro: logo, title |
| `<nav>` | the main links |
| `<main>` | the main content (once per page) |
| `<section>` | a themed part with a heading |
| `<article>` | something that stands on its own: a post, a card |
| `<aside>` | side content |
| `<footer>` | the bottom: copyright, contact |

```html tryit
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    header, nav, main, footer { padding: 8px; margin: 4px 0; border: 1px dashed #04AA6D; }
  </style>
</head>
<body>
  <header><h1>Tasty Blog</h1></header>
  <nav>
    <a href="#">Home</a> | <a href="#">Recipes</a> | <a href="#">About</a>
  </nav>
  <main>
    <article>
      <h2>Perfect pancakes</h2>
      <p>Mix flour, milk and eggs...</p>
    </article>
  </main>
  <footer>&copy; 2026 Tasty Blog</footer>
</body>
</html>
```

## Accessibility in one minute

- Headings in order, one `<h1>`.
- Alt text on images.
- A `<label>` for every form field (next lesson).
- Semantic elements instead of a page of `<div>`s.

These habits make your page usable by everyone, including people using screen readers, and they also help your search ranking.

## Summary

- `<div>` and `<span>` group content without meaning.
- `<header>`, `<nav>`, `<main>`, `<article>` and `<footer>` describe the page's parts.

```exercise
{
  "title": "Add a footer",
  "prompt_md": "Add a `<footer>` element after `<main>` containing the text `Contact: hello@example.com`.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <header><h1>My site</h1></header>\n  <main><p>Welcome!</p></main>\n\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <header><h1>My site</h1></header>\n  <main><p>Welcome!</p></main>\n  <footer>Contact: hello@example.com</footer>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "<footer>[\\s\\S]*hello@example\\.com[\\s\\S]*</footer>",
  "hint": "<footer>Contact: hello@example.com</footer>"
}
```

```quiz
[
  {"question": "Which element holds the main links of a site?", "options": ["<nav>", "<aside>", "<span>"], "answer": 0, "explanation": "nav is for navigation links."},
  {"question": "Why use semantic elements?", "options": ["They describe the content for browsers, search engines and screen readers", "They load faster than div", "They add colours automatically"], "answer": 0, "explanation": "Semantic tags carry meaning; div does not."}
]
```
