---
title: Graphs
slug: graphs
summary: Represent networks with adjacency lists, explore them with BFS and DFS, and find shortest paths.
minutes: 12
---
## Nodes and edges

A **graph** is a set of **nodes** (vertices) connected by **edges**. Maps, social networks, the web and package dependencies are all graphs.

- **Undirected**: edges go both ways (friendship).
- **Directed**: edges have a direction (following someone, a one-way street).
- **Weighted**: edges have a cost (distance, time).

A tree is a special graph with no cycles.

## Adjacency lists

The usual way to store a graph is a dictionary: each node maps to its neighbours.

```python tryit
friends = {
    "Ana": ["Ben", "Cy"],
    "Ben": ["Ana", "Dee"],
    "Cy":  ["Ana", "Dee"],
    "Dee": ["Ben", "Cy", "Eli"],
    "Eli": ["Dee"],
}
print(friends["Dee"])
print("Ben" in friends["Ana"])
print(sum(len(n) for n in friends.values()) // 2, "friendships")
```

## Breadth-first search (BFS)

BFS explores the closest nodes first, ring by ring, using a queue. In an unweighted graph it finds the path with the **fewest edges**.

```python tryit
from collections import deque

friends = {
    "Ana": ["Ben", "Cy"], "Ben": ["Ana", "Dee"], "Cy": ["Ana", "Dee"],
    "Dee": ["Ben", "Cy", "Eli"], "Eli": ["Dee"],
}

def shortest_path(graph, start, goal):
    came_from = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = came_from[node]
            return path[::-1]
        for neighbour in graph[node]:
            if neighbour not in came_from:     # not visited yet
                came_from[neighbour] = node
                queue.append(neighbour)
    return None

print(shortest_path(friends, "Ana", "Eli"))
```

## Depth-first search (DFS)

DFS goes as deep as possible before backing up. It is written with recursion (or a stack). It is good for "can I reach it?" and for visiting everything.

```python tryit
graph = {
    "A": ["B", "C"], "B": ["D"], "C": ["D", "E"],
    "D": ["F"], "E": ["F"], "F": [],
}

def dfs(node, visited=None):
    if visited is None:
        visited = []
    visited.append(node)
    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs(neighbour, visited)
    return visited

print(dfs("A"))
```

The `visited` check is essential: without it, a cycle would make the search loop forever.

## Weighted graphs: Dijkstra's algorithm

When edges have costs, the path with the fewest edges is not always the cheapest. **Dijkstra's algorithm** always expands the cheapest known node next, using a priority queue.

```python tryit
import heapq

roads = {                       # town: {neighbour: km}
    "A": {"B": 4, "C": 1},
    "B": {"D": 1},
    "C": {"B": 2, "D": 5},
    "D": {},
}

def dijkstra(graph, start):
    distance = {start: 0}
    queue = [(0, start)]
    while queue:
        dist, node = heapq.heappop(queue)
        if dist > distance[node]:
            continue            # an older, longer entry
        for neighbour, km in graph[node].items():
            new = dist + km
            if new < distance.get(neighbour, float("inf")):
                distance[neighbour] = new
                heapq.heappush(queue, (new, neighbour))
    return distance

print(dijkstra(roads, "A"))     # A->C->B->D = 4 km, not A->B->D = 5
```

## Summary

- Graphs are nodes and edges; store them as adjacency lists (a dict of lists).
- BFS (queue) finds the fewest-edges path; DFS (recursion) goes deep first.
- Always track visited nodes; Dijkstra finds the cheapest path in weighted graphs.

```exercise
{
  "title": "Who can I reach?",
  "prompt_md": "Use BFS or DFS to collect every node reachable from `\"home\"` (including `home`). Print them sorted. The output must be `['bank', 'cafe', 'home', 'park']` - `zoo` cannot be reached.",
  "starter_code": "streets = {\n    \"home\": [\"cafe\", \"park\"],\n    \"cafe\": [\"bank\"],\n    \"park\": [\"home\"],\n    \"bank\": [],\n    \"zoo\": [\"home\"],\n}\n",
  "solution_code": "streets = {\n    \"home\": [\"cafe\", \"park\"],\n    \"cafe\": [\"bank\"],\n    \"park\": [\"home\"],\n    \"bank\": [],\n    \"zoo\": [\"home\"],\n}\nseen = {\"home\"}\nto_visit = [\"home\"]\nwhile to_visit:\n    place = to_visit.pop()\n    for nxt in streets[place]:\n        if nxt not in seen:\n            seen.add(nxt)\n            to_visit.append(nxt)\nprint(sorted(seen))",
  "check_type": "output",
  "expected_value": "['bank', 'cafe', 'home', 'park']",
  "hint": "Keep a set of seen places and a list to visit. Pop a place, add its unseen neighbours to both."
}
```

```quiz
[
  {"question": "How is a graph usually stored in Python?", "options": ["A dict of neighbour lists", "One long string", "A sorted list"], "answer": 0, "explanation": "Adjacency lists map each node to its neighbours."},
  {"question": "Which search finds the path with the fewest edges?", "options": ["DFS", "BFS"], "answer": 1, "explanation": "BFS explores ring by ring from the start."},
  {"question": "Why keep track of visited nodes?", "options": ["To save memory", "So cycles don't cause endless loops", "To sort the nodes"], "answer": 1, "explanation": "Without it the search could go round a cycle forever."}
]
```
