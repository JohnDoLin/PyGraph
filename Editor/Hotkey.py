class Hotkey:
    def __init__(self, **args):
        # ["click", "double_click", "drag", "right_click"]
        self.mouse = args.get("mouse", set()) 
        self.kbd = args.get("kbd", set())
        self.wheel = args.get("wheel", False)
        self.release = args.get("release", False)
        self.strict = args.get("strict", True)
        self.press = args.get("press", False)
    def __str__(self):
        return f"Hotkey(mouse = {self.mouse}, kbd = {self.kbd}, wheel = {self.wheel}, release = {self.release})"

    def __repr__(self) -> str:
        return self.__str__()