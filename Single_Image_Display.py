#import Helpers

from tkinter import filedialog as fd
import tkinter as tk
from PIL import Image, ImageTk
import os

#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------

class UI(tk.LabelFrame):
    '''
    Frame for basic data management commands
    Appears regardless of selected tab
    '''
    def __init__(self, master, **options):
        tk.LabelFrame.__init__(self, master, text="General Parameters",
                               font=14, **options)

        # Shot Run Directory
        if (os.path.exists("PermPathFile")):
            file = open("PermPathFile", "r")
            self.path_perm = file.read()
        else:
            self.path_perm = ".."

        def set_path_perm(self):
            '''
            Sets the directory for the permanent (destination) files
            '''
            self.path_perm = fd.askdirectory(initialdir="..",
                                        title="Set Permanent Storage Directory")
            perm_dir_file = open("PermDirFile", "w")
            perm_dir_file.write(self.path_perm)
        
        self.btn_path_perm = tk.Button(self, text="Select Shot Run Directory",
                                      command=lambda: set_path_perm(self))
        self.btn_path_perm.pack(pady=5)

        # Shot counters

        # Buttons

        # Options

        self.testlabel = tk.Label(self, text="test")
        self.testlabel.pack()
