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
dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

# dpg.show_style_editor()
# dpg.show_item_registry()

# dpg.show_debug()
# dpg.show_metrics()

################# Treminal Function #################
def terminal_callback(sender, data):
    myThread = Thread(target=lambda: exec(dpg.get_value("terminal")))
    myThread.start()
    dpg.set_value('terminal', '')

def constant_cb(sender, data):
    Force.constants[int(sender[1:])] = data

################# GUI #################
## GUI::Main ##
with dpg.window(label="Primary", tag="primary", width = 1000, height=600):
    with dpg.group(horizontal=True, width=dpg.get_item_width("primary")/4*3):
        with dpg.tab_bar(label = "Graph View Bar", tag = "view_bar"):
            with dpg.tab(label = "Main View", tag = "main_view"):
                    with dpg.drawlist(label = "Main", tag = "main", width = 600, height = 600, pos = [0, 0]):
                        pass
        with dpg.group(horizontal=False):
            ## GUI::Info ##
            with dpg.group():
                with dpg.tab_bar(label = "Info Tab Bar", tag = "info_bar"):
                    with dpg.tab(label = "Info", tag = "info"):
                        dpg.add_text(default_value="This is info text.")

            ## GUI::Constants / Control ##
            with dpg.group():
                with dpg.tab_bar(label = "Control Tab Bar", tag = "control_bar"):
                    with dpg.tab(label = "Control", tag = "control"):
                        dpg.add_slider_double(label="c1", tag="c1", callback=constant_cb, default_value=Force.constants[1], min_value=0.001, max_value=10)
                        dpg.add_slider_double(label="c2", tag="c2", callback=constant_cb, default_value=Force.constants[2], min_value=1, max_value=1000)
                        dpg.add_slider_double(label="c3", tag="c3", callback=constant_cb, default_value=Force.constants[3], min_value=1, max_value=10000000)
                        dpg.add_slider_double(label="c4", tag="c4", callback=constant_cb, default_value=Force.constants[4], min_value=0, max_value=100)

            ## GUI::Terminal ##
            with dpg.group():
                with dpg.tab_bar(label = "Terminal Tab Bar", tag = "terminal_bar"):
                    with dpg.tab(label = "Terminal", tag = "terminal_tab"):
                        dpg.add_input_text(tag='terminal', multiline=True, default_value="")
                        dpg.add_button(tag="terminal_run", label="Run", callback=terminal_callback)

# dpg.toggle_viewport_fullscreen()

################# Editor Register #################
ed_reg = EditorRegister()
# g = nx.grid_2d_graph(m = 7, n = 7)
# main_ed = ed_reg.add_editor(window="main", graph = g)


# main_ed.set_camera(0.1, [0, 0])
main_ed = ed_reg.add_editor(window="main")

main_ed.add_node(1, pos=[0, 0], color = (0, 0, 255))
main_ed.add_node(2, pos=[700, 400], color = (0, 255, 255))
main_ed.add_node(3, pos=[300, 500], color = (0, 255, 0))
main_ed.add_node(4, pos=[30, 500], color = (255, 255, 0))
main_ed.add_node(5, pos=[300, 50], color = (255, 0, 0))

main_ed.add_edge(3,5)
main_ed.add_edge(2,5)
main_ed.add_edge(4,5)
main_ed.add_edge(3,2)
main_ed.add_edge(1,4)

# write a piece of code that generates colors?

### test algoritms ###
tested = False
def test_alg():
    alg.hl_shortest_path(main_ed,3,4)
    # print(alg.eccentricity(main_ed, 2))
    alg.hl_eccentricity(main_ed, 2)
    alg.hl_periphery(main_ed)

#### Actions and HotKeys ###
hkhandler = HKHandler()
with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=hkhandler.update_wheel)


################# Main Loop #################
dpg.show_viewport()
dpg.set_primary_window("primary", True)
while dpg.is_dearpygui_running():
    hkhandler.update()
    # print('hkhandler.mouse_down_mode', hkhandler.mouse_down_mode)
    # print("hkhandler", hkhandler)
    # if hkhandler.release: print("RELASED")
    for action in action_dict:
        for hk in action_dict[action]:
            if hkhandler.is_hk_active(hk):
                # print("hk", hk)
                # print("action", action)
                # print("mode", hkhandler.mouse_down_mode)
                action_func_dict[action](hkhandler)

    for ed in ed_reg.editors.values():
        ed.update_window()

    # if not tested:
    #     tested = True
    #     test_alg()
    dpg.render_dearpygui_frame()

dpg.destroy_context()






