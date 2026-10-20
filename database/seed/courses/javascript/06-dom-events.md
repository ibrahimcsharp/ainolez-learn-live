---
title: The DOM and Events
slug: dom-events
summary: Find elements, change text and styles, and react to clicks and typing.
minutes: 9
---
## The DOM

When the browser loads HTML, it builds the **DOM** (Document Object Model): a tree of objects, one per element. JavaScript changes the page by changing the DOM.

## Finding and changing elements

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <h1 id="title">Hello</h1>
  <p class="note">First note</p>
  <p class="note">Second note</p>

  <script>
    const title = document.querySelector("#title");
    title.textContent = "Changed by JavaScript";
    title.style.color = "#04AA6D";

    const notes = document.querySelectorAll(".note");
    notes.forEach((note) => note.classList.add("done"));
    console.log(notes.length, "notes found");
  </script>
</body>
</html>
```

`querySelector` takes a CSS selector and returns the first match; `querySelectorAll` returns all of them.

## Events

`addEventListener` runs a function when something happens: a click, a key press, a form being sent.

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <button id="add">Add one</button>
  <p>Clicks: <span id="count">0</span></p>

  <script>
    let clicks = 0;
    document.querySelector("#add").addEventListener("click", () => {
      clicks++;
      document.querySelector("#count").textContent = clicks;
    });
  </script>
</body>
</html>
```

## Reading input

```html tryit
<!DOCTYPE html>
<html lang="en">
<body>
  <label>Your name <input id="name"></label>
  <p id="greeting">Type your name.</p>

  <script>
    const input = document.querySelector("#name");
    input.addEventListener("input", () => {
      document.querySelector("#greeting").textContent = `Hello, ${input.value || "stranger"}!`;
    });
  </script>
</body>
</html>
```

## Creating elements

```javascript
const item = document.createElement("li");
item.textContent = "New task";
document.querySelector("ul").append(item);
```

!!! warning
    Use `textContent`, not `innerHTML`, for text a user typed. `innerHTML` runs it as HTML, which lets attackers inject code.

## Summary

- `document.querySelector()` finds elements.
- Change `textContent`, `style` and `classList`.
- `addEventListener("click", fn)` reacts to events.

```exercise
{
  "title": "A click handler",
  "prompt_md": "Add a `click` event listener to the button with the id `hello` that shows an alert or changes text. Your code must call `addEventListener(\"click\", ...)` on `#hello`.",
  "starter_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <button id=\"hello\">Say hello</button>\n  <p id=\"out\"></p>\n  <script>\n\n  </script>\n</body>\n</html>",
  "solution_code": "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n  <button id=\"hello\">Say hello</button>\n  <p id=\"out\"></p>\n  <script>\n    document.querySelector(\"#hello\").addEventListener(\"click\", () => {\n      document.querySelector(\"#out\").textContent = \"Hello!\";\n    });\n  </script>\n</body>\n</html>",
  "language": "html",
  "check_type": "regex",
  "expected_value": "(querySelector\\([\"']#hello[\"']\\)|getElementById\\([\"']hello[\"']\\))\\s*\\.addEventListener\\(\\s*[\"']click[\"']",
  "hint": "document.querySelector(\"#hello\").addEventListener(\"click\", () => { ... });"
}
```

```quiz
{
  "title": "Final quiz: JavaScript for Beginners",
  "final": true,
  "questions": [
    {"question": "Which keyword should you use for a value that never changes?", "options": ["const", "let", "var"], "answer": 0, "explanation": "const cannot be reassigned."},
    {"question": "Which operator compares value and type?", "options": ["===", "==", "="], "answer": 0, "explanation": "=== is strict equality; = assigns."},
    {"question": "What does [3, 8, 1].filter((n) => n > 2) return?", "options": ["[3, 8]", "[1]", "2"], "answer": 0, "explanation": "filter keeps the items that pass the test."},
    {"question": "How do you write a template literal?", "options": ["With backticks and ${}", "With single quotes", "With + only"], "answer": 0, "explanation": "`Hi ${name}`"},
    {"question": "Which method finds the first element matching a CSS selector?", "options": ["document.querySelector()", "document.find()", "document.css()"], "answer": 0, "explanation": "querySelector takes any CSS selector."},
    {"question": "Why prefer textContent over innerHTML for user input?", "options": ["innerHTML would run the input as HTML", "textContent is faster to type", "innerHTML does not exist"], "answer": 0, "explanation": "Inserting user input as HTML allows code injection."}
  ]
}
```
