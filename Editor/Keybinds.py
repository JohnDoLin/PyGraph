from Editor.Hotkey import Hotkey

down = Hotkey(mouse = {0})
down_5 = Hotkey(mouse = {0, 5})
scroll = Hotkey(wheel = True)



# enter = Hotkey(kbd = {13})
# ctrl_press = Hotkey(mouse = {0}, kbd = {17})
# shift_press = Hotkey(mouse = {0}, kbd = {16})

ctrl_press = Hotkey(mouse = {0}, kbd = {17}, press = True)

ctrl_shift_press = Hotkey(mouse = {0}, kbd = {17, 16}, press = True)

alt_down = Hotkey(mouse = {0}, kbd = {18})
alt_down_5 = Hotkey(mouse = {0, 5}, kbd = {18})
alt_release = Hotkey(kbd = {18}, release = True)

alt_shift_down = Hotkey(mouse = {0}, kbd = {16, 18})
alt_shift_down_5 = Hotkey(mouse = {0, 5}, kbd = {16, 18})
alt_shift_release = Hotkey(kbd = {16, 18}, release = True)

# shift_press = Hotkey(mouse = {0}, kbd = {16})
# shift_press_5 = Hotkey(mouse = {0, 5}, kbd = {16})

# ctrl_release = Hotkey(kbd = {17}, release = True)
# ctrl_release_5 = Hotkey(mouse = {0, 5}, kbd = {17}, release = True)

# shift_release = Hotkey(kbd = {16}, release = True)
# shift_release_5 = Hotkey(mouse = {0, 5}, kbd = {16}, release = True)

# unstrict_release = Hotkey(strict = False, release = True)

action_dict = {
                "pan": [down, down_5],
                "zoom": [scroll],
                "drag_node": [down, down_5],

                "add_node": [ctrl_press],
                "delete_node": [ctrl_shift_press],

                "add_edge": [alt_down, alt_release, alt_down_5],
                "delete_edge": [alt_shift_down, alt_shift_release, alt_shift_down_5],
                }


