from Structure.Vec2 import Vec2 
import dearpygui.dearpygui as dpg
import uuid as UUID
import random


class Node:
    default_radius = 25
    default_color = (255, 255, 255)
    default_highlighted_color = (255,0,255)
    
    def __init__(self, pos = None, vel = [0, 0], uuid = None, updated = True, created = False, color = default_color, radius = default_radius):
        if pos == None: self.pos = Vec2(random.random()*100, random.random()*100) 
        else: self.pos = Vec2(pos)
        self.vel = vel
        self.uuid = uuid 
        if uuid == None: self.uuid = str((UUID.uuid4()).int)[:8]
        self.updated = updated
        self.created = created
        self.style = {"color": color, "radius": radius}

    def draw_node(self, window: str, scale: float = 1, offset: Vec2 = Vec2([0, 0])):
        pos_array = ((self.pos - offset) * scale).to_precision_array(8)
        if self.created:
            dpg.configure_item(self.uuid, center=pos_array, radius=self.style["radius"] * scale, fill = self.style["color"])
        else:
            dpg.draw_circle(pos_array, self.style["radius"] * scale, tag=self.uuid, parent= window, fill=self.style["color"])
            self.created = True

    def is_hovered(self, hkhandler, offset, scale):
        if Vec2.dist(Vec2(hkhandler.pos) / scale + offset, self.pos) <= self.style["radius"]:
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
    