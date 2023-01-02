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
