---
title: What Is JavaScript?
slug: intro
summary: Learn what JavaScript does on a web page and print your first output with console.log.
minutes: 5
---
## The language of the browser

HTML gives a page structure, CSS gives it style, and **JavaScript** gives it behaviour: menus that open, forms that check themselves, games, maps, chat. Every browser runs JavaScript, and with Node.js it also runs on servers.

!!! note
    JavaScript and Java are different languages. The similar name was a marketing idea from 1995.

## Your first program

`console.log()` prints a value. In this editor the output appears under the code; on a real page it appears in the browser's console (press F12).

```javascript tryit
console.log("Hello, JavaScript!");
console.log(2 + 3);
console.log("Learn it.", "Code it.", "Own it.");
```

## Statements and comments

A program is a list of **statements**, run top to bottom. Ending each one with `;` is a good habit.

```javascript tryit
// A comment on one line
/* A comment
   on several lines */
console.log("Comments are ignored when the code runs");
```

## JavaScript in a web page

On a real site JavaScript lives in a `<script>` element, usually in its own file:

```html
<script src="app.js"></script>
```

You will change a page with JavaScript in the last chapter.

## Summary

- JavaScript makes web pages interactive.
- `console.log()` prints values.
- `//` and `/* */` write comments.

```exercise
{
  "title": "Say hello",
  "prompt_md": "Print exactly `Hello, world!` with `console.log`.",
  "starter_code": "// your code here\n",
  "solution_code": "console.log(\"Hello, world!\");",
  "check_type": "output",
  "expected_value": "Hello, world!",
  "hint": "console.log(\"Hello, world!\");"
}
```

```quiz
[
  {"question": "Which function prints a value in JavaScript?", "options": ["console.log()", "print()", "echo()"], "answer": 0, "explanation": "print() is Python; echo is PHP."},
  {"question": "Where does JavaScript run?", "options": ["In browsers and, with Node.js, on servers", "Only on servers", "Only in Java programs"], "answer": 0, "explanation": "Every browser runs it; Node.js runs it outside the browser."}
]
```
