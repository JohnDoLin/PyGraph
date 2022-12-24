from Editor.Hotkey import Hotkey

hk1 = Hotkey(mouse = {0}, kbd = set())
hk2 = Hotkey(mouse = {5}, kbd = set())
action_dict = {"pan": [hk1],
                "zoom": [hk2],
                "drag_node": [hk1]
                }


