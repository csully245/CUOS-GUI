import config
import Helpers

from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import os

#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------

class UI(tk.Frame):
    '''
    Frame for displaying a single image
    '''
    def update_options(self):
        '''
        Updates diagnostic options
        '''
        self.options = ["Select a Diagnostic"]
        self.options_dirs = {"Select a Diagnostic":"./"}
        for dr in os.listdir(config.shot_run_dir):
            if (os.path.isdir(dr)):
                path = os.path.join(config.shot_run_dir, dr)
                self.options_dirs[dr] = path
                self.options.append(dr)
    
    def update_image(self):
        '''
        Updates image to alphabetically-last in selected diagnostic
        '''
        self.lbl_img.grid_forget()
        
        root_path = self.options_dirs[self.diagnostic.get()]
        if not (os.path.isdir(root_path)):
            Helpers.Notice_Window("Error: Invalid diagnostic path.")
            print(self.diagnostic.get())
            return
        pics = os.listdir(root_path) # WARNING: Assumes dir contains only pics
        if (len(pics) == 0):
            Helpers.Notice_Window("Error: No data available.")
            return
        pic_path = sorted(pics)[-1]
        path = os.path.join(root_path, pic_path)
        
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.lbl_img = tk.Label(self, image=self.img)
        self.lbl_img.grid(row=0, column=0)
            
        
    def __init__(self, master, **options):
        tk.LabelFrame.__init__(self, master, **options)

        self.img = ImageTk.PhotoImage(Image.open("assets/default-image-s.png"))
        self.lbl_img = tk.Label(self, image=self.img)
        self.lbl_img.grid(row=0, column=0)

        self.fr_controls = tk.Frame(self)
        self.fr_controls.grid(row=1, column=0)

        # Drop-Down Diagnostic Select 
        self.options = []
        self.options_dirs = dict()
        self.update_options()
        
        self.diagnostic = tk.StringVar()
        self.diagnostic.set(self.options[0])
        
        self.drop_diag = ttk.Combobox(self.fr_controls, width=27,
                                      textvariable=self.diagnostic)
        self.drop_diag['values'] = tuple(self.options)
        self.drop_diag.pack()

        # Other
        btn_load = tk.Button(self.fr_controls, text="Load",
                             command=lambda: self.update_image())
        btn_load.pack()


        
def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.mainloop()
        
