---
title: Trees and Binary Trees
slug: trees
summary: Tree vocabulary, binary tree nodes, recursion, and the four ways to traverse a tree.
minutes: 11
---
## What is a tree?

A **tree** stores data in a hierarchy, like a family tree or the folders on your computer.

```text
          A          <- root
        /   \
       B     C
      / \     \
     D   E     F     <- leaves
```

- The top node is the **root**; nodes without children are **leaves**.
- Every node except the root has exactly one **parent**.
- The **height** is the number of levels below the root (here 2).

In a **binary tree** every node has at most two children: **left** and **right**.

## A binary tree in Python

```python tryit
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

root = TreeNode("A",
    TreeNode("B", TreeNode("D"), TreeNode("E")),
    TreeNode("C", None, TreeNode("F")),
)
print(root.value, root.left.value, root.right.right.value)
```

## Recursion fits trees

Each child is the root of a smaller tree, so tree code is naturally **recursive**: a function calls itself on the children.

```python tryit
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right

def count(node):
    if node is None:
        return 0
    return 1 + count(node.left) + count(node.right)

def height(node):
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))

root = TreeNode("A", TreeNode("B", TreeNode("D"), TreeNode("E")), TreeNode("C", None, TreeNode("F")))
print(count(root), "nodes, height", height(root))
```

The `if node is None` line is the **base case** that stops the recursion.

## Depth-first traversals

To *traverse* is to visit every node. The three depth-first orders differ only in when you visit the node itself:

```python tryit
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right

def pre_order(node):      # node, left, right
    if node:
        yield node.value
        yield from pre_order(node.left)
        yield from pre_order(node.right)

def in_order(node):       # left, node, right
    if node:
        yield from in_order(node.left)
        yield node.value
        yield from in_order(node.right)

def post_order(node):     # left, right, node
    if node:
        yield from post_order(node.left)
        yield from post_order(node.right)
        yield node.value

root = TreeNode("A", TreeNode("B", TreeNode("D"), TreeNode("E")), TreeNode("C", None, TreeNode("F")))
print("pre: ", list(pre_order(root)))
print("in:  ", list(in_order(root)))
print("post:", list(post_order(root)))
```

## Breadth-first (level order)

Visit the tree level by level with a queue.

```python tryit
from collections import deque

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right

def level_order(root):
    queue = deque([root])
    while queue:
        node = queue.popleft()
        yield node.value
        for child in (node.left, node.right):
            if child:
                queue.append(child)

root = TreeNode("A", TreeNode("B", TreeNode("D"), TreeNode("E")), TreeNode("C", None, TreeNode("F")))
print(list(level_order(root)))
```

## Summary

- A tree has a root, parents, children and leaves; a binary tree has at most two children per node.
- Tree functions are usually recursive, with `None` as the base case.
- Pre-, in- and post-order are depth-first; level order uses a queue.

```exercise
{
  "title": "Sum of the tree",
  "prompt_md": "Write a recursive function `tree_sum(node)` that returns the sum of all values (0 for `None`). Print the sum for the tree below. The output must be `28`.",
  "starter_code": "class TreeNode:\n    def __init__(self, value, left=None, right=None):\n        self.value, self.left, self.right = value, left, right\n\nroot = TreeNode(7, TreeNode(3, TreeNode(1), TreeNode(5)), TreeNode(9, None, TreeNode(3)))\n",
  "solution_code": "class TreeNode:\n    def __init__(self, value, left=None, right=None):\n        self.value, self.left, self.right = value, left, right\n\nroot = TreeNode(7, TreeNode(3, TreeNode(1), TreeNode(5)), TreeNode(9, None, TreeNode(3)))\n\ndef tree_sum(node):\n    if node is None:\n        return 0\n    return node.value + tree_sum(node.left) + tree_sum(node.right)\n\nprint(tree_sum(root))",
  "check_type": "output",
  "expected_value": "28",
  "hint": "Base case: return 0 for None. Otherwise return node.value + tree_sum(left) + tree_sum(right)."
}
```

```quiz
[
  {"question": "What is a leaf?", "options": ["The top node", "A node with no children", "A node with two children"], "answer": 1, "explanation": "Leaves are at the bottom of the tree."},
  {"question": "In-order traversal visits...", "options": ["node, left, right", "left, node, right", "left, right, node"], "answer": 1, "explanation": "In-order puts the node in the middle."},
  {"question": "Which structure does level-order traversal use?", "options": ["a stack", "a queue", "a hash table"], "answer": 1, "explanation": "A queue visits nodes level by level."}
]
```
