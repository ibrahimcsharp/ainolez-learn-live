---
title: Stacks
slug: stacks
summary: Last in, first out - build a stack, then use it to undo actions and check brackets.
minutes: 8
---
## Last in, first out

A **stack** works like a pile of plates: you add to the top and take from the top. The last item in is the first one out (**LIFO**).

| Operation | Meaning |
|---|---|
| `push(x)` | put `x` on top |
| `pop()` | remove and return the top item |
| `peek()` | look at the top item without removing it |
| `is_empty()` | is the stack empty? |

All of them are O(1).

## A list is already a stack

`append()` and `pop()` work at the end of a list, which is fast.

```python tryit
stack = []
stack.append("a")
stack.append("b")
stack.append("c")
print(stack.pop())   # c - the last one in
print(stack[-1])     # b - peek
print(stack)
```

## A Stack class

Wrapping the list in a class gives clear names and stops misuse, such as inserting in the middle.

```python tryit
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)

s = Stack()
for word in ["one", "two", "three"]:
    s.push(word)
print(len(s), s.peek())
while not s.is_empty():
    print(s.pop())
```

## Use 1: undo

Editors keep your actions on a stack. *Undo* pops the latest one.

```python tryit
text = ""
history = []

for word in ["Hello", " big", " world"]:
    history.append(text)    # save the state before the change
    text += word
print(text)

text = history.pop()        # undo
print(text)
text = history.pop()        # undo again
print(text)
```

## Use 2: balanced brackets

Every opening bracket must be closed in the right order. Push openers; when a closer arrives, it must match the top of the stack.

```python tryit
def balanced(code):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in code:
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack

for code in ["(a[0] + b) * {c}", "(]", "((x)", "print(len([1, 2]))"]:
    print(f"{code:<20} {balanced(code)}")
```

Stacks are also how Python keeps track of function calls: each call is pushed onto the *call stack* and popped when it returns.

## Summary

- A stack is last in, first out; push, pop and peek are O(1).
- A Python list with `append()` and `pop()` is a stack.
- Stacks power undo, bracket checking and function calls.

```exercise
{
  "title": "Reverse a word",
  "prompt_md": "Push every letter of `word` onto a stack (a list), then pop them all off to build the reversed word. Print it. The output must be `nohtyp`.",
  "starter_code": "word = \"python\"\nstack = []\n",
  "solution_code": "word = \"python\"\nstack = []\nfor letter in word:\n    stack.append(letter)\nreversed_word = \"\"\nwhile stack:\n    reversed_word += stack.pop()\nprint(reversed_word)",
  "check_type": "output",
  "expected_value": "nohtyp",
  "hint": "Use append() for each letter, then while stack: add stack.pop() to a new string."
}
```

```quiz
[
  {"question": "Which item does pop() take from a stack?", "options": ["The first one added", "The last one added", "A random one"], "answer": 1, "explanation": "Stacks are last in, first out."},
  {"question": "Which list methods make a fast stack?", "options": ["insert(0, x) and pop(0)", "append(x) and pop()", "add(x) and remove(x)"], "answer": 1, "explanation": "Both work at the end of the list in O(1)."},
  {"question": "Is \"([)]\" balanced?", "options": ["Yes", "No"], "answer": 1, "explanation": "The ) arrives while [ is on top of the stack."}
]
```
