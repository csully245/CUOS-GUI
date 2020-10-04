import config
import Helpers

from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import os

#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------

def min_num_in_dir(path):
    '''
    Returns the minimum numbered file in a given directory
    Expects all files in directory to be pics in convention: name-xxxx
    with xxxx representing number
    '''
    pic_names = os.listdir(path)
    nums = []
    for name in pic_names:
        pic = name.partition(".")[0]
        pic = pic.partition("-")[2]
        try:
            pic = int(pic)
            nums.append(pic)
        except:
            print("Bad filename: " + name)
        print()
    if (len(nums) == 0):
        return None
    else:
        return min(nums)

def convert_to_4_digit(num):
    '''
    Returns a 4-digit string of the input positive int
    Returns '9999' if num is more than four digits
    Returns '-001' if num is negative
    '''
    if (num < 0):
        return "-001"
    elif (num >= 9999):
        return "9999"
    elif (num > 999):
        return str(num)
    elif (num > 99):
        return "0" + str(num)
    elif (num > 9):
        return "00" + str(num)
    else:
        return "000" + str(num)
    

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
        self.drop_diag.grid(row=0, column=0, columnspan=2)
    
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
        
        self.img = Helpers.load_image(path)
        self.lbl_img = tk.Label(self, image=self.img)
        self.lbl_img.grid(row=0, column=0)
            
        
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)

        self.img = Helpers.load_image("assets/CUOS-med.png")
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
        self.drop_diag.grid(row=0, column=0, columnspan=2)

        # Image loading
        btn_load = tk.Button(self.fr_controls, text="Load",
                             command=lambda: self.update_image())
        btn_load.grid(row=1, column=0)

        self.entry_num = tk.Entry(self.fr_controls)
        min_img = min_num_in_dir(config.shot_run_dir)
        if (min_img == None):
            self.img_num = ""
            self.entry_num.config(state='disabled')
        else:
            self.img_num = convert_to_4_digit(min_img)
        self.entry_num.insert(0, self.img_num)
        self.entry_num.grid(row=1, column=1)

        
def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()
        
