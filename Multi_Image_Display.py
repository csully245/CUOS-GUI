import config
import Helpers

from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import os

#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------  

class Diagnostic_Col(tk.Frame):
    '''
    Subframe for displaying three images of a single diagnostic
    '''
    def update_options(self):
        '''
        Updates diagnostic options
        '''
        self.options = ["Select a Diagnostic"]
        self.options_dirs = {"Select a Diagnostic":"./"}
        for dr in os.listdir(config.shot_run_dir):
            #if (os.path.isdir(dr)):
            path = os.path.join(config.shot_run_dir, dr)
            self.options_dirs[dr] = path
            self.options.append(dr)

    def update_dropdown(self):
        '''
        Updates dropdown for new options
        '''
        self.diagnostic.set(self.options[0])

        self.drop_diag.pack_forget()
        self.drop_diag = ttk.Combobox(self.fr_controls, width=27,
                                      textvariable=self.diagnostic)
        self.drop_diag['values'] = tuple(self.options)
        self.drop_diag.grid(row=0, column=0)
    
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
        
        self.img = Image.open("assets/default-image-s.png")
        self.img.resize((20, 12))
        self.img = ImageTk.PhotoImage(self.img)
        self.lbl_img = tk.Label(self, image=self.img)
        self.lbl_img.grid(row=1, column=0) 
        
    def __init__(self, master, k=0, max_width=None, max_height=None,
                 **options):
        tk.Frame.__init__(self, master, **options)
        self.fr_controls = tk.Frame(self)
        self.fr_controls.grid(row=0, column=0)
        
        # Images
        self.img_lbls = []
        self.img = Helpers.load_image("assets/CUOS-med.png", k, max_width,
                                      max_height)
        for i in range(3):
            img_lbl = tk.Label(self, image=self.img)
            img_lbl.grid(row=i+1, column=0)
            self.img_lbls.append(img_lbl)

        # Drop-Down Diagnostic Select 
        self.options = []
        self.options_dirs = dict()
        self.update_options()
        
        self.diagnostic = tk.StringVar()
        self.diagnostic.set(self.options[0])
        
        self.drop_diag = ttk.Combobox(self.fr_controls, width=27,
                                      textvariable=self.diagnostic)
        self.drop_diag['values'] = tuple(self.options)
        self.drop_diag.grid(row=0, column=0, columnspan=2)

        # Other
        btn_load = tk.Button(self.fr_controls, text="Load",
                             command=lambda: self.update_image())
        btn_load.grid(row=1, column=0)

class UI(tk.Frame):
    '''
    Frame for displaying several images at once
    '''
    def add_diagnostic(self, initial=False, k=1):
        if not initial:
            self.num_diagnostics += 1
        k = 3 / self.num_diagnostics
        col = Diagnostic_Col(self, k, max_width=self.max_img_width,
                             max_height = self.max_img_height)
        col.grid(row=0, column=len(self.diagnostics))
        self.diagnostics.append(col)

        if not initial:
            self.refresh_diagnostics()
    
    def refresh_diagnostics(self):
        for diag in self.diagnostics:
            diag.grid_forget()
        num = len(self.diagnostics)
        for _ in range(num):
            self.add_diagnostic(initial=True)

    def remove_diagnostic(self):
        self.num_diagnostics -= 1
        self.diagnostics[-1].destroy()
        del self.diagnostics[-1]
        self.refresh_diagnostics()
    
    def __init__(self, master, num_diagnostics=3, **options):
        tk.Frame.__init__(self, master, **options)

        self.max_img_height = 300
        self.max_img_width = 500

        self.num_diagnostics = num_diagnostics
        self.diagnostics = []
        for x in range(num_diagnostics):
            self.add_diagnostic(initial=True)

        self.fr_controls = tk.Frame(self)
        self.fr_controls.grid(row=1, column=0)

        btn_add_diag = tk.Button(self.fr_controls, text="Add diagnostic",
                                 command=lambda: self.add_diagnostic())
        btn_add_diag.pack()

        btn_refresh = tk.Button(self.fr_controls, text="Refresh",
                                command=lambda: self.refresh_diagnostics())
        btn_refresh.pack()

        btn_rm = tk.Button(self.fr_controls, text="Remove Diagnostic",
                           command=lambda: self.remove_diagnostic())
        btn_rm.pack()

        
def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.mainloop()
        
