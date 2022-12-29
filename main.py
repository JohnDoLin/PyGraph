import dearpygui.dearpygui as dpg
from Editor.HKHandler import HKHandler
from Editor.Hotkey import Hotkey
from Editor.EditorRegister import EditorRegister
from Editor.Actions import action_func_dict
from Editor.Keybinds import action_dict
import networkx as nx 
import Core.algorithms as alg
import time
from Core.Force import Force
from threading import Thread
import sys
from io import StringIO
dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

# dpg.show_style_editor()
# dpg.show_item_registry()

# dpg.show_debug()
# dpg.show_metrics()

terminal_rs = ""
################# Terminal Function #################
def terminal_callback(sender, data):
    global terminal_rs
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    myThread = Thread(target=lambda: exec(dpg.get_value("terminal")))
    myThread.start()
    sys.stdout = old_stdout
    dpg.set_value('terminal', '')
    terminal_rs += "\n" + redirected_output.getvalue()
    dpg.set_value("terminal_result", terminal_rs)

def constant_cb(sender, data):
    Force.constants[int(sender[1:])] = data

def style_cb(sender, data):
    if hkhandler.selection[2] == None: return 
    item_type = hkhandler.selection[1]
    item = None
    for ed in EditorRegister.editors.values():
        if ed.window == hkhandler.selection[2]:
            if item_type == "node":
                item = ed.node_dict[hkhandler.selection[0]]
            else:
                item = ed.edge_dict[hkhandler.selection[0]]
    if sender == "node_color":
        item.style["color"] = tuple(map(lambda x: x*255, data))
    elif sender == "node_radius":
        item.style["radius"] = data
    elif sender == "node_text":
        item.text = data
    elif sender == "node_border_color":
        item.style["border_color"] = tuple(map(lambda x: x*255, data))
    elif sender == "node_border_width":
        item.style["border_width"] = data
    elif sender == "edge_color":
        item.style["color"] = tuple(map(lambda x: x*255, data))
    elif sender == "edge_thickness":
        item.style["thickness"] = data

    # if hkhandler.selection[1] == "node":

    # if sender == "node_color":
        # hkhandler.selection
    # print(sender, data)

# with dpg.handler_registry():
#     with dpg.add_resize_handler(parent="primary"):
def resize_cb():
    # print(kargs)
    w, h = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.configure_item("main", height=h* 0.95, width=w * 0.5)
    dpg.configure_item("c1", width=w * 0.4)
    dpg.configure_item("c2", width=w * 0.4)
    dpg.configure_item("c3", width=w * 0.4)
    dpg.configure_item("c4", width=w * 0.4)
    dpg.configure_item("terminal", width=w * 0.4)
    dpg.configure_item("terminal_result", wrap=w * 0.4)
    # dpg.configure_item("graph_group", width=dpg.get_item_width("primary")/4)
    # dpg.configure_item("side_window", height=h*0.9, width=w * 0.5)
    # print("w, h of window", w, h)
    # print("w, h of main", dpg.get_item_width("main"), dpg.get_item_height("main"))
    # print("w, h of side_window", dpg.get_item_width("side_window"), dpg.get_item_height("side_window"))
dpg.set_viewport_resize_callback(callback=resize_cb)

def graph_generator_cb(sender):
    if sender == "graph_generator_button_1_1":
        H = nx.star_graph(n=int(dpg.get_value("graph_generator_input_1_1")))
        EditorRegister.editors["main"].graph = nx.compose(H, EditorRegister.editors["main"].graph)
    elif sender == "graph_generator_button_1_2":
        EditorRegister.editors["main"].graph = nx.star_graph(n=int(dpg.get_value("graph_generator_input_1_1")))
    elif sender == "graph_generator_button_2_1":
        H = nx.grid_2d_graph(m=int(dpg.get_value("graph_generator_input_2_1")), n=int(dpg.get_value("graph_generator_input_2_1")))
        EditorRegister.editors["main"].graph = nx.compose(H, EditorRegister.editors["main"].graph)
    elif sender == "graph_generator_button_2_2":
        EditorRegister.editors["main"].graph = nx.grid_2d_graph(m=int(dpg.get_value("graph_generator_input_2_1")), n=int(dpg.get_value("graph_generator_input_2_1")))
    elif sender == "graph_generator_button_3_1":
        H = nx.cubical_graph()
        EditorRegister.editors["main"].graph = nx.compose(H, EditorRegister.editors["main"].graph)
    elif sender == "graph_generator_button_3_2":
        EditorRegister.editors["main"].graph = nx.cubical_graph()
    elif sender == "graph_generator_button_4_1":
        H = nx.random_tree(n=int(dpg.get_value("graph_generator_input_4_1")))
        EditorRegister.editors["main"].graph = nx.compose(H, EditorRegister.editors["main"].graph)
    elif sender == "graph_generator_button_4_2":
        EditorRegister.editors["main"].graph = nx.random_tree(n=int(dpg.get_value("graph_generator_input_4_1")))

    # print(sender)
################# GUI #################
## GUI::Main ##
with dpg.window(label="Primary", tag="primary", width = 1000, height=600):
    with dpg.group(horizontal=True, width=dpg.get_item_width("primary")/4*3):
        with dpg.tab_bar(label = "Graph View Bar", tag = "view_bar"):
            with dpg.tab(label = "Main View", tag = "main_view"):
                    with dpg.drawlist(label = "Main", tag = "main", width = 600, height = 600, pos = [0, 0]):
                        pass

        with dpg.group(horizontal=False, width=dpg.get_item_width("primary")/4):
            ## GUI::Style ##
            # with dpg.group():
                # with dpg.tab_bar(label = "Style Tab Bar", tag = "style_bar"):
        ## GUI::Info ##
            with dpg.child_window(tag="side_window", no_scrollbar=False, autosize_y=True, autosize_x=True, horizontal_scrollbar=True):
                with dpg.tab_bar(label = "Info Tab Bar", tag="info_bar", reorderable=True):
                    with dpg.tab(label="Info", tag="info"):
                        dpg.add_text(f"Some Information of this Graph:")
                        # with dpg.collapsing_header(label="Textures & Images"):
                        with dpg.tree_node(label="Profile", selectable=True, default_open=True):
                            # dpg.add_separator()
                            dpg.add_text(f"Number of Vertices:", bullet=True)
                            dpg.add_text(f"Number of Edges:", bullet=True)
                            dpg.add_text(f"Vertices:", bullet=True)
                            dpg.add_text(f"Edges:", bullet=True)
                        with dpg.tree_node(label="Basic Properties", selectable=True, default_open=True):
                            # dpg.add_separator()
                            dpg.add_text(f"Number of Components:", bullet=True)
                            dpg.add_text(f"Is Connected?", bullet=True)
                            dpg.add_text(f"Centroid:", bullet=True)
                            dpg.add_text(f"Diameter:", bullet=True)
                        with dpg.tree_node(label="Statistics", selectable=True, default_open=True):
                            # dpg.add_separator()
                            dpg.add_text(f"Maximum Degree:", bullet=True)
                            dpg.add_text(f"Minimum Degree:", bullet=True)
                    with dpg.tab(label="Queries"):
                        dpg.add_button(label="Clear All Highlights", callback = lambda: {alg.reset_edge(main_ed), alg.reset_node(main_ed)})
                        with dpg.group(horizontal=True):
                            dpg.add_text("Shortest Path from", bullet=True)
                            dpg.add_input_text(width=50)
                            dpg.add_text("to")
                            dpg.add_input_text(width=50)
                            dpg.add_button(label="Highlight One of the Paths")
                        # dpg.add_button(label="Highlight One of the Paths")
                    with dpg.tab(label="Graph Generator", tag="graph_generator"):
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Compose", tag="graph_generator_button_1_1", callback=graph_generator_cb)
                            dpg.add_button(label="Override", tag="graph_generator_button_1_2", callback=graph_generator_cb)
                            dpg.add_spacer(width=50)
                            dpg.add_text("Star Graph of Size", bullet=True)
                            dpg.add_input_int(tag="graph_generator_input_1_1", width=100)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Compose", tag="graph_generator_button_2_1", callback=graph_generator_cb)
                            dpg.add_button(label="Override", tag="graph_generator_button_2_2", callback=graph_generator_cb)
                            dpg.add_spacer(width=50)
                            dpg.add_text("Lattice Graph of Size", bullet=True)
                            dpg.add_input_int(tag="graph_generator_input_2_1", width=100)
                            dpg.add_text("x")
                            dpg.add_input_int(tag="graph_generator_input_2_2", width=100)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Compose", tag="graph_generator_button_3_1", callback=graph_generator_cb)
                            dpg.add_button(label="Override", tag="graph_generator_button_3_2", callback=graph_generator_cb)
                            dpg.add_spacer(width=50)
                            dpg.add_text("Cubical Graph", bullet=True)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Compose", tag="graph_generator_button_4_1", callback=graph_generator_cb)
                            dpg.add_button(label="Override", tag="graph_generator_button_4_2", callback=graph_generator_cb)
                            dpg.add_spacer(width=50)
                            dpg.add_text("Random Tree Graph of Size", bullet=True)
                            dpg.add_input_int(tag="graph_generator_input_4_1", width=100)
                        
                ## GUI::Constants / Control ##
                with dpg.group():
                    with dpg.tab_bar(label = "Control Tab Bar", tag = "control_bar", reorderable=True):
                        with dpg.tab(label = "Control", tag = "control"):
                            dpg.add_slider_double(label="c1", tag="c1", callback=constant_cb, default_value=Force.constants[1], min_value=0.001, max_value=10, width=600)
                            dpg.add_slider_double(label="c2", tag="c2", callback=constant_cb, default_value=Force.constants[2], min_value=1, max_value=1000, width=600)
                            dpg.add_slider_double(label="c3", tag="c3", callback=constant_cb, default_value=Force.constants[3], min_value=1, max_value=10000000, width=600)
                            dpg.add_slider_double(label="c4", tag="c4", callback=constant_cb, default_value=Force.constants[4], min_value=0, max_value=100, width=600)
                        with dpg.tab(label = "Style", tag = "style"):
                            dpg.add_text(f"Current Selection: None", tag="current_selection")
                            with dpg.group(tag="node_style_menu", horizontal=True, show=False):
                                with dpg.group():
                                    dpg.add_color_picker((0, 0, 0, 255), tag="node_color", width=200, height=200, label="Color", callback=style_cb)
                                    dpg.add_slider_double(tag="node_radius", label="Radius", min_value=0.1, max_value=100, width=200, callback=style_cb)
                                    dpg.add_input_text(tag="node_text", label="Text", width=200, callback=style_cb)
                                with dpg.group():
                                    dpg.add_color_picker((0, 0, 0, 255), tag="node_border_color", width=200, height=200, label="Border Color", callback=style_cb)
                                    dpg.add_slider_double(label="Border Width", tag="node_border_width", min_value=0.1, max_value=100, width=200, callback=style_cb)
                            with dpg.group(tag="edge_style_menu", show=False):
                                with dpg.group(horizontal=True):
                                    with dpg.group():
                                        dpg.add_color_picker((0, 0, 0, 255), tag="edge_color", width=200, height=200, label="Color", callback=style_cb)
                                        dpg.add_slider_double(label="Thickness", tag="edge_thickness", min_value=0.1, max_value=100, width=200, callback=style_cb)

                ## GUI::Terminal ##
                with dpg.group():
                    with dpg.tab_bar(label = "Terminal Tab Bar", tag = "terminal_bar", reorderable=True):
                        with dpg.tab(label = "Terminal", tag = "terminal_tab"):
                            dpg.add_input_text(tag='terminal', multiline=True, default_value="alg.hl_shortest_path(main_ed, (0, 0), (1, 2))", width=600)
                            dpg.add_button(tag="terminal_run", label="Run", callback=terminal_callback)
                            dpg.add_text(tag="terminal_result", wrap=600)
                        with dpg.tab(label = "History", tag="history"):
                            dpg.add_text("History of the terminal")

# dpg.toggle_viewport_fullscreen()

################# Editor Register #################
ed_reg = EditorRegister()
g = nx.grid_2d_graph(m = 3, n = 3)
# g = nx.chvatal_graph()
main_ed = ed_reg.add_editor(window="main", graph = g)


# main_ed.set_camera(0.1, [0, 0])
# main_ed = ed_reg.add_editor(window="main")

# main_ed.add_node(0, pos=[0, 0], color = (0, 0, 255))
# main_ed.add_node(1, pos=[100, 0], color = (0, 0, 255))
# main_ed.add_node(2, pos=[700, 400], color = (0, 255, 255))
# main_ed.add_node(3, pos=[300, 500], color = (0, 255, 0))
# main_ed.add_node(4, pos=[30, 500], color = (255, 255, 0))
# main_ed.add_node(5, pos=[300, 50], color = (255, 0, 0))

# main_ed.add_edge(3,5)
# main_ed.add_edge(2,5)
# main_ed.add_edge(4,5)
# main_ed.add_edge(3,2)
# main_ed.add_edge(1,4)

# write a piece of code that generates colors?

### test algoritms ###
tested = False
def test_alg():
    # alg.hl_shortest_path(main_ed,(1, 2),(3, 5))
    # print(alg.eccentricity(main_ed, 2))
    # alg.hl_eccentricity(main_ed, 2)
    # alg.hl_periphery(main_ed)
    pass

#### Actions and HotKeys ###
hkhandler = HKHandler()
with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=hkhandler.update_wheel)

################# Main Loop #################
dpg.show_viewport()
dpg.set_primary_window("primary", True)
# t0, t1 = time.time()-1, time.time()
# min_fps = 1000
# max_lag = 0
while dpg.is_dearpygui_running():
    # t0, t1 = t1, time.time()
    hkhandler.update()
    for action in action_dict:
        for hk in action_dict[action]:
            if hkhandler.is_hk_active(hk):
                action_func_dict[action](hkhandler)
    for ed in ed_reg.editors.values():
        ed.update_window()
    # t1 = time.time()
    if not tested:
        tested = True
        test_alg()
    dpg.render_dearpygui_frame()
    # if t1 != t0: print("fps =", 1/(t1-t0))
    # else: print("fps =", "oo")
    # print("lag =", time.time() - t0)
    # lag = time.time() - t0
    # if t1 != t0: fps = 1/(t1 - t0)
    # else: fps = 1000
    # if max_lag < lag:
    #     max_lag = lag
    #     print("got laggier:", lag)
    # if min_fps > fps:
    #     min_fps = fps
    #     print("lower fps", fps)
dpg.destroy_context()






