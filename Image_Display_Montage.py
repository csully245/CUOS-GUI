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
    
    #-------------------------
    # Update commands
    #-------------------------  
    def _update_options(self):
        '''
        Updates diagnostic options
        '''
        self.options = ["Select a Diagnostic"]
        self.options_dirs = {"Select a Diagnostic":"./"}
        shotrundir = Helpers.get_from_file("shotrundir", "setup.json")
        for dr in os.listdir(shotrundir):
            #if (os.path.isdir(dr)):
            path = os.path.join(shotrundir, dr)
            self.options_dirs[dr] = path
            self.options.append(dr)

    def _update_dropdown(self):
        '''
        Updates dropdown for new options
        '''
        self.diagnostic.set(self.options[0])

        self.drop_diag.pack_forget()
        self.drop_diag = ttk.Combobox(self.fr_controls, width=27,
                                      textvariable=self.diagnostic)
        self.drop_diag['values'] = tuple(self.options)
        self.drop_diag.grid(row=0, column=0)

    # Associated with self.load()
    def _get_img_paths(self):
        ''' Returns a list of all pictures in diagnostic dir '''
        root_path = self.options_dirs[self.diagnostic.get()]
        if not (os.path.isdir(root_path)):
            Helpers.Notice_Window("Error: Invalid diagnostic path.")
            return [""]
        else:
            imgs = os.listdir(root_path)
            out = []
            for img in imgs:
               out.append(root_path + "/" + img)
            return out
            # WARNING: Assumes dir contains only pics
        
    def load(self, img_num):
        ''' Updates images to match shot num '''
        img_paths = self._get_img_paths()
        count = 1
        for img_lbl in self.img_lbls:
            # Finds image
            num_str = "-" + Helpers.to_4_digit(img_num)
            img_path = "assets/CUOS-med.png"
            for path in img_paths:
                if num_str in path:
                    img_path = path
                    break
            img = Helpers.load_image(img_path)
            
            # Replaces image
            img_lbl.grid_forget()
            lbl_img = tk.Label(self, image=img)
            lbl_img.grid(row=count, column=0)
            
            # Moves to previous image
            img_num -= 1
            count += 1

    #-------------------------
    # init
    #-------------------------
    def __init__(self, master, k=1, **options):
        tk.Frame.__init__(self, master, **options)
        self.fr_controls = tk.Frame(self)
        self.fr_controls.grid(row=0, column=0)
        
        # Images
        self.img_lbls = []
        self.img = Helpers.load_image("assets/CUOS-med.png", k=k)
        for i in range(3):
            img_lbl = tk.Label(self, image=self.img)
            img_lbl.grid(row=i+1, column=0)
            self.img_lbls.append(img_lbl)

        # Drop-Down Diagnostic Select 
        self.options = []
        self.options_dirs = dict()
        self._update_options()
        
        self.diagnostic = tk.StringVar()
        self.diagnostic.set(self.options[0])
        
        self.drop_diag = ttk.Combobox(self.fr_controls, width=27,
                                      textvariable=self.diagnostic)
        self.drop_diag['values'] = tuple(self.options)
        self.drop_diag.grid(row=0, column=0, columnspan=2)

class UI(tk.Frame):
    '''
    Frame for displaying images of multiple diagnostics, ready to be
    continually updated as more data is ready
    '''
    def _set_shot_num(self, num):
        ''' Sets number stored in shot number entry to num'''
        self.entry_num.delete(0, tk.END)
        self.entry_num.insert(0, str(num))
    
    def add_diagnostic(self, btn=True, k=1):
        ''' Adds a column for three images of one diagnostic '''
        if btn:
            self.num_diagnostics += 1
        k = 3 / self.num_diagnostics
        col = Diagnostic_Col(self.fr_diags, k=k)
        col.grid(row=0, column=len(self.diagnostics))
        self.diagnostics.append(col)

        if btn:
            self.refresh_diagnostics()
    
    def refresh_diagnostics(self):
        '''
        Reloads all diagnostics, including to proper scale factor
        '''
        for diag in self.diagnostics:
            diag.destroy()
        num = self.num_diagnostics
        for _ in range(num):
            self.add_diagnostic(btn=False)

    def remove_diagnostic(self):
        ''' Removes the rightmost diagnostic column '''
        if (self.num_diagnostics < 1):
            Helpers.Error_Window("No diagnostics to remove.")
            return
        self.num_diagnostics -= 1
        self.diagnostics[-1].destroy()
        del self.diagnostics[-1]
        self.refresh_diagnostics()
        #NOTE: this will undo any picture settings. Use workspaces?

    def load_images(self):
        ''' Updates each diagnostic column to match shot num '''
        for diag in self.diagnostics:
            shot_num = int(self.entry_num.get())
            diag.load(shot_num)
    
    def advance_shot(self):
        ''' Advances images to next shot '''
        shot_num = int(self.entry_num.get())
        self._set_shot_num(shot_num + 1)
        self.load_images()
    
    def __init__(self, master, num_diagnostics=3, **options):
        tk.Frame.__init__(self, master, **options)

        # Display diagnostic columns
        self.fr_diags = tk.Frame(self)
        self.fr_diags.grid(row=0, column=0, columnspan=num_diagnostics)
        self.num_diagnostics = num_diagnostics
        self.diagnostics = []
        for x in range(num_diagnostics):
            self.add_diagnostic(btn=False)

        # Diagnostic controls
        self.fr_controls = tk.Frame(self)
        self.fr_controls.grid(row=1, column=0)

        btn_add_diag = tk.Button(self.fr_controls, text="Add diagnostic",
                                 command=lambda: self.add_diagnostic())
        btn_add_diag.pack()
        
        btn_rm = tk.Button(self.fr_controls, text="Remove Diagnostic",
                           command=lambda: self.remove_diagnostic())
        btn_rm.pack()

        # Shot number updating
        self.fr_shot = tk.Frame(self)
        self.fr_shot.grid(row=1, column=1)
        
        self.entry_num = tk.Entry(self.fr_shot)
        self._set_shot_num(0)
        self.entry_num.pack()

        self.btn_load = tk.Button(self.fr_shot, text="Load",
                                  command=lambda: self.load_images())
        self.btn_load.pack()

        self.btn_advance = tk.Button(self.fr_shot, text="Advance Shot",
                                     command=lambda: self.advance_shot())
        self.btn_advance.pack()

        
def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.mainloop()
        
