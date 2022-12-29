import dearpygui.dearpygui as dpg
import networkx as nx
from Core.Node import Node
from Core.Edge import Edge
import math
import time

### default colors ###
node_df = (255,255,255,255)
edge_df = (255,255,255,255)
node_dfhl = (255,0,255,255)
edge_dfhl = (255,0,255,255)

### highlight ###
def hl_node(ed, nodes, hl:tuple = node_dfhl): # highlights a node, or nodes in a list
    if type(nodes) == list:
        for node in nodes:
            ed.node_dict[node].set_style(color = hl)
    else:
        ed.node_dict[nodes].set_style(color = hl)
    return None
    
def hl_edge(ed, edges, hl:tuple = node_dfhl): # highlights an edge, or edges in a list
    if type(edges) == list:
        for edge in edges:
            edge = frozenset({edge[0], edge[1]})
            ed.edge_dict[edge].set_style(color = hl)
    else:
        edge = frozenset({edges[0], edges[1]})
        ed.edge_dict[edge].set_style(color = hl)
    return None
    
def reset_node(ed, *args): # resets node(s) back to initial style
    if len(args) == 0:
        for node in ed.node_dict:
            reset_node(ed, node)
        return None
    for node in args:
        ed.node_dict[node].set_style(color = ed.node_dict[node].initial_style["color"], radius = ed.node_dict[node].initial_style["radius"])
    return None

def reset_edge(ed, *args): # resets edge(s) back to initial style
    if len(args) == 0:
        for edge in ed.edge_dict:
            reset_edge(ed, edge)
        return None
    for edge in args:
        ed.edge_dict[edge].set_style(color = ed.edge_dict[edge].initial_style["color"], thickness = ed.edge_dict[edge].initial_style["thickness"])
    return None

def reset_all(ed): # reset all nodes and edges
    for node in ed.node_dict:
            reset_node(ed, node)
    for edge in ed.edge_dict:
            reset_edge(ed, edge)
    return None

## Example Algorithms

visited = set() # Set to keep track of visited nodes of graph.
def dfs_tree_animation(ed, source, visited = set()):
    if source not in visited:
        # print(node)
        visited.add(source)
        hl_node(ed, source) # Visited
        time.sleep(0.25)
        for neighbour in ed.graph[source]:
            hl_edge(ed, (source, neighbour))
            time.sleep(0.25)
            dfs_tree_animation(ed, neighbour, visited)
    # visited = set()
    
def dijkstra_animation(ed, source, target):
    checked_color = (0, 255, 0)
    checking_color = (0, 0, 255)
    result_color = (255, 0, 0)
    
    hl_node(ed, [source, target])
    
    def dist_sort(node):
        return G.nodes[node]['dist']
    
    G = nx.Graph()
    G.add_nodes_from(ed.graph)
    G.add_edges_from(ed.graph.edges)
    unvisited = [node for node in G.nodes]
    attrs = {node: {'dist': math.inf, 'prev': None} for node in G.nodes}
    nx.set_node_attributes(G, attrs)
    current = source
    G.nodes[current]['dist'] = 0
    unvisited.sort(key = dist_sort)
    while G.nodes[unvisited[0]]['dist'] < math.inf and target in unvisited:
        ed.node_dict[current].set_style(color = checking_color)
        time.sleep(0.25)
        for node in G.adj[current]:
            if node in unvisited:
                ed.node_dict[node].set_style(color = checking_color)
                ed.edge_dict[frozenset([node, current])].set_style(color = checking_color)
                time.sleep(0.25)
                reset_node(ed, node)
                if node == target:
                    hl_node(ed, node) # color of target node during search?
                reset_edge(ed, frozenset([node, current]))
                if G.nodes[node]['dist'] > 1 + G.nodes[current]['dist']:
                    G.nodes[node]['dist'] = 1 + G.nodes[current]['dist']
                    G.nodes[node]['prev'] = current
        unvisited.remove(current)
        unvisited.sort(key = dist_sort)
        ed.node_dict[current].set_style(color = checked_color)
        if current == source:
            hl_node(ed, current) # color of source node during search?
        if G.nodes[current]['prev'] != None:
            ed.edge_dict[frozenset([current, G.nodes[current]['prev']])].set_style(color = checked_color)
        time.sleep(0.25)
        if len(unvisited) == 0:
            break
        current = unvisited[0]
        
    trace_back = target
    while G.nodes[trace_back]['prev'] != None:
        ed.edge_dict[frozenset([trace_back, G.nodes[trace_back]['prev']])].set_style(color = result_color)
        trace_back = G.nodes[trace_back]['prev']
    ed.node_dict[source].set_style(color = result_color)
    ed.node_dict[target].set_style(color = result_color)
         
    return None


### distance properties ###
def dist(ed, source, target): # returns distance between source and target nodes
    return len(list(nx.shortest_simple_paths(ed.graph, source, target))[0])-1

def hl_shortest_path(ed, source, target, node_hl = node_dfhl, edge_hl = edge_dfhl): # highlights a shortest path between source and target nodes
   
    path = list(nx.shortest_simple_paths(ed.graph, source, target))[0]
    # hl_node(ed, [path[0], path[-1]], node_hl)
    # print("path", path)
    if len(path)>1:
        # print("path[0]", path[0])
        hl_node(ed, [path[i] for i in range(len(path))], node_hl)
        hl_edge(ed, [(path[i],path[i+1]) for i in range(len(path)-1)], edge_hl)
    return None

def eccentricity(ed, *args): # returns a dictionary consisting of each node's eccentricity, or the eccentricity of a particular node
    if len(args) == 0:
        if nx.is_connected(ed.graph):
            return nx.eccentricity(ed.graph)
        else: 
            return {node:math.inf for node in ed.graph.nodes}
    if len(args) == 1:
        if nx.is_connected(ed.graph):
            return nx.eccentricity(ed.graph)[args[0]]
        else:
            return math.inf
        
def hl_eccentricity(ed, node, node_hl = node_dfhl, edge_hl = edge_dfhl): # highlights a shortest path between input node and another node with its length being the eccentricity of the input node
    if nx.is_connected(ed.graph):
        for n2 in ed.node_dict:
            if dist(ed, node, n2) == eccentricity(ed, node):
                hl_shortest_path(ed, node, n2, node_hl, edge_hl)
                return None
    return None
    # this seems inefficient
        
def diameter(ed): # returns the diameter (maximum eccentricity) 
    if nx.is_connected(ed.graph):
        return nx.diameter(ed.graph)
    else:
        return math.inf  
    
def periphery(ed): # returns a list of nodes in periphery. the periphery is the set of nodes with eccentricity equal to the diameter.    
    if nx.is_connected(ed.graph):
        return nx.periphery(ed.graph)
    return None

def hl_periphery(ed, hl = node_dfhl): # highlights the periphery
    hl_node(ed, periphery(ed), hl)
    return None

def hl_diameter(ed, node_hl = node_dfhl, edge_hl = edge_dfhl): # highlights a shortest path whose length is the diameter
    hl_eccentricity(ed, periphery(ed)[0], node_hl, edge_hl)
    return None

def radius(ed): # returns the radius (minimum eccentricity) 
    if nx.is_connected(ed.graph):
        return nx.radius(ed.graph)
    else:
        return math.inf  
    
def center(ed): # returns a list of center nodes. the center is the set of nodes with eccentricity equal to radius.    
    if nx.is_connected(ed.graph):
        return nx.center(ed.graph)
    return None

def hl_center(ed, hl = node_dfhl): # highlights the center
    hl_node(ed, center(ed), hl)
    return None

def hl_radius(ed, node_hl = node_dfhl, edge_hl = edge_dfhl): # highlights a shortest path whose length is the radius
    hl_eccentricity(ed, center(ed)[0], node_hl, edge_hl)
    return None

    

                
