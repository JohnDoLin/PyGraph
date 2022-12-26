from Editor.Hotkey import Hotkey

hk1 = Hotkey(mouse = {0})
hk2 = Hotkey(wheel = True)
enter = Hotkey(kbd = {13})
ctrl_click = Hotkey(mouse = {0}, kbd = {17})

action_dict = {"pan": [hk1],
                "zoom": [hk2],
                "drag_node": [hk1],
                # "eval_terminal": [enter],
                "add_node": [ctrl_click],
                "delete_node": [ctrl_click],
                }


