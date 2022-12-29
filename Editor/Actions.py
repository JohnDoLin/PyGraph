import dearpygui.dearpygui as dpg
import networkx as nx
from Editor.EditorRegister import EditorRegister as EdReg
from Structure.Vec2 import Vec2
def pan(hkhandler):
    if hkhandler.mouse_down_mode != "pan" and hkhandler.mouse_down_mode != None: return
    # if len(hkhandler.kbd) != 0: return 
    # print("panning")
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list[window]["node"]) == 0):
            for ed in EdReg.editors.values():
                if hkhandler.press:
                    ed.prev_offset = ed.offset
                if hkhandler.is_dragging:
                    if ed.window == window:
                        ed.set_camera(ed.scale, ed.prev_offset + (Vec2(hkhandler.press_pos) - Vec2(hkhandler.pos)) / ed.scale)
                        hkhandler.mouse_down_mode = "pan"
                        return
    if hkhandler.mouse_down_mode != "pan": hkhandler.mouse_down_mode == "-pan"


def drag_node(hkhandler):
    # if len(hkhandler.mouse) != 0: return 
    # print("dragging node")
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
    # print("zooming")
    zooming_ratio = 1.5
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list) != 0):
            for ed in EdReg.editors.values():
                if ed.window == window:
                    ed.set_camera(ed.scale * zooming_ratio**(hkhandler.wheel_speed), ed.offset + Vec2(hkhandler.pos)/ed.scale*(1-1/(zooming_ratio**(hkhandler.wheel_speed))))
                    # print("zooming")

def add_node(hkhandler):
    # print(hkhandler)
    # if not hkhandler.press: return 
    if hkhandler.mouse_down_mode != None: return 
    # print("adding node")
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list) != 0):
            for ed in EdReg.editors.values():
                if ed.window == window and len(hkhandler.hover_list[window]["node"]) == 0:
                    ed.add_node(pos = ((Vec2(hkhandler.pos)) / ed.scale + ed.offset))
                    return
    hkhandler.mouse_down_mode = "-add_node"

def delete_node(hkhandler):
    # if not hkhandler.release: return 
    # print("deleting node")
    if hkhandler.mouse_down_mode != None: return 
    for window in hkhandler.hover_list:
        if (len(hkhandler.hover_list) != 0):
            for ed in EdReg.editors.values():
                if ed.window == window and len(hkhandler.hover_list[window]["node"]) != 0:
                    ed.delete_node(hkhandler.hover_list[window]["node"][0])
                    return

def add_edge(hkhandler):
    # print("add_edge")
    if not (
        hkhandler.mouse_down_mode == "-add_node" 
        or hkhandler.mouse_down_mode == "add_edge"
        or hkhandler.mouse_down_mode == None
        ): return

    if not hkhandler.release:
        if hkhandler.mouse_down_data != None: return 
        for window in hkhandler.hover_list:
            for ed in EdReg.editors.values():
                if ed.window == window and len(hkhandler.hover_list[window]["node"]) != 0:
                    hkhandler.mouse_down_mode = "add_edge"
                    hkhandler.mouse_down_data = {"node": hkhandler.hover_list[window]["node"][0]}
                    # print("upd node")
                    return
        # hkhandler.mouse_down_mode = "-add_edge"
    else:
        # print("RELEASED")
        if hkhandler.mouse_down_mode != "add_edge": return
        for window in hkhandler.hover_list:
            for ed in EdReg.editors.values():
                if ed.window == window and len(hkhandler.hover_list[window]["node"]) != 0:
                    if hkhandler.mouse_down_data["node"] == hkhandler.hover_list[window]["node"][0]:
                        # print("FAILED TO ADD SELF LOOP")
                        pass
                    else:
                        node_pair = frozenset({hkhandler.mouse_down_data["node"], hkhandler.hover_list[window]["node"][0]})
                        if node_pair not in ed.edge_dict:
                            ed.add_edge(hkhandler.mouse_down_data["node"], hkhandler.hover_list[window]["node"][0])
def delete_edge(hkhandler):
    # print("deleting edge")
    if not (
    # hkhandler.mouse_down_mode == "-add_node" 
    hkhandler.mouse_down_mode == "delete_edge"
    or hkhandler.mouse_down_mode == None
    ): return
    hkhandler.mouse_down_mode = "delete_edge"

    if not hkhandler.release:
        if hkhandler.mouse_down_data != None: return 
        for window in hkhandler.hover_list:
            for ed in EdReg.editors.values():
                if ed.window == window and len(hkhandler.hover_list[window]["node"]) != 0:
                    hkhandler.mouse_down_data = {"node": hkhandler.hover_list[window]["node"][0]}
                    return
        # hkhandler.mouse_down_mode = "-delete_edge"
    else:
        # print("RELEASE")
        for window in hkhandler.hover_list:
            for ed in EdReg.editors.values():
                if ed.window == window and len(hkhandler.hover_list[window]["node"]) != 0:
                    # print("now node", hkhandler.hover_list[window]["node"][0])
                    # print("start node", hkhandler.hover_list[window]["node"][0])
                    if hkhandler.mouse_down_data["node"] == hkhandler.hover_list[window]["node"][0]:
                        # print("FAILED TO DELETE SELF LOOP")
                        # ed.delete_node(hkhandler.mouse_down_data["node"])
                        pass
                    else:
                        node_pair = frozenset({hkhandler.mouse_down_data["node"], hkhandler.hover_list[window]["node"][0]})
                        if node_pair in ed.edge_dict:
                            ed.delete_edge(node_pair)
                            # print("edge deleted: ", node_pair)

def selection(hkhandler):
    # print("selecting")
    for window in hkhandler.hover_list:
        for ed in EdReg.editors.values():
            if ed.window == window:
                if len(hkhandler.hover_list[window]["node"]) != 0:
                    hkhandler.selection = (hkhandler.hover_list[window]["node"][0], "node", window)
                    node_name = hkhandler.selection[0]
                    nd = ed.node_dict[node_name]
                    dpg.configure_item(item="node_style_menu", show=True)
                    dpg.configure_item(item="edge_style_menu", show=False)
                    dpg.configure_item(item="node_color", default_value=nd.style["color"])
                    dpg.configure_item(item="node_radius", default_value=nd.style["radius"])
                    dpg.configure_item(item="node_text", default_value=nd.text)
                    dpg.configure_item(item="node_border_color", default_value=nd.style["border_color"])
                    dpg.configure_item(item="node_border_width", default_value=nd.style["border_width"])
                elif len(hkhandler.hover_list[window]["edge"]) != 0:
                    hkhandler.selection = (hkhandler.hover_list[window]["edge"][0], "edge", window)
                    dpg.configure_item(item="node_style_menu", show=False)
                    dpg.configure_item(item="edge_style_menu", show=True)
                    edge_name = hkhandler.selection[0]
                    edge = ed.edge_dict[edge_name]
                    dpg.configure_item(item="edge_color", default_value=edge.style["color"])
                    dpg.configure_item(item="edge_thickness", default_value=edge.style["thickness"])
                else:
                    hkhandler.selection = (None, None, None)
                    dpg.configure_item(item="node_style_menu", show=False)
                    dpg.configure_item(item="edge_style_menu", show=False)
                dpg.set_value("current_selection", f"Current Selection: {hkhandler.selection[0]}")
                # print('hkhandler.selection', f"Current Selection: {hkhandler.selection}")
                return

action_func_dict = {
                    "add_edge": add_edge,
                    "delete_edge": delete_edge,
                    "pan": pan,
                    "zoom": zoom,
                    "drag_node": drag_node,
                    "add_node": add_node,
                    "delete_node": delete_node,
                    "selection": selection,
                    }
