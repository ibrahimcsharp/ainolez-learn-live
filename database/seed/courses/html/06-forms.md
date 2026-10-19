---
title: Forms
slug: forms
summary: Collect input with form, input, label, select, textarea and buttons.
minutes: 8
---
## A form

A `<form>` collects input and sends it to a server. Each field is an `<input>` (or `<select>`, `<textarea>`) with a `name`, and each field needs a `<label>`:

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <form>
    <p>
      <label for="name">Your name</label><br>
      <input id="name" name="name" type="text" required>
    </p>
    <p>
      <label for="email">Email</label><br>
      <input id="email" name="email" type="email" placeholder="you@example.com">
    </p>
    <button type="submit">Join</button>
  </form>
</body>
</html>
```

The label's `for` matches the input's `id`: clicking the label focuses the field, and screen readers read the label aloud.

## Input types

The `type` gives the right keyboard on phones and free checking in the browser:

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <form>
    <p><label>Age <input type="number" min="13" max="120"></label></p>
    <p><label>Birthday <input type="date"></label></p>
    <p><label>Password <input type="password" minlength="8"></label></p>
    <p><label><input type="checkbox" name="news"> Send me the newsletter</label></p>
    <p>
      Level:
      <label><input type="radio" name="level" value="new"> New</label>
      <label><input type="radio" name="level" value="some"> Some experience</label>
    </p>
    <button>Check</button>
  </form>
</body>
</html>
```

Radio buttons with the same `name` form a group where only one can be chosen.

## select and textarea

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <form>
    <p>
      <label for="topic">Topic</label>
      <select id="topic" name="topic">
        <option>HTML</option>
        <option>CSS</option>
        <option>Python</option>
      </select>
    </p>
    <p>
      <label for="msg">Message</label><br>
      <textarea id="msg" name="message" rows="4" cols="30"></textarea>
    </p>
    <button>Send</button>
  </form>
</body>
</html>
```

!!! note
    Browser checks like `required` help visitors, but a server must always check the data again: anyone can send any data to a server.

## Summary

- A `<form>` holds fields and a submit `<button>`.
- Give every field a `name` and a `<label>`.
- Input types (`email`, `number`, `date`, `checkbox`, `radio`) give free checks and better keyboards.

```exercise
{
  "title": "An email field",
  "prompt_md": "Add an `<input>` of type `email` with the id `email`, and a `<label>` for it.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <form>\n\n    <button>Subscribe</button>\n  </form>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <form>\n    <label for=\"email\">Email</label>\n    <input id=\"email\" name=\"email\" type=\"email\">\n    <button>Subscribe</button>\n  </form>\n</body>\n</html>",
  "check_type": "regex",
  "expected_value": "<label[^>]*for=\"email\"[\\s\\S]*<input(?=[^>]*type=\"email\")(?=[^>]*id=\"email\")[^>]*>",
  "hint": "<label for=\"email\">Email</label> <input id=\"email\" type=\"email\">"
}
```

```quiz
{
  "title": "Final quiz: HTML for Beginners",
  "final": true,
  "questions": [
    {"question": "Which part of an HTML page is visible?", "options": ["<body>", "<head>", "<!DOCTYPE>"], "answer": 0, "explanation": "The body holds the visible content."},
    {"question": "Which attribute gives an image a text description?", "options": ["alt", "src", "title"], "answer": 0, "explanation": "alt describes the image."},
    {"question": "Which tag makes a link?", "options": ["<a>", "<link>", "<href>"], "answer": 0, "explanation": "<a href=...> is a link; <link> loads files like CSS."},
    {"question": "What should tables be used for?", "options": ["Data in rows and columns", "Page layout", "Navigation menus"], "answer": 0, "explanation": "Use CSS for layout; tables are for data."},
    {"question": "Which element holds the main content of the page?", "options": ["<main>", "<section>", "<div>"], "answer": 0, "explanation": "main appears once and holds the main content."},
    {"question": "How do you connect a label to its input?", "options": ["label for= matches input id=", "Put them in the same paragraph", "Give them the same class"], "answer": 0, "explanation": "for and id link them."}
  ]
}
```
