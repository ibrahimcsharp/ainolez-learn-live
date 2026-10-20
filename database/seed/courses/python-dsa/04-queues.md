---
title: Queues
slug: queues
summary: First in, first out - queues with deque, a queue class, and priority queues with heapq.
minutes: 8
---
## First in, first out

A **queue** works like a line at a shop: people join at the back and are served from the front. The first one in is the first one out (**FIFO**).

| Operation | Meaning |
|---|---|
| `enqueue(x)` | join at the back |
| `dequeue()` | remove and return the front item |
| `peek()` | look at the front item |

## Don't use a list

`list.pop(0)` moves every other item, so it is O(n). `collections.deque` removes from the front in O(1).

```python tryit
from collections import deque

line = deque()
line.append("Ana")     # enqueue
line.append("Ben")
line.append("Cy")
print(line.popleft())  # dequeue: Ana
print(line[0])         # peek: Ben
print(list(line))
```

## A Queue class

```python tryit
from collections import deque

class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if not self._items:
            raise IndexError("dequeue from an empty queue")
        return self._items.popleft()

    def peek(self):
        return self._items[0]

    def __len__(self):
        return len(self._items)

printer = Queue()
for doc in ["report.pdf", "photo.png", "notes.txt"]:
    printer.enqueue(doc)
while len(printer):
    print("printing", printer.dequeue())
```

## Use: taking turns

A queue is perfect for round-robin: each task gets a turn, then goes to the back if it is not finished.

```python tryit
from collections import deque

tasks = deque([("download", 3), ("email", 1), ("backup", 2)])   # (name, steps left)
while tasks:
    name, left = tasks.popleft()
    print("working on", name)
    if left > 1:
        tasks.append((name, left - 1))
```

## Priority queues

Sometimes the most important item should go first, not the oldest. A **priority queue** always hands out the smallest item. Python's `heapq` module keeps a list arranged as a *heap*, so adding and removing are O(log n).

```python tryit
import heapq

er = []                                   # emergency room
heapq.heappush(er, (3, "sprained ankle"))
heapq.heappush(er, (1, "heart attack"))
heapq.heappush(er, (2, "broken arm"))

while er:
    priority, patient = heapq.heappop(er)
    print(priority, patient)

print(heapq.nsmallest(2, [40, 10, 30, 20]))
```

Tuples compare by their first item, so `(priority, name)` sorts by priority.

## Summary

- A queue is first in, first out.
- Use `collections.deque` with `append()` and `popleft()` - both O(1).
- `heapq` gives a priority queue where the smallest item comes out first.

```exercise
{
  "title": "Hot potato",
  "prompt_md": "Players stand in a queue. Each round, move the front player to the back 2 times, then remove the front player. Repeat until one player is left and print the winner. The output must be `Di`.",
  "starter_code": "from collections import deque\n\nplayers = deque([\"Al\", \"Bo\", \"Cy\", \"Di\", \"Ed\"])\n",
  "solution_code": "from collections import deque\n\nplayers = deque([\"Al\", \"Bo\", \"Cy\", \"Di\", \"Ed\"])\nwhile len(players) > 1:\n    for _ in range(2):\n        players.append(players.popleft())\n    players.popleft()\nprint(players[0])",
  "check_type": "output",
  "expected_value": "Di",
  "hint": "Inside while len(players) > 1: do players.append(players.popleft()) twice, then players.popleft()."
}
```

```quiz
[
  {"question": "Which item leaves a queue first?", "options": ["The newest", "The oldest", "The biggest"], "answer": 1, "explanation": "Queues are first in, first out."},
  {"question": "Why use deque instead of a list for a queue?", "options": ["popleft() is O(1)", "It sorts items", "It uses no memory"], "answer": 0, "explanation": "list.pop(0) is O(n)."},
  {"question": "What does heapq.heappop() return?", "options": ["The newest item", "The smallest item", "The largest item"], "answer": 1, "explanation": "heapq is a min-heap."}
]
```
