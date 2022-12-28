import dearpygui.dearpygui as dpg
import Editor.Hotkey as Hotkey
from Editor.EditorRegister import EditorRegister as Edreg
import time
from Structure.Vec2 import Vec2

class HKHandler:
    dragging_threashold = 0.001
    dragging_mouse_btn = dpg.mvMouseButton_Left
    # check EditorRegister.editors

    # mouse_calibration = [8, 12]
    mouse_calibration = [8, 31]

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

        self.delta = [0, 0]

        self.wheel_sum = 0
        self.wheel_speed = 0
        self.is_wheel_updated = False

        self.mouse_down_mode = None
        self.mouse_down_data = None
    
        self.selection = (None, None, None)

    def __str__(self):
        return f'''HKHandler(
                            mouse = {self.mouse},
                            kbd = {self.kbd},
                            pos = {self.pos},
                            is_dragging = {self.is_dragging},
                            down = {self.down},
                            press = {self.press},
                            press_pos = {self.press_pos},
                            press_tp = {self.press_tp},
                            release = {self.release},
                            release_pos = {self.release_pos},
                            release_tp = {self.release_tp},
                            delta = {self.delta},
                            wheel_sum = {self.wheel_sum},
                            wheel_speed = {self.wheel_speed},
                            is_wheel_updated = {self.is_wheel_updated},
                            mouse_down_mode = {self.mouse_down_mode},
                            mouse_down_data = {self.mouse_down_data},
                            )'''
    def __repr__(self):
        return self.__str__()

    def update_wheel(self, sender, data):
        # print("data", data)
        # self.is_wheel_updated = True
        self.wheel_sum += data

    def update(self):
        # Global -- kbd
        self.kbd = set()
        for key in range(0, 300):
            if dpg.is_key_down(key):
                self.kbd.add(key)

        # Global -- mouse position
        print(dpg.get_drawing_mouse_pos(), dpg.get_mouse_pos(local=False))
        self.pos = dpg.get_mouse_pos(local=False)
        self.pos = [self.pos[0] - HKHandler.mouse_calibration[0], self.pos[1] - HKHandler.mouse_calibration[1]]

        # Global -- mouse keys and press / release
        if self.release:
            self.mouse_down_mode = None
            self.mouse_down_data = None
            
        self.mouse = set()
        for btn in range(0, 10):
            if dpg.is_mouse_button_down(btn):
                self.mouse.add(btn)

        self.press = False
        if len(self.mouse) != 0 and self.down == False:
            self.down = True
            self.press_pos = self.pos
            self.press_tp = time.time()
            self.press = True

        self.release = False

        if len(self.mouse) == 0 and self.down == True:
            # print("RELEASED")
            self.down = False
            self.press_pos = self.pos
            self.release_tp = time.time()
            self.release = True

        # Global -- mouse wheel
        self.is_wheel_updated = False
        if self.wheel_sum != 0:
            self.wheel_speed = self.wheel_sum
            self.is_wheel_updated = True
        self.wheel_sum = 0


        # Global -- mouse dragging
        # self.delta = dpg.get_mouse_drag_delta() ## Bad :(
        self.is_dragging = False
        # if dpg.is_mouse_button_dragging(HKHandler.dragging_mouse_btn, HKHandler.dragging_threashold):
        if self.down and (Vec2(self.press_pos) - Vec2(self.pos)).norm() >= HKHandler.dragging_threashold:  
            self.is_dragging = True
            self.deltadelta = [self.pos[0] - self.press_pos[0] - self.delta[0], self.pos[1] - self.press_pos[1] - self.delta[1]]
            self.delta = [self.pos[0] - self.press_pos[0], self.pos[1] - self.press_pos[1]]
            # print("self.mous_down_mode", self.mouse_down_mode)

        # Global -- mouse hovering
        self.hover_list = dict()
        # Window
        for ed in Edreg.editors.values():
            window = ed.window
            p = self.pos
            sz = dpg.get_item_rect_size(window)
            win_pos = dpg.get_item_pos(window)
            if 0 <= p[0] - win_pos[0] <= sz[0] and 0 <= p[1] - win_pos[1] <= sz[1]:
                self.hover_list[window] = {"node": [], "edge": []}
                # Drawing
                for node_name, node in ed.node_dict.items():
                    if node.is_hovered(self, offset = ed.offset, scale = ed.scale):
                        self.hover_list[window]["node"].append(node_name)
                for node_pair, edge in ed.edge_dict.items():
                    if edge.is_hovered(self, offset = ed.offset, scale = ed.scale):
                        self.hover_list[window]["edge"].append(node_pair)
        # print('self.hover_list', self.hover_list)


        # print("dpg.get_item_rect_size(window)", dpg.get_item_rect_size(window))
        # print(self.hover_list)


        # if len(self.mouse) != 0:
        #     print("mouse", self.mouse)
        # if len(self.kbd) != 0:
        #     print("kbd", self.kbd)

    def is_hk_active(self, hk: Hotkey):
        if hk.strict:
            if (
                (self.mouse == hk.mouse)
                and (self.kbd == hk.kbd)
                and (not hk.wheel or self.is_wheel_updated)
                and (not hk.release or self.release)
                and (not hk.press or self.press)
                ):
                return True
        else:
            if (
                (self.mouse >= hk.mouse)
                and (self.kbd >= hk.kbd)
                and (not hk.wheel or self.is_wheel_updated)
                and (not hk.release or self.release)
                and (not hk.press or self.press)
                ):
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


