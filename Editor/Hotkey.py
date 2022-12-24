class Hotkey:
    def __init__(self, **args):
        # ["click", "double_click", "drag", "right_click"]
        self.mouse = args.get("mouse", set()) 
        self.kbd = args.get("kbd", set())
        self.wheel = args.get("wheel", False)