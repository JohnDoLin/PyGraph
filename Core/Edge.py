from Structure.Vec2 import Vec2 
import dearpygui.dearpygui as dpg
from Core.Node import Node as Node
import uuid as UUID


class Edge:
    edge_thickness = 5
    default_color = (255, 255, 255)
    default_highlighted_color = (255, 0, 255)

    def __init__(self, start: Node, end: Node, uuid = None, updated = True, created = False, color: tuple = default_color):
        self.start = start
        self.end = end
        self.uuid = uuid
        if uuid == None: self.uuid = str((UUID.uuid4()).int)[:8]
        self.updated = updated
        self.created = created
        self.style = {"color": color}

    def draw_edge(self, window: str, scale: float = 1):
        pos1_array = self.start.pos.to_precision_array(8)
        pos2_array = self.end.pos.to_precision_array(8)
        if self.created:
            dpg.configure_item(self.uuid, p1 = pos1_array, p2 = pos2_array, color = self.style["color"], thickness= Edge.edge_thickness * scale)
        else:
            dpg.draw_line(pos1_array, pos2_array, tag=self.uuid, parent= window, color= self.style["color"], thickness= Edge.edge_thickness * scale)
            self.created = True

    def is_hovered(self, hkhandler):
        if Vec2(hkhandler.pos).dist_to_two_dots(self.start.pos, self.end.pos) <= Edge.edge_thickness/2:
            return True
        return False

    def set_style(self, **kargs):
        for key in kargs:
            self.style[key] = kargs[key]
    
    def toggle_highlight(self):
        if self.style["color"] != Edge.default_color:
            self.set_style(color = Edge.default_color)
        else:
            self.set_style(color = Edge.default_highlighted_color)
    def setter(self, **kargs):
        for key in kargs:
            self.key = kargs[key]
