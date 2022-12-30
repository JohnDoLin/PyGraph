# PyGraph
> “If you know your graph and know yourself, you need not fear the result of a hunndred exams.”
>
> <cite>― Sun Tzu, The Art of War</cite>

## How to Run
1. Run ```pip install -r requirements.txt```
2. Run ```python main.py```

## Features 
### Info
Shows basic properties of the graph

### Queires
You may clear highlights, highlight shortest path, or even run Dijkstra animation on the graph!

### Style
Right click on a node or edge and you can modify its radius, color, border width/color, text, or thickness.

### Graph Generator
We offer 4 types of common graphs:
- Star Graph
- Grid Lattice
- Cubical
- Random Tree
which can be be composed with the current graph owned, or replace with the graph.

### Control
You may adjust 4 constants that determine the force between nodes, the higher the greater the force:
- c1: Govern the attraction force between any two nodes
- c2: Relativity constant 
- c3: Repulsion between any two nodes
- c4: Additional attraction Force between nodes connected with edge

The formula for the forces are as follows:
- Attraction: c1 * log(d / c2)
- Repulsion: c3 / d\*\*2
- Edge Attraction: c4 * log(d / c2)
where d stands for the distance between the two nodes.

### Terminal
You may run custom python script, debug, or do more with your creativity and imagination!

## How to Interact
- Drag nodes and pan the whole graph with your mouse!
- Zoom in and out with your wheel!
- Ctrl + Left click adds a new node
- Ctrl + Shift + Left click removes a node
- Alt + Drag adds a new edge
- Ctrl + Shift + Drag removes an edge

