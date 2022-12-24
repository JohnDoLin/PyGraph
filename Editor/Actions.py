import networkx as nx
from Editor.EditorRegister import EditorRegister as EdReg
from Structure.Vec2 import Vec2
def pan(hkhandler):
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list) != 0 
            and len(hkhandler.hover_list[window]["node"]) == 0
            ):
            for ed in EdReg.editors.values():
                if hkhandler.press:
                    ed.prev_offset = ed.offset
                if hkhandler.is_dragging:
                    if ed.window == window:
                        ed.set_camera(ed.scale, ed.prev_offset - Vec2(hkhandler.press_pos) + Vec2(hkhandler.pos))
    # print("panning")
def drag_node(hkhandler):
    pass

def zoom(hkhandler):
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list) != 0):
            for ed in EdReg.editors.values():
                if ed.window == window:
                    ed.set_camera(ed.scale * 2**(hkhandler.wheel_speed), ed.offset)
                    # Cursor should be the center
    # print("zooming")

action_func_dict = {"pan": pan,
                    "zoom": zoom,
                    "drag_node": drag_node
                    }
