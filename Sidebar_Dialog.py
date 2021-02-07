import Startup

import tkinter as tk

class UI(tk.Frame):
    '''
    Frame for quick user questions.
    '''
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)
        self.frames = []
        self.add_frame("startup_menu")
    
    def add_frame(self, name):
        ''' Adds frame with name 'name' '''
        if (name == "startup_menu"):
            new_frame = Startup.Startup_Menu(self)
            self.frames.append(new_frame)
            self.frames[-1].grid(row=len(self.frames), column=0)

    def clear(self):
        ''' Removes all frames. Still available for data access '''
        for frame in self.frames:
            frame.grid_forget()

def test():
    root = tk.Tk()
    fr = UI(root)
    fr.add_frame("startup_menu")
    fr.pack()
    root.mainloop()