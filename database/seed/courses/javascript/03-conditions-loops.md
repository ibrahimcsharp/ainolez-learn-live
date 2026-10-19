---
title: Conditions and Loops
slug: conditions-loops
summary: Make decisions with if, else and the ternary operator, and repeat with for and while.
minutes: 8
---
## if, else if, else

```javascript tryit
const temperature = 24;

if (temperature > 30) {
  console.log("Hot");
} else if (temperature > 15) {
  console.log("Pleasant");
} else {
  console.log("Cold");
}
```

Combine conditions with `&&` (and), `||` (or) and `!` (not).

## The ternary operator

A short `if` that gives a value:

```javascript tryit
const age = 17;
const status = age >= 18 ? "adult" : "minor";
console.log(status);
```

## Truthy and falsy

`0`, `""`, `null`, `undefined`, `NaN` and `false` count as **false** in a condition. Everything else counts as true.

## for loops

```javascript tryit
for (let i = 1; i <= 5; i++) {
  console.log(`Step ${i}`);
}

const fruits = ["apple", "banana", "cherry"];
for (const fruit of fruits) {
  console.log(fruit);
}
```

The classic `for` has three parts: start (`let i = 1`), condition (`i <= 5`) and step (`i++`). `for...of` walks through the items of an array.

## while

```javascript tryit
let coins = 1;
while (coins < 100) {
  coins = coins * 2;
}
console.log(coins);
```

`break` leaves a loop; `continue` skips to the next round.

## Summary

- `if / else if / else` choose what runs.
- `condition ? a : b` picks a value.
- `for`, `for...of` and `while` repeat code.

```exercise
{
  "title": "FizzBuzz to 5",
  "prompt_md": "For the numbers 1 to 5, print `Fizz` when the number is divisible by 3, otherwise print the number.",
  "starter_code": "for (let i = 1; i <= 5; i++) {\n  \n}",
  "solution_code": "for (let i = 1; i <= 5; i++) {\n  console.log(i % 3 === 0 ? \"Fizz\" : i);\n}",
  "check_type": "output",
  "expected_value": "1\n2\nFizz\n4\n5",
  "hint": "i % 3 === 0 is true when i divides by 3."
}
```

```quiz
[
  {"question": "What does age >= 18 ? \"yes\" : \"no\" give when age is 20?", "options": ["\"yes\"", "\"no\"", "true"], "answer": 0, "explanation": "The condition is true, so the first value is used."},
  {"question": "Which value is falsy?", "options": ["0", "\"0\"", "[]"], "answer": 0, "explanation": "The number 0 is falsy; the string \"0\" and an empty array are truthy."}
]
```
