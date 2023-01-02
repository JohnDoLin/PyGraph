# API Reference
The following are API we implemented.

## Editors

``` python
ed_reg.add_editor(window: str = *window*, graph: nx.Graph = *graph*)
```
Create a new editor (This is not recommended to use since we don't support multiple graoh views).

Returns an editor object and add into ```ed_reg```, the EditorRegistor object created in main.py.

``` python
ed.clear()
```

Delete all nodes in the editors.

``` python
ed.set_camera(scale: float, offset: list(2))
```

Set the scale and camera offset for the graph viewing window.


## Modify the Graph Directly

You may directly modify the graph in the editor, however, id, style and other informations are not stored in the graph, and thus modifying the graph can only affect the structure, not any other things. 

## Node
The information of a node is stored in ```ed.node_dict[node]```


```python 
ed.add_node(node: any = None, pos: list(2) = [0, 0], **kargs)
```

Add node in an editor. 

If the parameter ```node``` is number 0, the node id is set to ```"0"```, and if it is ```None``` we will generate a random uuid for it. Note that the uuid is a string consisting of 8 numbers.



```python 
ed.delete_node(node: any = None)
```

Delete the node of node id ```node``` from the editor and the graph.


``` python
ed.set_node(node: any, **kargs)
```

Set the node ```node``` in the editor according to ```kargs```.

```python
ed.node_dict[node].set_style(**kargs)
```

Set the style of the node ```node``` in the editor according to ```kargs```. This is equivalent to use ```ed.set_node(node, style[key] = value)```

## Edge
The information of an edge is stored in ```ed.edge_dict[frozenset({node1, node2})]```


```python 
ed.add_node(node1: any, node2: any, **kargs)
```

Add the edge from ```node1``` to ```node2``` in the editor. If the edge has already been created, the command is simply ignored. If any one of the nodes does not exist, the command also creates them.

```python 
ed.delete_node(np: frozenset(2))
```

Delete the edge ```np``` from the editor and the graph, where np is of the form ```frozenset({node1, node2})```.

``` python
ed.set_edge(np: frozenset(2), **kargs)
```

Set the edge ```np``` in the editor according to ```kargs```.

```python
ed.edge_dict[frozenset({node1, node2})].set_style(**kargs)
```

Set the style of the edge ```frozenset({node1, node2})``` in the editor according to ```kargs```. This is equivalent to use ```ed.set_edge(frozenset({node1, node2}), style[key] = value)```

## Algorithms
```python
alg.hl_node(ed, nodes: any, hl: tuple = node_dfhl)
```

Highlight the node(s) with color ```hl```. If ```nodes``` is a list it will iterate thorugh all of them.

```python
alg.hl_edge(ed, edges: any, hl: tuple = edge_dfhl)
```

Highlight the edge(s) with color ```hl```. If ```edges``` is a list it will iterate thorugh all of them.

```python
alg.reset_node(ed, *args)
```

Reset the style of nodes in ```args```. If ```args``` is not specified it will reset all nodes.

```python
alg.reset_edge(ed, *args)
```

Reset the style of edges in ```args```. If ```args``` is not specified it will reset all edges.

```python
alg.reset_all(ed)
```

Reset the style of nodes and edges in the editor ```ed```.

```python
alg.dfs_tree_animation(ed, source, visited = set())
```

Run the DFS algorithm animation of a tree. 

```python
alg.dijkstra_animation(ed, source, target)
```

Run the Dijkstra algorithm animation. 



## Examples

### Coloring Nodes
```python 
for node in main_ed.node_dict:
  neighbors = main_ed.graph[node]
  if len(neighbors) == 4:
    main_ed.node_dict[node].set_style(color=(255, 0, 0))
  elif len(neighbors) == 3:
    main_ed.node_dict[node].set_style(color=(0, 0, 255))
  elif len(neighbors) == 2:
    main_ed.node_dict[node].set_style(color=(255, 255, 0))
```

### Create a Custom Graph
```python
main_ed.clear()

main_ed.add_node(0, pos=[0, 0], color = (0, 0, 255))
main_ed.add_node(1, pos=[100, 0], color = (0, 0, 255))
main_ed.add_node(2, pos=[700, 400], color = (0, 255, 255))
main_ed.add_node(3, pos=[300, 500], color = (0, 255, 0))
main_ed.add_node(4, pos=[30, 500], color = (255, 255, 0))
main_ed.add_node(5, pos=[300, 50], color = (255, 0, 0))

main_ed.add_edge(3,5)
main_ed.add_edge(2,5)
main_ed.add_edge(4,5)
main_ed.add_edge(3,2)
main_ed.add_edge(1,4)
```

### Run Dijkstra Algorithm Animation

```python
alg.dijkstra_animation(main_ed, node1, node2)
```

