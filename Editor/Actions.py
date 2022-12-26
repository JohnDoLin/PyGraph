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
                if hkhandler.mouse_down_data["node"] not in ed.node_dict:
                    hkhandler.mouse_down_mode = "-drag_node"
                    return
                ed.node_dict[hkhandler.mouse_down_data["node"]].pos = (Vec2(hkhandler.pos))/ed.scale + ed.offset
                ed.node_dict[hkhandler.mouse_down_data["node"]].vel = Vec2(0, 0) 
                # print("dragging node")

def zoom(hkhandler):
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list) != 0):
            for ed in EdReg.editors.values():
                if ed.window == window:
                    ed.set_camera(ed.scale * 2**(hkhandler.wheel_speed), ed.offset + Vec2(hkhandler.pos)/ed.scale*(1-1/(2**(hkhandler.wheel_speed))))
    # print("zooming")

c= 2
def eval_terminal(hkhandler):
    global c
    c+=1
    # print('eval_terminal activated')
    # print(dpg.get_value("terminal"))
    # dpg.configure_item("terminal", enabled=False)
    # dpg.set_value("terminal", "")
    # dpg.configure_item("terminal", enabled=True)
    print("terminal activated")
    print("changing graph")
    EdReg.editors["main"].graph = nx.star_graph(c)
    # if dpg.get_item_state("terminal")["focused"]:
        # dpg.set_value("terminal", "")
    pass

def add_node(hkhandler):
    if not hkhandler.press: return 
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list) != 0):
            for ed in EdReg.editors.values():
                if ed.window == window and len(hkhandler.hover_list[window]["node"]) == 0:
                    ed.add_node(pos = ((Vec2(hkhandler.pos)) / ed.scale + ed.offset))
                    return

def delete_node(hkhandler):
    if not hkhandler.press: return 
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list) != 0):
            for ed in EdReg.editors.values():
                if ed.window == window and len(hkhandler.hover_list[window]["node"]) != 0:
                    ed.delete_node(hkhandler.hover_list[window]["node"][0])
                    return



action_func_dict = {"pan": pan,
                    "zoom": zoom,
                    "drag_node": drag_node,
                    # "eval_terminal": eval_terminal,
                    "add_node": add_node,
                    "delete_node": delete_node,
                    }
