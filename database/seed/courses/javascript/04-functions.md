---
title: Functions
slug: functions
summary: Write functions with parameters and return values, including arrow functions.
minutes: 7
---
## Declaring a function

```javascript tryit
function greet(name) {
  return `Hello, ${name}!`;
}

console.log(greet("Mia"));
console.log(greet("Leo"));
```

- `name` is a **parameter**; `"Mia"` is the **argument**.
- `return` sends a value back. A function without `return` gives `undefined`.

## Default parameters

```javascript tryit
function price(amount, tax = 0.2) {
  return amount * (1 + tax);
}
console.log(price(100));
console.log(price(100, 0.05));
```

## Arrow functions

A shorter way to write a function, very common in modern code:

```javascript tryit
const square = (n) => n * n;
const add = (a, b) => {
  const total = a + b;
  return total;
};
console.log(square(7), add(2, 3));
```

With one expression and no braces, the value is returned automatically.

## Functions as values

Functions can be passed to other functions. This is how arrays, events and timers work:

```javascript tryit
function twice(action) {
  action();
  action();
}
twice(() => console.log("Hip hip hooray!"));
```

## Scope

Variables made with `let` or `const` inside `{ }` exist only inside those braces. Keep variables in the smallest scope that works.

## Summary

- `function name(params) { return value; }`
- Arrow functions: `(a, b) => a + b`.
- Functions can be stored and passed like any value.

```exercise
{
  "title": "Area of a rectangle",
  "prompt_md": "Write an arrow function `area` that returns `width * height`. The program then prints `area(4, 5)`, which must show `20`.",
  "starter_code": "const area = \n\nconsole.log(area(4, 5));",
  "solution_code": "const area = (width, height) => width * height;\n\nconsole.log(area(4, 5));",
  "check_type": "output",
  "expected_value": "20",
  "hint": "const area = (width, height) => width * height;"
}
```

```quiz
[
  {"question": "What does a function return without a return statement?", "options": ["undefined", "0", "null"], "answer": 0, "explanation": "Without return, the result is undefined."},
  {"question": "What does (n) => n + 1 do?", "options": ["Returns n plus one", "Prints n", "Nothing until you add return"], "answer": 0, "explanation": "A one-expression arrow function returns that expression."}
]
```
