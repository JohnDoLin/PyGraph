import dearpygui.dearpygui as dpg
from Editor.HKHandler import HKHandler
from Editor.EditorRegister import EditorRegister
from Editor.Actions import action_func_dict
from Editor.Keybinds import action_dict
import networkx as nx 
import Core.algorithms as alg
from Core.Force import Force
from threading import Thread
import sys
from io import StringIO
dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

terminal_rs = ""
################# Misc Function #################
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
def resize_cb():
    w, h = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.configure_item("main", height=h* 0.95, width=w * 0.5)
    dpg.configure_item("c1", width=w * 0.35)
    dpg.configure_item("c2", width=w * 0.35)
    dpg.configure_item("c3", width=w * 0.35)
    dpg.configure_item("c4", width=w * 0.35)
    dpg.configure_item("terminal", width=w * 0.4)
    dpg.configure_item("terminal_result", wrap=w * 0.4)

dpg.set_viewport_resize_callback(callback=resize_cb)

def graph_generator_cb(sender):
    if sender == "graph_generator_button_1_1":
        H = nx.star_graph(n=int(dpg.get_value("graph_generator_input_1_1")))
        EditorRegister.editors["main"].graph = nx.compose(H, EditorRegister.editors["main"].graph)
    elif sender == "graph_generator_button_1_2":
        EditorRegister.editors["main"].graph = nx.star_graph(n=int(dpg.get_value("graph_generator_input_1_1")))
    elif sender == "graph_generator_button_2_1":
        H = nx.grid_2d_graph(m=int(dpg.get_value("graph_generator_input_2_1")), n=int(dpg.get_value("graph_generator_input_2_2")))
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

def hl_shortest_path_cb():
    s, t = eval(dpg.get_value("shortest_path_source")), eval(dpg.get_value("shortest_path_target"))
    alg.hl_shortest_path(main_ed, s, t)

def update_info():
    dpg.set_value("info_nodes_num", main_ed.graph.number_of_nodes())
    dpg.set_value("info_edges_num", main_ed.graph.number_of_edges())

    dpg.configure_item("info_nodes", items = list(main_ed.graph.nodes))
    dpg.configure_item("info_edges", items = list(main_ed.graph.edges))

    dpg.set_value("info_components_num", nx.number_connected_components(main_ed.graph))
    dpg.set_value("info_is_connected", nx.is_connected(main_ed.graph))
    if nx.is_connected(main_ed.graph):
        dpg.set_value("info_center", nx.center(main_ed.graph))
        dpg.set_value("info_diameter", nx.diameter(main_ed.graph))
    else:
        dpg.set_value("info_center", "-")
        dpg.set_value("info_diameter", "-")
    m, M = 1000000, -1
    for i in nx.degree(main_ed.graph):
        if m > i[1]:
            m = i[1]
        if M < i[1]:
            M = i[1]
    dpg.set_value("info_max_deg", M)
    dpg.set_value("info_min_deg", m)

    # dpg.set_value("info_edges_num", main_ed.graph.number_of_edges())
    # pass


################# GUI #################
text_hl_color = (255, 255, 0)

## GUI::Main ##
with dpg.window(label="Primary", tag="primary", width = 1000, height=600, no_scrollbar=True, horizontal_scrollbar=False, autosize=False, no_bring_to_front_on_focus=True):
    with dpg.group(horizontal=True, width=dpg.get_item_width("primary")/2, tag="graph_group"):
        with dpg.tab_bar(label = "Graph View Bar", tag = "view_bar", reorderable=True):
            with dpg.tab(label = "Main View", tag = "main_view"):
                    with dpg.drawlist(label = "Main", tag = "main", width = 600, height = 600, pos = [0, 0]):
                        pass
                        
        with dpg.group(horizontal=False, width=dpg.get_item_width("primary")/4):
            ## GUI::Style ##
            with dpg.child_window(tag="side_window", no_scrollbar=False, autosize_y=True, autosize_x=True, horizontal_scrollbar=True):
                with dpg.tab_bar(label = "Info Tab Bar", tag="info_bar", reorderable=True):
                    with dpg.tab(label="Info", tag="info"):
                        with dpg.tree_node(label="Profile", selectable=True, default_open=True):
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Number of Nodes:", bullet=True)
                                dpg.add_text(tag="info_nodes_num", color=text_hl_color)
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Number of Edges:", bullet=True)
                                dpg.add_text(tag="info_edges_num", color=text_hl_color)
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Nodes:", bullet=True)
                                dpg.add_listbox(tag="info_nodes")
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Edges:", bullet=True)
                                dpg.add_listbox(tag="info_edges")
                        with dpg.tree_node(label="Basic Properties", selectable=True, default_open=True):
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Number of Connected Components:", bullet=True)
                                dpg.add_text(tag="info_components_num", color=text_hl_color)
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Is Connected?:", bullet=True)
                                dpg.add_text(tag="info_is_connected", color=text_hl_color)
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Center:", bullet=True)
                                dpg.add_text(tag="info_center", color=text_hl_color)
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Diameter:", bullet=True)
                                dpg.add_text(tag="info_diameter", color=text_hl_color)
                        with dpg.tree_node(label="Statistics", selectable=True, default_open=True):
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Maximum Degree:", bullet=True)
                                dpg.add_text(tag="info_max_deg", color=text_hl_color)
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"Minimum Degree:", bullet=True)
                                dpg.add_text(tag="info_min_deg", color=text_hl_color)
                    with dpg.tab(label="Queries"):
                        dpg.add_button(label="Clear All Highlights", callback = lambda: {alg.reset_edge(main_ed), alg.reset_node(main_ed)})
                        with dpg.group(horizontal=True):
                            dpg.add_text("Shortest Path from", bullet=True)
                            dpg.add_input_text(width=50, tag="shortest_path_source")
                            dpg.add_text("to")
                            dpg.add_input_text(width=50, tag="shortest_path_target")
                            dpg.add_button(label="Highlight One of the Paths", callback=hl_shortest_path_cb)
               ## GUI::Constants / Control ##
                with dpg.tab_bar(label = "Control Tab Bar", tag = "control_bar", reorderable=True):
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
                    with dpg.tab(label="Graph Generator", tag="graph_generator"):
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Compose", tag="graph_generator_button_1_1", callback=graph_generator_cb)
                            dpg.add_button(label="Override", tag="graph_generator_button_1_2", callback=graph_generator_cb)
                            dpg.add_spacer(width=50)
                            dpg.add_text("Star Graph of Size", bullet=True)
                            dpg.add_input_int(tag="graph_generator_input_1_1", width=100, default_value=3)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Compose", tag="graph_generator_button_2_1", callback=graph_generator_cb)
                            dpg.add_button(label="Override", tag="graph_generator_button_2_2", callback=graph_generator_cb)
                            dpg.add_spacer(width=50)
                            dpg.add_text("Lattice Graph of Size", bullet=True)
                            dpg.add_input_int(tag="graph_generator_input_2_1", width=100, default_value=3)
                            dpg.add_text("x")
                            dpg.add_input_int(tag="graph_generator_input_2_2", width=100, default_value=3)
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
                            dpg.add_input_int(tag="graph_generator_input_4_1", width=100, default_value=3)
                ## GUI::Terminal ##
                with dpg.group():
                    with dpg.tab_bar(label = "Terminal Tab Bar", tag = "terminal_bar", reorderable=True):
                        with dpg.tab(label = "Control", tag = "control"):
                            dpg.add_slider_double(label="c1 (Attraction)", tag="c1", callback=constant_cb, default_value=Force.constants[1], min_value=0.001, max_value=10, width=600)
                            dpg.add_slider_double(label="c2 (Repulsion)", tag="c2", callback=constant_cb, default_value=Force.constants[2], min_value=1, max_value=1000, width=600)
                            dpg.add_slider_double(label="c3 (Repulsion)", tag="c3", callback=constant_cb, default_value=Force.constants[3], min_value=1, max_value=10000000, width=600)
                            dpg.add_slider_double(label="c4 (Edge Attraction)", tag="c4", callback=constant_cb, default_value=Force.constants[4], min_value=0, max_value=100, width=600)
                        with dpg.tab(label = "Terminal", tag = "terminal_tab"):
                            dpg.add_input_text(tag='terminal', multiline=True, default_value="", width=600)
                            dpg.add_button(tag="terminal_run", label="Run", callback=terminal_callback)
                            dpg.add_text(tag="terminal_result", wrap=600)

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


#### Actions and HotKeys ###
hkhandler = HKHandler()
with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=hkhandler.update_wheel)

################# Main Loop #################
dpg.show_viewport()
dpg.set_primary_window("primary", True)
while dpg.is_dearpygui_running():
    hkhandler.update()
    for action in action_dict:
        for hk in action_dict[action]:
            if hkhandler.is_hk_active(hk):
                action_func_dict[action](hkhandler)
    for ed in ed_reg.editors.values():
        ed.update_window()
    update_info()
    dpg.render_dearpygui_frame()
dpg.destroy_context()






