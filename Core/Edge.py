from Structure.Vec2 import Vec2 
import dearpygui.dearpygui as dpg
from Core.Node import Node as Node
import uuid as UUID


class Edge:
    default_thickness = 5
    default_color = (255, 255, 255)
    default_highlighted_color = (255, 0, 255)

    def __init__(self, start: Node, end: Node, uuid = None, updated = True, created = False, color: tuple = default_color, thickness = default_thickness):
        self.start = start
        self.end = end
        self.uuid = uuid
        if uuid == None: self.uuid = str((UUID.uuid4()).int)[:8]
        self.updated = updated
        self.created = created
        self.style = {"color": color, "thickness": thickness}

    def draw_edge(self, window: str, scale: float = 1, offset: Vec2 = Vec2(0, 0)):
        pos1_array = ((self.start.pos - offset) * scale).to_precision_array(8)
        pos2_array = ((self.end.pos - offset)  * scale).to_precision_array(8)
        if self.created:
            dpg.configure_item(self.uuid, p1 = pos1_array, p2 = pos2_array, color = self.style["color"], thickness= self.style["thickness"] * scale)
        else:
            dpg.draw_line(pos1_array, pos2_array, tag=self.uuid, parent= window, color= self.style["color"], thickness= self.style["thickness"] * scale)
            self.created = True

    def is_hovered(self, hkhandler, offset, scale):
        if (Vec2(hkhandler.pos)/ scale + offset).dist_to_two_dots(self.start.pos, self.end.pos) <= self.style["thickness"] /2:
            ## Should be * scale
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
