---
title: Binary Search Trees
slug: binary-search-trees
summary: Keep values ordered in a tree for fast search, insert and min/max - and why balance matters.
minutes: 10
---
## The BST rule

A **binary search tree** (BST) is a binary tree with one rule for every node:

- everything in its **left** subtree is **smaller**,
- everything in its **right** subtree is **larger**.

```text
         50
       /    \
     30      70
    /  \    /  \
   20  40  60  80
```

To find 60: 60 > 50, go right; 60 < 70, go left; found. Each step throws away half of what is left.

## Insert and search

```python tryit
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(node, value):
    if node is None:
        return Node(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node                  # duplicates are ignored

def contains(node, value):
    while node:
        if value == node.value:
            return True
        node = node.left if value < node.value else node.right
    return False

root = None
for v in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, v)
print(contains(root, 60), contains(root, 65))
```

## In-order gives sorted values

Because smaller values are always on the left, an in-order traversal returns the values in sorted order.

```python tryit
class Node:
    def __init__(self, value):
        self.value, self.left, self.right = value, None, None

def insert(node, value):
    if node is None:
        return Node(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node

def in_order(node):
    if node:
        yield from in_order(node.left)
        yield node.value
        yield from in_order(node.right)

def smallest(node):
    while node.left:
        node = node.left
    return node.value

root = None
for v in [42, 17, 88, 5, 23, 61, 99]:
    root = insert(root, v)
print(list(in_order(root)))
print("min:", smallest(root))
```

## Balance matters

Search is O(log n) **only if the tree is balanced**. Insert values that are already sorted and every node goes to the right - the tree becomes a long chain, and search becomes O(n).

```python tryit
class Node:
    def __init__(self, value):
        self.value, self.left, self.right = value, None, None

def insert(node, value):
    if node is None:
        return Node(value)
    if value < node.value:
        node.left = insert(node.left, value)
    else:
        node.right = insert(node.right, value)
    return node

def height(node):
    return -1 if node is None else 1 + max(height(node.left), height(node.right))

mixed = None
for v in [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]:
    mixed = insert(mixed, v)
in_order = None
for v in range(1, 16):
    in_order = insert(in_order, v)
print("mixed order height:", height(mixed))
print("sorted order height:", height(in_order))
```

**Self-balancing** trees such as **AVL trees** and **red-black trees** rotate nodes after each insert to keep the height close to log n. Databases use a related structure, the B-tree, for their indexes.

## Summary

- In a BST, left is smaller and right is larger at every node.
- Search and insert follow one path down: O(log n) when balanced, O(n) when not.
- In-order traversal of a BST gives the values sorted.

```exercise
{
  "title": "Largest value",
  "prompt_md": "Write `largest(node)` that walks right until there is no right child, and returns that value. Print it for the tree built below. The output must be `93`.",
  "starter_code": "class Node:\n    def __init__(self, value):\n        self.value, self.left, self.right = value, None, None\n\ndef insert(node, value):\n    if node is None:\n        return Node(value)\n    if value < node.value:\n        node.left = insert(node.left, value)\n    else:\n        node.right = insert(node.right, value)\n    return node\n\nroot = None\nfor v in [41, 20, 65, 11, 29, 50, 93, 72]:\n    root = insert(root, v)\n",
  "solution_code": "class Node:\n    def __init__(self, value):\n        self.value, self.left, self.right = value, None, None\n\ndef insert(node, value):\n    if node is None:\n        return Node(value)\n    if value < node.value:\n        node.left = insert(node.left, value)\n    else:\n        node.right = insert(node.right, value)\n    return node\n\nroot = None\nfor v in [41, 20, 65, 11, 29, 50, 93, 72]:\n    root = insert(root, v)\n\ndef largest(node):\n    while node.right:\n        node = node.right\n    return node.value\n\nprint(largest(root))",
  "check_type": "output",
  "expected_value": "93",
  "hint": "while node.right: node = node.right, then return node.value."
}
```

```quiz
[
  {"question": "In a BST, where are smaller values?", "options": ["In the left subtree", "In the right subtree", "Anywhere"], "answer": 0, "explanation": "Left is smaller, right is larger."},
  {"question": "What does an in-order traversal of a BST give?", "options": ["Random order", "Sorted order", "Reverse insertion order"], "answer": 1, "explanation": "Left, node, right visits values from small to large."},
  {"question": "Inserting 1, 2, 3, 4, 5 in order makes search...", "options": ["O(log n)", "O(n)", "O(1)"], "answer": 1, "explanation": "The tree becomes a chain."}
]
```
