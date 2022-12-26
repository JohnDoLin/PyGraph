from Editor.Hotkey import Hotkey

down = Hotkey(mouse = {0})
down_5 = Hotkey(mouse = {0, 5})
scroll = Hotkey(wheel = True)
# enter = Hotkey(kbd = {13})
# ctrl_press = Hotkey(mouse = {0}, kbd = {17})
# shift_press = Hotkey(mouse = {0}, kbd = {16})

ctrl_press = Hotkey(mouse = {0}, kbd = {17})
ctrl_press_5 = Hotkey(mouse = {0, 5}, kbd = {17})

shift_press = Hotkey(mouse = {0}, kbd = {16})
shift_press_5 = Hotkey(mouse = {0, 5}, kbd = {16})

ctrl_release = Hotkey(kbd = {17}, release = True)
ctrl_release_5 = Hotkey(mouse = {0, 5}, kbd = {17}, release = True)

shift_release = Hotkey(kbd = {16}, release = True)
shift_release_5 = Hotkey(mouse = {0, 5}, kbd = {16}, release = True)

# unstrict_release = Hotkey(strict = False, release = True)

action_dict = {
                "add_node": [ctrl_press],
                "delete_node": [shift_release],
                # "add_edge": [ctrl_press, ctrl_release, ctrl_press_5],
                # "delete_edge": [shift_press, shift_release, shift_press_5, shift_release_5],
                "pan": [down, down_5],
                "zoom": [scroll],
                "drag_node": [down, down_5],
                # "eval_terminal": [enter],
                }


