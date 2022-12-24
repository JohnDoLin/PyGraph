from Editor.EditorRegister import EditorRegister

def pan(hkhandler):
    if (len(hkhandler.hover_list) != 0 
        and len(hkhandler.hover_list["main"]["node"]) == 0
        and hkhandler.is_dragging
        ):
        print("pan!!!")
    
def drag_node(hkhandler):
    pass

def zoom(hkhandler):
    pass



action_func_dict = {"pan": pan,
                    "zoom": zoom,
                    "drag_node": drag_node
                    }
