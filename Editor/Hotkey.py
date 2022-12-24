class Hotkey:
    def __init__(self, **args):
        # ["click", "double_click", "drag", "right_click"]
        self.mouse = args["mouse"] 
        self.kbd = args["kbd"]
        pass