---
title: Python Lambda and Functions as Values
slug: lambda
summary: Write small one-line lambda functions, pass functions to other functions, and build functions that return new functions.
minutes: 11
---
## Functions are values

In Python a function is an object, just like a number or a list. You can store it in a variable, put it in a list, pass it to another function and return it from one.

```python tryit
def shout(text):
    return text.upper() + "!"

say = shout             # no brackets: the function itself, not a call
print(say("hello"))

for action in [str.lower, str.upper, shout]:
    print(action("Mixed Case"))
```

## lambda: a function in one expression

`lambda parameters: expression` makes a small function with no name. It returns the value of the expression automatically; there is no `return` keyword.

```python tryit
half = lambda n: n / 2
area = lambda width, height: width * height

print(half(9))
print(area(3, 4))
```

A lambda can hold only **one expression**: no loops, no `if` statements (a one-line `x if test else y` is fine), no assignments. For anything longer, use `def`.

## Where lambda shines: as an argument

Lambdas are most useful when a function asks for another function, such as the `key` of `sorted()`, `min()` and `max()`.

```python tryit
planets = [("Mars", 6779), ("Venus", 12104), ("Mercury", 4879), ("Earth", 12742)]

by_size = sorted(planets, key=lambda planet: planet[1])
print([name for name, size in by_size])

biggest = max(planets, key=lambda planet: planet[1])
print("biggest:", biggest[0])

by_name_length = sorted(planets, key=lambda planet: len(planet[0]))
print([name for name, size in by_name_length])
```

## map and filter

`map(function, items)` calls the function on every item. `filter(function, items)` keeps the items for which the function returns `True`. Both give an iterator, so wrap them in `list()` to see the result.

```python tryit
temps_c = [12, 25, 31, 18, 7]

temps_f = list(map(lambda c: round(c * 9 / 5 + 32), temps_c))
print(temps_f)

warm = list(filter(lambda c: c >= 20, temps_c))
print(warm)
```

The same results with comprehensions, which many Python programmers find easier to read:

```python tryit
temps_c = [12, 25, 31, 18, 7]
print([round(c * 9 / 5 + 32) for c in temps_c])
print([c for c in temps_c if c >= 20])
```

## Writing a function that takes a function

```python tryit
def apply_to_all(func, items):
    return [func(item) for item in items]

print(apply_to_all(len, ["sun", "moon", "galaxy"]))
print(apply_to_all(lambda x: x * 10, [1, 2, 3]))
```

## Functions that build functions

A function can create and return a new function. The new function remembers the values from the place where it was made; this is called a **closure**.

```python tryit
def make_discount(percent):
    def apply(price):
        return round(price * (100 - percent) / 100, 2)
    return apply

summer_sale = make_discount(20)
staff_price = make_discount(35)

print(summer_sale(50))    # 40.0
print(staff_price(50))    # 32.5
```

The same factory can return a lambda:

```python tryit
def make_greeting(word):
    return lambda name: f"{word}, {name}!"

hello = make_greeting("Hello")
hola = make_greeting("Hola")
print(hello("Ravi"), hola("Ravi"))
```

## Summary

- Functions are values: store them, pass them, return them.
- `lambda x: expression` is a short, nameless function with a single expression.
- Use lambdas for `key=` in `sorted`, `min` and `max`, and with `map` and `filter`.
- A function returned from another function remembers its surroundings (a closure).

```exercise
{
  "title": "Sort by the last letter",
  "prompt_md": "Sort `words` by their **last** letter using `sorted()` with a lambda as the `key`, and print the list. The output must be `['apple', 'fig', 'lemon', 'cherry']`.",
  "starter_code": "words = [\"cherry\", \"apple\", \"lemon\", \"fig\"]\n",
  "solution_code": "words = [\"cherry\", \"apple\", \"lemon\", \"fig\"]\nprint(sorted(words, key=lambda word: word[-1]))",
  "check_type": "output",
  "expected_value": "['apple', 'fig', 'lemon', 'cherry']",
  "hint": "word[-1] is the last letter: key=lambda word: word[-1]"
}
```

```exercise
{
  "title": "A tax calculator factory",
  "prompt_md": "Write `make_tax(rate)` that returns a function. The returned function takes a price and returns the price plus `rate` percent tax, rounded to 2 decimals. The code below must print `121.0 107.5`.",
  "starter_code": "def make_tax(rate):\n    pass\n\nvat = make_tax(21)\nlow = make_tax(7.5)\nprint(vat(100), low(100))",
  "solution_code": "def make_tax(rate):\n    return lambda price: round(price * (1 + rate / 100), 2)\n\nvat = make_tax(21)\nlow = make_tax(7.5)\nprint(vat(100), low(100))",
  "check_type": "output",
  "expected_value": "121.0 107.5",
  "hint": "return lambda price: round(price * (1 + rate / 100), 2)"
}
```

```quiz
[
  {"question": "What does (lambda a, b: a - b)(10, 4) give?", "options": ["14", "6", "an error"], "answer": 1, "explanation": "The lambda is called straight away with a=10 and b=4."},
  {"question": "Which of these can a lambda NOT contain?", "options": ["a comparison", "a for loop statement", "a function call"], "answer": 1, "explanation": "A lambda holds one expression; statements like for and while are not allowed."},
  {"question": "What does filter(lambda n: n > 2, [1, 2, 3, 4]) keep?", "options": ["[1, 2]", "[3, 4]", "[True, True]"], "answer": 1, "explanation": "filter keeps the items for which the function returns True."}
]
```
