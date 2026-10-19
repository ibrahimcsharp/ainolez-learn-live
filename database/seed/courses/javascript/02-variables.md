---
title: Variables and Types
slug: variables
summary: Store values with let and const, and work with numbers, strings and booleans.
minutes: 7
---
## let and const

```javascript tryit
const name = "Amara";   // const: cannot be reassigned
let score = 10;         // let: can change
score = score + 5;
console.log(name, score);
```

Use `const` by default and `let` when the value must change. Old code uses `var`; avoid it in new code.

## Types

| Type | Example |
|------|---------|
| number | `42`, `3.14` |
| string | `"text"`, `'text'` |
| boolean | `true`, `false` |
| undefined | a variable with no value yet |
| null | "no value", set on purpose |
| object / array | `{ a: 1 }`, `[1, 2]` |

```javascript tryit
console.log(typeof 42);
console.log(typeof "hi");
console.log(typeof true);
let empty;
console.log(empty);
```

## Strings and template literals

Backticks make a **template literal**: put values inside with `${...}`.

```javascript tryit
const item = "coffee";
const price = 3.5;
console.log(`One ${item} costs $${price}.`);
console.log(item.toUpperCase(), item.length);
console.log("ice " + item);
```

## Watch out: + with strings

```javascript tryit
console.log(1 + 2);       // 3
console.log("1" + 2);     // "12": the number becomes text
console.log(Number("1") + 2);
console.log(1 === 1, 1 === "1");   // === checks value and type
```

Always compare with `===` and `!==`. The loose `==` converts types and gives surprising results.

## Summary

- `const` for values that stay, `let` for values that change.
- Template literals: `` `Hi ${name}` ``.
- Compare with `===`.

```exercise
{
  "title": "A greeting",
  "prompt_md": "Use a template literal to print `Hi Leo, you are 12` using the variables `name` and `age`.",
  "starter_code": "const name = \"Leo\";\nconst age = 12;\n",
  "solution_code": "const name = \"Leo\";\nconst age = 12;\nconsole.log(`Hi ${name}, you are ${age}`);",
  "check_type": "output",
  "expected_value": "Hi Leo, you are 12",
  "hint": "console.log(`Hi ${name}, you are ${age}`);"
}
```

```quiz
[
  {"question": "Which keyword makes a variable that cannot be reassigned?", "options": ["const", "let", "var"], "answer": 0, "explanation": "const cannot be reassigned."},
  {"question": "What is \"5\" + 1 in JavaScript?", "options": ["\"51\"", "6", "An error"], "answer": 0, "explanation": "With a string, + joins text."}
]
```
