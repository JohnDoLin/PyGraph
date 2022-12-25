import dearpygui.dearpygui as dpg
import networkx as nx
import Core.Force as fs
from Core.Node import Node as Node
from Core.Edge import Edge as Edge 
from Structure.Vec2 import Vec2 
dt = 1

class Editor:
    '''
    Editor will only show things in edge_dict and node_dict.
    '''

    def __init__(self, window = None, graph: nx.Graph = None):
        self.window = window
        if graph == None: graph = nx.Graph()
        self.graph = graph
        self.node_dict = dict()
        self.edge_dict = dict()
        self.scale = 1
        self.offset = Vec2(0, 0)
        self.prev_offset = Vec2(0, 0)

    def graph_to_view_coords(self, pos):
        return (pos - self.offset) * self.scale
    
    def update_window(self):             
        for node in self.graph:
            if node in self.node_dict:
                new_vel = Vec2(0, 0)
                for n2 in self.graph.nodes:
                    if node != n2: # Not needed?
                        new_vel += (self.node_dict[n2].pos-self.node_dict[node].pos).normalized() * fs.attraction(self.node_dict[node].pos, self.node_dict[n2].pos)
                        new_vel += (self.node_dict[node].pos-self.node_dict[n2].pos).normalized() * fs.repulsion(self.node_dict[node].pos, self.node_dict[n2].pos)
                # new_vel *= 0.5
                self.node_dict[node].vel = new_vel
                self.node_dict[node].pos += new_vel*dt
                self.node_dict[node].updated = True
            else:
                self.node_dict[node] = Node()

        for node_pair in list(self.graph.edges):
            # For now I ignore parallel edges (i.e. multiedges) bc I literally don't care about them

            # A new issue: for undirected graph (deault), e1 = (n1, n2) and e2 = (n2, n1) are recognized differently in edge_dict but not in nxgraph objects.
            # I could use set instead but that would be a pain when converting graph between directed and undirected ones. 
            
            # Solution I use here: for undirected graph edge_dict stores both e1 and e2, and pointin towards the same Edge object.
            # This gives rise to another problem: when updating (or any time iterating edge_dict), you encounter the same edge twice.
            # But you can just check if that edge is updated so it's prolly not a big issue (for example in HKHandler).

            # OK that was a really dumb idea. Let's use frozenset instead.
            node_fs = frozenset({node_pair[0], node_pair[1]})
            if node_fs not in self.edge_dict:
                self.add_edge(node_pair[0], node_pair[1])
            else:
                self.edge_dict[node_fs].updated = True

        # Draw the edge first so it would be on the back 
        pop_list = []
        for node_pair in self.edge_dict:
            edge = self.edge_dict[node_pair]
            if not edge.updated:
                pop_list.append(node_pair)
            else:
                edge.draw_edge(window = self.window, scale = self.scale, offset = self.offset)
            edge.updated = False
        for np in pop_list:
            self.edge_dict.pop(np)
        
        for node in self.node_dict:
            nd = self.node_dict[node]
            if not nd.updated:
                self.node_dict.pop(nd)
            else:
                nd.draw_node(window = self.window, scale = self.scale, offset = self.offset)
            nd.updated = False

    def add_node(self, node, pos = [0,0], **kargs):
        if node not in self.node_dict:
            self.graph.add_node(node)
            self.node_dict[node] = Node(pos = Vec2(pos), **kargs)

    def add_edge(self, node1, node2, **kargs):
        node_pair = frozenset({node1, node2})
        # If the nodes didn't exist we simply create them
        self.graph.add_edges_from([node_pair])
        self.add_node(node1)
        self.add_node(node2)
        self.edge_dict[node_pair] = Edge(start = self.node_dict[node1], end = self.node_dict[node2], **kargs)


    # def delete_node(self, node):
    #     self.graph.remove_nodes_from([node])  
    #     self.node_dict.remove(self.graph.nodes[node])

    # def set_node(self, node, data):
    #     pass

    def set_camera(self, scale: float, offset: list):
        self.scale = scale
        self.offset = Vec2(offset)


        

            