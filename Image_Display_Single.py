import Helpers

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
        #self.update_image()

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
        self.drop_diag.grid(row=0, column=0, columnspan=2)
        
    def _get_img_path(self):
        ''' Returns the path of the desired image '''
        # Gets shot run directory
        root_path = Helpers.get_from_file("shotrundir", "setup.json")
        
        # Gets diagnostic path
        root_path = self.options_dirs[self.diagnostic.get()]
        #root_path = os.path.join(root_path, diagnostic_path)
        if not (os.path.isdir(root_path)):
            error_text = "Diagnostic path does not exist:\n"
            error_text += root_path
            Helpers.Error_Window(error_text)
            return "./"

        # Gets path of number equal to entry
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
            if "._" in pic_path:
                pic_path = pic_path.partition("._")[2]
            while ("\\\\" in pic_path):
                part = pic_path.partition("\\")
                pic_path = part[0] + "/" + part[2]
            while ("\\" in pic_path):
                part = pic_path.partition("\\")
                pic_path = part[0] + "/" + part[2]
            self.img_path = os.path.join(root_path, pic_path)
            return self.img_path

    def _update_image(self):
        '''
        Updates image to selected image in entry
        '''
        self.img_path = self._get_img_path()
        self.lbl_img.grid_forget()
        Helpers.delete_img(self.img)
        self.lbl_img, self.img = Helpers.plot_image(self.img_path, self,
                                                    k=self.scale, recolor=True)
        self.lbl_img.grid(row=0, column=0)

    def _update_buttonstate(self):
        '''
        Updates whether the left-right image buttons are clickable or not
        '''
        path = Helpers.get_from_file("shotrundir", "Setup.json")
        path += "/" + self.diagnostic.get()
        if not (os.path.isdir(path)):
            self.arrow_left.config(state='disabled')
            self.arrow_right.config(state='disabled')
            return
        img_num = int(self.entry_num.get())
        if (img_num == 0):
            self.arrow_left.config(state='disabled')
        else:
            self.arrow_left.config(state='active')
        max_num = Helpers.max_num_in_dir(path)
        if (img_num == max_num):
            self.arrow_right.config(state='disabled')
        else:
            self.arrow_right.config(state='active')

    def update_all(self):
        '''
        Calls all widget update commands
        '''
        self._update_options()
        self._update_dropdown()
        #self._update_image()
        self._update_buttonstate()

    #-------------------------
    # Other internal functions
    #-------------------------
    
    def move_img_left(self):
        '''
        Moves to previous image, if image exists
        Updates button ability
        '''
        # Updates img_num and entry
        img_num = int(self.entry_num.get())
        if (img_num == 0):
            return
        else:
            self._set_shot_num(img_num-1)
        
        # Updates buttons
        self._update_buttonstate()
        
        # Loads new image
        self._update_image()
            
    def move_img_right(self):
        '''
        Moves to next image, if image exists
        Updates button ability
        '''
        # Updates img_num and entry
        img_num = int(self.entry_num.get())
        path = Helpers.get_from_file("shotrundir", "setup.json")
        path += "/" + self.diagnostic.get()
        max_num = Helpers.max_num_in_dir(path)
        if (img_num == max_num):
            return
        else:
            self._set_shot_num(img_num+1)
        
        # Updates buttons
        self._update_buttonstate()
        
        # Loads new image
        self._update_image()

    def _set_shot_num(self, num):
        ''' Sets number stored in shot number entry to num'''
        self.entry_num.delete(0, tk.END)
        self.entry_num.insert(0, str(num))
    def drop_diag_handle(self, event):
        #self._update_buttonstate()
        return

    def _load_btn(self):
        self._update_image()
        self._update_buttonstate()

    #-------------------------
    # init
    #-------------------------
    
    def __init__(self, master, scale=3, **options):
        tk.Frame.__init__(self, master, **options)

        self.scale = scale

        # Image and colorbar
        self.img_path = "assets/CUOS-med.png"
        self.lbl_img, self.img = Helpers.load_image(self.img_path, self,
                                                    k=scale)
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
        self._update_options()
        
        self.diagnostic = tk.StringVar()
        self.diagnostic.set(self.options[0])
        
        self.drop_diag = ttk.Combobox(self.fr_controls, width=27,
                                      textvariable=self.diagnostic)
        self.drop_diag['values'] = tuple(self.options)

        # ERROR WITH CALLBACK
        self.drop_diag.bind("<<ComboboxSelected>>", self.drop_diag_handle)
        self.drop_diag.grid(row=0, column=0, columnspan=2)

        # Increase/decrease scale buttons
        def increase_scale(self):
            self.scale += 0.2
            self._update_image()

        # Image loading
        '''
        Button for manually reloading the image
        '''
        btn_load = tk.Button(self.fr_controls, text="Load",
                             command=lambda: self._load_btn())
        btn_load.grid(row=1, column=0)

        # Image select 
        '''
        Text entry box for manually entering the desired picture number
        Buttons for moving to the previous or next picture
        '''
        self.entry_num = tk.Entry(self.fr_controls)
        self._set_shot_num(0)
        self.entry_num.grid(row=1, column=2)

        self.arrow_left = tk.Button(self.fr_controls, text="Previous Image",
                                    command=lambda: self.move_img_left())
        self.arrow_right = tk.Button(self.fr_controls, text="Next Image",
                                    command=lambda: self.move_img_right())
        self._update_buttonstate()
        self.arrow_left.grid(row=1, column=1)
        self.arrow_right.grid(row=1, column=3)
        

#-------------------------------------------------
# Execution
#-------------------------------------------------

def test():
    root = tk.Tk()
    gui = UI(root, scale=1)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()
        
