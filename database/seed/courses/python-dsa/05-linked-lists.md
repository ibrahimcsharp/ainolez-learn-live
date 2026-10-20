---
title: Linked Lists
slug: linked-lists
summary: Build a linked list from nodes, add and remove items, and reverse it.
minutes: 11
---
## Nodes and links

A **linked list** is a chain of **nodes**. Each node holds a value and a link (`next`) to the following node. The list only remembers the first node, the **head**.

```text
head
 |
[7 | •]--> [3 | •]--> [9 | None]
```

Unlike an array, nodes do not sit next to each other in memory, so there is no jumping to an index - but adding at the front never moves other items.

## The Node class

```python tryit
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

third = Node(9)
second = Node(3, third)
head = Node(7, second)

node = head
while node is not None:     # walk the chain
    print(node.value)
    node = node.next
```

## A LinkedList class

```python tryit
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def push_front(self, value):          # O(1)
        self.head = Node(value, self.head)
        self.size += 1

    def append(self, value):              # O(n): walk to the end
        new = Node(value)
        if self.head is None:
            self.head = new
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new
        self.size += 1

    def __iter__(self):
        node = self.head
        while node:
            yield node.value
            node = node.next

    def __str__(self):
        return " -> ".join(str(v) for v in self) or "(empty)"

items = LinkedList()
items.append(3)
items.append(9)
items.push_front(7)
print(items, "size", items.size)
```

## Removing a node

To remove a node, make the previous node skip over it.

```python tryit
class Node:
    def __init__(self, value, next=None):
        self.value, self.next = value, next

def remove(head, value):
    """Return the new head after removing the first node with this value."""
    if head is None:
        return None
    if head.value == value:
        return head.next
    node = head
    while node.next and node.next.value != value:
        node = node.next
    if node.next:
        node.next = node.next.next     # skip it
    return head

def show(head):
    out = []
    while head:
        out.append(head.value)
        head = head.next
    print(out)

head = Node(1, Node(2, Node(3, Node(4))))
head = remove(head, 3)
show(head)
head = remove(head, 1)
show(head)
```

## Reversing a linked list

A classic interview question: turn every arrow around, in one pass.

```python tryit
class Node:
    def __init__(self, value, next=None):
        self.value, self.next = value, next

def reverse(head):
    previous = None
    while head:
        following = head.next   # remember the rest
        head.next = previous    # turn the arrow around
        previous = head
        head = following
    return previous

head = reverse(Node(1, Node(2, Node(3))))
while head:
    print(head.value, end=" ")
    head = head.next
```

## Arrays vs linked lists

| | List (array) | Linked list |
|---|---|---|
| Read item `i` | O(1) | O(n) |
| Add / remove at the front | O(n) | O(1) |
| Add at the end | O(1) | O(n), or O(1) with a tail link |
| Memory | compact | a link per node |

In everyday Python a list or `deque` is usually the better choice, but linked structures are the basis of trees and graphs.

## Summary

- A linked list is a chain of nodes; each node has a value and `next`.
- Adding at the front is O(1); finding an item is O(n).
- Removing means re-linking the previous node; reversing turns every link around.

```exercise
{
  "title": "Sum a linked list",
  "prompt_md": "Walk the linked list from `head` and print the sum of all values. The output must be `30`.",
  "starter_code": "class Node:\n    def __init__(self, value, next=None):\n        self.value = value\n        self.next = next\n\nhead = Node(5, Node(10, Node(15)))\n",
  "solution_code": "class Node:\n    def __init__(self, value, next=None):\n        self.value = value\n        self.next = next\n\nhead = Node(5, Node(10, Node(15)))\ntotal = 0\nnode = head\nwhile node is not None:\n    total += node.value\n    node = node.next\nprint(total)",
  "check_type": "output",
  "expected_value": "30",
  "hint": "Start with node = head; in a while loop add node.value and move with node = node.next."
}
```

```quiz
[
  {"question": "What does each node store?", "options": ["A value and a link to the next node", "Only an index", "The whole list"], "answer": 0, "explanation": "Nodes hold a value and next."},
  {"question": "What is the Big O of adding at the front of a linked list?", "options": ["O(1)", "O(n)", "O(log n)"], "answer": 0, "explanation": "Only the head changes."},
  {"question": "What is the Big O of reading the 500th item?", "options": ["O(1)", "O(n)"], "answer": 1, "explanation": "You have to walk node by node."}
]
```
