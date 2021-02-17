import Helpers
import Image_Options_Menu

from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import os
from matplotlib import pyplot as plt
  
#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------  

class UI(tk.Frame):
    '''
    Frame for displaying a single image
    '''
    #-------------------------
    # init
    #-------------------------
    
    def __init__(self, master, scale=3, **options):
        tk.Frame.__init__(self, master, **options)

        self.scale = scale

        # Image and colorbar
        self.img_path = Helpers.default_img_path
        self.wgt_img, self.img = Helpers.load_image(self.img_path, self,
                                                    k=scale)
        self.wgt_img.grid(row=0, column=0)
        
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
                             command=lambda: self.load_btn())
        btn_load.grid(row=1, column=0)

        # Image select 
        '''
        Text entry box for manually entering the desired picture number
        Buttons for moving to the previous or next picture
        '''
        self.entry_num = tk.Entry(self.fr_controls)
        self.set_shot_num(0)
        self.entry_num.grid(row=1, column=2)

        self.arrow_left = tk.Button(self.fr_controls, text="Previous Image",
                                    command=lambda: self.move_img_left())
        self.arrow_right = tk.Button(self.fr_controls, text="Next Image",
                                    command=lambda: self.move_img_right())
        self.update_buttonstate()
        self.arrow_left.grid(row=1, column=1)
        self.arrow_right.grid(row=1, column=3)

        # Image options
        self.fr_options = Image_Options_Menu.UI(self)
        self.fr_options.grid(row=2, column=0, columnspan=2, pady=2)
    
    #-------------------------
    # workspace
    #-------------------------
    def load_from_workspace(self, workspace):
        '''
        Loads default data from input values generated from selected workspace
        .json file
        Workspace: dict containing diagnostic name and image number
        '''
        self.diagnostic.set(workspace["diagnostic"])
        self.entry_num.delete(0, tk.END)
        self.entry_num.insert(0, workspace["entry_num"])

    def get_workspace(self):
        '''
        Returns all variables needed to later recreate an identical frame
        '''
        workspace = {
            "diagnostic": self.diagnostic.get(),
            "entry_num": self.entry_num.get()
            }
        return workspace
    
    #-------------------------
    # Update commands
    #-------------------------  
    def update_options(self):
        '''
        Updates diagnostic options
        '''
        self.options = ["Select a Diagnostic"]
        self.options_dirs = {"Select a Diagnostic":"./"}
        shotrundir = Helpers.get_from_file("shotrundir")
        for dr in os.listdir(shotrundir):
            #if (os.path.isdir(dr)):
            path = os.path.join(shotrundir, dr)
            self.options_dirs[dr] = path
            self.options.append(dr)

    def update_dropdown(self):
        '''
        Updates dropdown for new options
        '''
        self.drop_diag.pack_forget()
        self.drop_diag = ttk.Combobox(self.fr_controls, width=27,
                                      textvariable=self.diagnostic)
        self.drop_diag['values'] = tuple(self.options)
        self.drop_diag.grid(row=0, column=0, columnspan=2)
        if (self.diagnostic not in self.drop_diag['values']):
            self.diagnostic.set(self.options[0])
        
    def get_img_path(self):
        ''' Returns the path of the desired image '''
        # Get shot run directory
        root_path = Helpers.get_from_file("shotrundir")
        
        # Get diagnostic path
        root_path = self.options_dirs[self.diagnostic.get()]
        if not (os.path.isdir(root_path)):
            error_text = "Diagnostic path does not exist:\n"
            error_text += root_path
            Helpers.Error_Window(error_text)
            return "./"

        # Get path of pic with number equal to entry
        pics = os.listdir(root_path) # WARNING: Assumes dir contains only pics
        if (len(pics) == 0):
            Helpers.Error_Window("No data available.")
            return "./"
        num = "s" + Helpers.to_3_digit(int(self.entry_num.get()))
        valid_pics = []
        for pic in pics:
            if num in pic:
                valid_pics.append(pic)
        if (len(valid_pics) > 1):
            text = "Multiple pics with shot number '"
            text += num + "'."
            Helpers.Error_Window(text)
            return ""
        elif (len(valid_pics) == 0):
            text = "No pics with shot number '"
            text += num + "'."
            Helpers.Error_Window(text)
            return "./"
        else:
            pic_path = valid_pics[0]
            self.img_path = os.path.join(root_path, pic_path)
            return self.img_path

    def update_image(self):
        '''
        Updates image to selected image in entry
        '''
        # Locate image path
        self.img_path = self.get_img_path()
        if not (os.path.isfile(self.img_path)):
            error_text = "Image path does not exist: " + self.img_path
            Helpers.Error_Window(error_text)
            self.img_path = Helpers.default_img_path

        # Plot
        vmin, vmax, flipud = self.fr_options.get()
        size = 700
        self.wgt_img.grid_forget()
        garbage_img = self.img
        if (self.img_path == Helpers.default_img_path):
            self.wgt_img, self.img = Helpers.load_image(self.img_path,
                                                self, recolor=False)
        else:
            self.wgt_img, self.img = Helpers.plot_image(self.img_path,
                                                self, recolor=True,
                                                vmin=vmin, vmax=vmax,
                                                flipud=flipud, base=size)
        self.wgt_img.grid(row=0, column=0)
        Helpers.delete_img(garbage_img)

    def update_buttonstate(self):
        '''
        Updates whether the left-right image buttons are clickable or not
        '''
        path = Helpers.get_from_file("shotrundir")
        path = os.path.join(path, self.diagnostic.get())
        if not (os.path.isdir(path)):
            self.arrow_left.config(state='disabled')
            self.arrow_right.config(state='disabled')
            return

        # Left button
        img_num = int(self.entry_num.get())
        if (img_num == 0):
            self.arrow_left.config(state='disabled')
        else:
            self.arrow_left.config(state='active')
        
        # Right button
        max_num = Helpers.max_num_in_dir(path)
        if (img_num == max_num):
            self.arrow_right.config(state='disabled')
        else:
            self.arrow_right.config(state='active')

    def update_all(self):
        '''
        Calls all widget update commands
        '''
        self.update_options()
        self.update_dropdown()
        self.update_buttonstate()

    #-------------------------
    # Other internal functions
    #-------------------------
    
    def move_img_left(self):
        '''
        Moves to previous image, if image exists
        Updates button ability
        '''
        # Update img_num and entry
        img_num = int(self.entry_num.get())
        if (img_num == 0):
            return
        else:
            self.set_shot_num(img_num-1)
        
        # Update buttons
        self.update_buttonstate()
        
        # Load new image
        self.update_image()
            
    def move_img_right(self):
        '''
        Moves to next image, if image exists
        Updates button ability
        '''
        # Update img_num and entry
        img_num = int(self.entry_num.get())
        path = Helpers.get_from_file("shotrundir")
        path = os.path.join(path, self.diagnostic.get()) 
        max_num = Helpers.max_num_in_dir(path)
        if (img_num == max_num):
            return
        else:
            self.set_shot_num(img_num+1)
        
        # Update buttons
        self.update_buttonstate()
        
        # Load new image
        self.update_image()

    def set_shot_num(self, num):
        ''' Sets number stored in shot number entry to num'''
        self.entry_num.delete(0, tk.END)
        self.entry_num.insert(0, str(num))

    def load_btn(self):
        ''' Commands to be executed on pressing 'load' button '''
        self.update_image()
        self.update_buttonstate()

#-------------------------------------------------
# Execution
#-------------------------------------------------

def test():
    root = tk.Tk()
    gui = UI(root, scale=1)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()