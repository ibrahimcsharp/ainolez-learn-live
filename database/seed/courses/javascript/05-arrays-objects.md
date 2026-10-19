---
title: Arrays and Objects
slug: arrays-objects
summary: Store lists in arrays, records in objects, and transform data with map, filter and reduce.
minutes: 9
---
## Arrays

```javascript tryit
const colors = ["red", "green", "blue"];
console.log(colors[0], colors.length);

colors.push("yellow");      // add to the end
const last = colors.pop();  // remove from the end
console.log(last, colors);
console.log(colors.includes("green"), colors.indexOf("blue"));
```

## map, filter and reduce

These methods take a function and return something new without changing the array:

```javascript tryit
const prices = [12, 5, 30, 8];

const withTax = prices.map((p) => p * 1.1);
const cheap = prices.filter((p) => p < 10);
const total = prices.reduce((sum, p) => sum + p, 0);

console.log(withTax);
console.log(cheap);
console.log(total);
```

## Objects

An object groups named values (**properties**):

```javascript tryit
const user = {
  name: "Amara",
  age: 21,
  skills: ["HTML", "CSS"],
};

console.log(user.name);
console.log(user["age"]);
user.city = "Lagos";        // add a property
console.log(Object.keys(user));
```

## Arrays of objects

Most data from servers looks like this:

```javascript tryit
const products = [
  { name: "Pen", price: 2 },
  { name: "Backpack", price: 35 },
  { name: "Lamp", price: 25 },
];

const names = products.filter((p) => p.price > 10).map((p) => p.name);
console.log(names);

const sorted = [...products].sort((a, b) => a.price - b.price);
console.log(sorted.map((p) => p.name).join(", "));
```

`[...products]` copies the array, because `sort()` changes the array it is called on.

## Destructuring

```javascript tryit
const { name, price } = { name: "Mug", price: 6 };
const [first, second] = ["gold", "silver", "bronze"];
console.log(name, price, first, second);
```

## Summary

- Arrays: `push`, `pop`, `includes`, `length`.
- `map` transforms, `filter` selects, `reduce` combines.
- Objects hold named properties; destructuring pulls them out.

```exercise
{
  "title": "Total of in-stock items",
  "prompt_md": "Use `filter` and `reduce` to print the total `price` of the items whose `inStock` is `true`. The output must be `27`.",
  "starter_code": "const items = [\n  { name: \"Pen\", price: 2, inStock: true },\n  { name: \"Lamp\", price: 25, inStock: true },\n  { name: \"Desk\", price: 120, inStock: false },\n];\n",
  "solution_code": "const items = [\n  { name: \"Pen\", price: 2, inStock: true },\n  { name: \"Lamp\", price: 25, inStock: true },\n  { name: \"Desk\", price: 120, inStock: false },\n];\nconst total = items.filter((i) => i.inStock).reduce((sum, i) => sum + i.price, 0);\nconsole.log(total);",
  "check_type": "output",
  "expected_value": "27",
  "hint": "items.filter((i) => i.inStock).reduce((sum, i) => sum + i.price, 0)"
}
```

```quiz
[
  {"question": "What does [1, 2, 3].map((n) => n * 2) return?", "options": ["[2, 4, 6]", "[1, 2, 3]", "12"], "answer": 0, "explanation": "map applies the function to every item."},
  {"question": "How do you read the name property of user?", "options": ["user.name", "user->name", "user(name)"], "answer": 0, "explanation": "Dot notation, or user[\"name\"]."}
]
```
