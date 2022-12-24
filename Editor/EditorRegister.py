import Editor.Editor as Editor

class EditorRegister:
    editors = dict()

    def __init__(self):
        pass

    def add_editor(self, window = None, graph = None):
        ed = Editor.Editor(window, graph)
        self.editors[window] = ed
        return ed
    
    
    


