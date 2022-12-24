from Editor.Hotkey import Hotkey

hk1 = Hotkey(mouse = {0})
hk2 = Hotkey(wheel = True)


action_dict = {"pan": [hk1],
                "zoom": [hk2],
                "drag_node": [hk1]
                }


