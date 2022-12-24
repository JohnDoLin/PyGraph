import dearpygui.dearpygui as dpg
import Editor.Hotkey as Hotkey
from Editor.EditorRegister import EditorRegister as Edreg
import time

class HKHandler:
    dragging_threashold = 0.1
    dragging_mouse_btn = dpg.mvMouseButton_Left
    # check EditorRegister.editors

    mouse_calibration = [8, 12]
    def __init__(self):
        self.mouse = set()
        self.kbd = set()
        self.pos = None
        self.hover_list = dict()

        self.is_dragging = False

        self.down = False
        self.press = False
        self.press_pos = None
        self.press_tp = None
        self.release = False
        self.release_pos = None
        self.release_tp = None

    def update(self):
        # Global -- kbd
        self.kbd = set()
        for key in range(0, 300):
            if dpg.is_key_down(key):
                self.kbd.add(key)

        # Global -- mouse position
        # self.pos = dpg.get_mouse_pos(local=True)
        # self.pos = dpg.get_mouse_pos(local=False)
        self.pos = dpg.get_mouse_pos()
        self.pos = [self.pos[0] - HKHandler.mouse_calibration[0], self.pos[1] - HKHandler.mouse_calibration[1]]

        # Global -- mouse keys and press / release
        self.mouse = set()
        self.press = False
        self.release = False
        for btn in range(0, 10):
            if dpg.is_mouse_button_down(btn):
                self.mouse.add(btn)

        if len(self.mouse) != 0 and self.down == False:
            self.down = True
            self.press_pos = self.pos
            self.press_tp = time.monotonic_ns()
            self.press = True

        if len(self.mouse) == 0 and self.down == True:
            self.down = False
            self.press_pos = self.pos
            self.release_tp = time.monotonic_ns()
            self.release = True

        # Global -- mouse wheel


        # Global -- mouse dragging
        # self.delta = dpg.get_mouse_drag_delta() ## Bad :(
        self.is_dragging = False
        if dpg.is_mouse_button_dragging(HKHandler.dragging_mouse_btn, HKHandler.dragging_threashold):
            self.is_dragging = True
            self.delta = [self.pos[0] - self.press_pos[0], self.pos[1] - self.press_pos[1]]


        # Global -- mouse hovering
        self.hover_list = dict()
        # Window
        for ed in Edreg.editors:
            window = ed.window
            p = self.pos
            sz = dpg.get_item_rect_size(window)
            win_pos = dpg.get_item_pos(window)
            if 0 <= p[0] - win_pos[0] <= sz[0] and 0 <= p[1] - win_pos[1] <= sz[1]:
                self.hover_list[window] = {"node": [], "edge": []}
                # Drawing
                for node_name, node in ed.node_dict.items():
                    if node.is_hovered(self):
                        self.hover_list[window]["node"].append(node_name)
                for node_pair, edge in ed.edge_dict.items():
                    if edge.is_hovered(self):
                        self.hover_list[window]["edge"].append(node_pair)
        # print('self.hover_list', self.hover_list)


        # print("dpg.get_item_rect_size(window)", dpg.get_item_rect_size(window))
        # print(self.hover_list)


        # if len(self.mouse) != 0:
        #     print("mouse", self.mouse)
        # if len(self.kbd) != 0:
        #     print("kbd", self.kbd)

    def is_hk_active(self, hk: Hotkey):
        if (len(self.mouse)!=0 or len(self.kbd)!=0) and (self.mouse >= hk.mouse) and (self.kbd >= hk.kbd):
            return True
        return False




    # mouse_mode = None
    # mouse_data = None
    # def drag_handler(sender, app_data):
    # # editor_register
    #     if mouse_mode == None:
    #         # identify the position
    #         mouse_mode = "pan"
    #         mouse_data = [0, Vec2.Vec2([app_data[1], app_data[2]])]
    #     elif mouse_mode == "pan":
    #         # mouse_data = [register_index, original_mouse_pos]
    #         (editor_register[mouse_data[0]]
    #         ).set_camera(main_ed.scale, Vec2.Vec2(mouse_data[1]) - Vec2.Vec2([app_data[1], app_data[2]]))
    #     # print("sender", sender)
    #     # print("app_data", app_data)

    # def release_handler(sender, app_data):
    #     global mouse_mode, mouse_data   
    #     if mouse_mode == "pan":
    #         mouse_mode = None
    #         mouse_data = None


