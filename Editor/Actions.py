import dearpygui.dearpygui as dpg
import networkx as nx
from Editor.EditorRegister import EditorRegister as EdReg
from Structure.Vec2 import Vec2
def pan(hkhandler):
    if hkhandler.mouse_down_mode != "pan" and hkhandler.mouse_down_mode != None: return
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list[window]["node"]) == 0
            ):
            for ed in EdReg.editors.values():
                if hkhandler.press:
                    ed.prev_offset = ed.offset
                if hkhandler.is_dragging:
                    if ed.window == window:
                        ed.set_camera(ed.scale, ed.prev_offset + (Vec2(hkhandler.press_pos) - Vec2(hkhandler.pos)) / ed.scale)
                        hkhandler.mouse_down_mode = "pan"
    # print("panning")


def drag_node(hkhandler):
    if hkhandler.mouse_down_mode == None:
        for window in hkhandler.hover_list:
            if len(hkhandler.hover_list[window]["node"]) != 0:
                hkhandler.mouse_down_data = {"node": hkhandler.hover_list[window]["node"][0], "window": window}
                hkhandler.mouse_down_mode = "drag_node"
    if hkhandler.mouse_down_mode == "drag_node":
        for ed in EdReg.editors.values():
            if ed.window == hkhandler.mouse_down_data["window"]:
                ed.node_dict[hkhandler.mouse_down_data["node"]].pos = (Vec2(hkhandler.pos))/ed.scale + ed.offset
                # print("dragging node")

def zoom(hkhandler):
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list) != 0):
            for ed in EdReg.editors.values():
                if ed.window == window:
                    ed.set_camera(ed.scale * 2**(hkhandler.wheel_speed), ed.offset + Vec2(hkhandler.pos)/ed.scale*(1-1/(2**(hkhandler.wheel_speed))))
                    # Cursor should be the center
    # print("zooming")

def eval_terminal(hkhandler):
    print('eval_terminal activated')
    print(dpg.get_value("terminal"))
    dpg.configure_item("terminal", enabled=False)
    dpg.set_value("terminal", "")
    dpg.configure_item("terminal", enabled=True)
    # if dpg.get_item_state("terminal")["focused"]:
        # dpg.set_value("terminal", "")
    pass
action_func_dict = {"pan": pan,
                    "zoom": zoom,
                    "drag_node": drag_node,
                    "eval_terminal": eval_terminal,
                    }
