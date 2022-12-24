from Structure.Vec2 import Vec2 
import dearpygui.dearpygui as dpg
import uuid as UUID


class Node:
    node_radius = 25
    default_color = (255, 255, 255)
    default_highlighted_color = (255,0,255)
    
    def __init__(self, pos = [0, 0], vel = [0, 0], uuid = None, updated = True, created = False, color = default_color):
        self.pos = Vec2(pos)
        self.vel = vel
        self.uuid = uuid 
        if uuid == None: self.uuid = str((UUID.uuid4()).int)[:8]
        self.updated = updated
        self.created = created
        self.style = {"color": color}

    def draw_node(self, window: str, scale: float = 1):
        pos_array = self.pos.to_precision_array(8)
        if self.created:
            dpg.configure_item(self.uuid, center=pos_array, fill = self.style["color"])
        else:
            dpg.draw_circle(pos_array, Node.node_radius * scale, tag=self.uuid, parent= window, fill=self.style["color"])
            self.created = True

    def is_hovered(self, hkhandler):
        if Vec2.dist(Vec2(hkhandler.pos), self.pos) <= Node.node_radius:
            return True
        return False

    def set_style(self, **kargs):
        for key in kargs:
            self.style[key] = kargs[key]

    def toggle_highlight(self):
        if self.style["color"] != Node.default_color:
            self.set_style(color = Node.default_color)
        else:
            self.set_style(color = Node.default_highlighted_color)
    def setter(self, **kargs):
        for key in kargs:
            self.key = kargs[key]
    