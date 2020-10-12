import tkinter as tk

class UI(tk.Frame):
    '''
    Frame for displaying use instructions
    '''
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)
        
        self.lbl_title = tk.Label(self, text="Welcome to CUOS!")
        self.lbl_title.pack()

        instructions = "(Add instructions)"
        self.lbl_instructions = tk.Label(self, text=instructions)
        self.lbl_instructions.pack()

#-------------------------------------------------
# Execution
#-------------------------------------------------

def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()
        
