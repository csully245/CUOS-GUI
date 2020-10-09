import config
import Helpers

from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import os
from matplotlib import pyplot as plt

#-------------------------------------------------
# Helper functions
#-------------------------------------------------

def max_num_in_dir(path):
    '''
    Returns the max numbered file in a given directory
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
    if (len(nums) == 0):
        return None
    else:
        return max(nums)

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
    
#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------  

class UI(tk.Frame):
    '''
    Frame for displaying a single image
    '''
    #-------------------------
    # Update commands
    #-------------------------  
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
        Updates image to selected image in entry
        '''
        # LATER: add case for default image on failure

        # Gets diagnostic path
        root_path = self.options_dirs[self.diagnostic.get()]
        if not (os.path.isdir(root_path)):
            Helpers.Error_Window("Invalid diagnostic path.")
            print(self.diagnostic.get())
            return

        # Gets path of number equal to entry
        pics = os.listdir(root_path) # WARNING: Assumes dir contains only pics
        if (len(pics) == 0):
            Helpers.Error_Window("No data available.")
            return
        num = self.entry_num.get()
        valid_pics = []
        for pic in pics:
            if num in pic:
                valid_pics.append(pic)
        if (len(valid_pics) > 1):
            text = "Multiple pics with shot number '"
            text += num + "'."
            Helpers.Error_Window(text)
            return
        elif (len(valid_pics) == 0):
            text = "No pics with shot number '"
            text += num + "'."
            Helpers.Error_Window(text)
            return
        path = os.path.join(root_path, valid_pics[0])

        # Updates image
        self.img = Helpers.load_image(path)
        self.lbl_img.grid_forget()
        self.lbl_img = tk.Label(self, image=self.img)
        self.lbl_img.grid(row=0, column=0)

    def update_buttonstate(self):
        '''
        Updates whether the left-right image buttons are clickable or not
        '''
        if (self.img_num == "0000"):
            self.arrow_left.config(state='disabled')
        else:
            self.arrow_left.config(state='active')
        try:
            max_num = convert_to_4_digit(max_num_in_dir(self.diagnostic.get()))
        except:
            max_num = convert_to_4_digit(max_num_in_dir("./shotrundir/Example"))
        if (self.img_num == max_num):
            self.arrow_right.config(state='disabled')
        else:
            self.arrow_right.config(state='active')

    def update_all(self):
        '''
        Calls all widget update commands
        '''
        self.update_options()
        self.update_dropdown()
        self.update_image()
        self.update_buttonstate()

    #-------------------------
    # Other internal functions
    #-------------------------
    
    def move_img_left(self):
        '''
        Moves to previous image, if image exists
        Updates button ability
        '''
        # Updates img_num and entry
        if (self.img_num == "" or self.img_num == "0000"):
            return
        else:
            self.img_num = int(self.img_num) - 1
            self.img_num = convert_to_4_digit(self.img_num)
        self.entry_num.delete(0, tk.END)
        self.entry_num.insert(0, self.img_num)
        
        # Updates buttons
        self.update_buttonstate()
        
        # Loads new image
        self.update_image()
            
    def move_img_right(self):
        '''
        Moves to next image, if image exists
        Updates button ability
        '''
        # Updates img_num and entry
        max_num = convert_to_4_digit(max_num_in_dir("./shotrundir/Example"))
        if (self.img_num == "" or self.img_num == max_num):
            return
        else:
            self.img_num = int(self.img_num) + 1
            self.img_num = convert_to_4_digit(self.img_num)
        self.entry_num.delete(0, tk.END)
        self.entry_num.insert(0, self.img_num)
        
        # Updates buttons
        self.update_buttonstate()
        
        # Loads new image
        self.update_image()

    #-------------------------
    # init
    #-------------------------
    
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)

        # Image and colorbar
        self.img = Helpers.load_image("assets/20170607_XRAYCCD_s024.tif", k=10)
        self.lbl_img = tk.Label(self, image=self.img)
        self.lbl_img.grid(row=0, column=0)

        # Frames
        self.fr_controls = tk.Frame(self)
        self.fr_controls.grid(row=1, column=0)

        # Drop-Down Diagnostic Select
        '''
        Drop-down menu that gives a list of subfolders in the shot run
        directory. Intended to be used to select a diagnostic data folder
        to display pictures
        '''
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
        '''
        Button for manually reloading the image
        '''
        btn_load = tk.Button(self.fr_controls, text="Load",
                             command=lambda: self.update_image())
        btn_load.grid(row=1, column=0)

        # Image select 
        '''
        Text entry box for manually entering the desired picture number
        Buttons for moving to the previous or next picture
        '''
        self.entry_num = tk.Entry(self.fr_controls)
        max_img = max_num_in_dir("./shotrundir/Example")
        if (max_img == None):
            self.img_num = ""
            #self.entry_num.config(state='disabled')
        else:
            self.img_num = "0000"
        self.entry_num.delete(0, tk.END)
        self.entry_num.insert(0, self.img_num)
        self.entry_num.grid(row=1, column=2)

        self.arrow_left = tk.Button(self.fr_controls, text="Previous Image",
                                    command=lambda: self.move_img_left())
        self.arrow_right = tk.Button(self.fr_controls, text="Next Image",
                                    command=lambda: self.move_img_right())
        self.update_buttonstate()
        self.arrow_left.grid(row=1, column=1)
        self.arrow_right.grid(row=1, column=3)

        
        # Can we expect there to be a "default values" folder in shotrundir?
        # I could make it upon init
        

#-------------------------------------------------
# Execution
#-------------------------------------------------

def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()
        
