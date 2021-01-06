import Helpers

from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk
import os

class UI(tk.Frame):
    '''
    Frame for buttons that control saving shot data
    '''

    def save_most_recent(self):
        ''' Saves most recent shot data '''
        diag_data = self.wksp_diag()
        paths = []
        names = []
        for diag in diag_data:
            paths.append(diag["dir_temp"])
            names.append(diag["diagnostic"])
        shotrundir = Helpers.get_from_file("shotrundir", "setup.json")
        for path, name in zip(paths, names):
            dest = shotrundir + "/" + name
            # ADD: check if enabled
            if (os.path.isdir(path) and os.path.isdir(dest) and name != ""):
                Helpers.save_most_recent(path, dest, name)

    def save_by_number(self):
        ''' Saves shot number data, if it exists '''
        diag_data = self.wksp_diag()
        shotrundir = Helpers.get_from_file("shotrundir", "setup.json")
        for diag in diag_data:
            src = diag["dir_temp"]
            dest = shotrundir + "/" + diag["diagnostic"]
            if (os.path.isdir(src) and os.path.isdir(dest)):
                Helpers.save_by_number(src, dest, self.entry_num.get(),
                                       diag["diagnostic"])
    
    def __init__(self, master, wksp_diag, **options):
        tk.Frame.__init__(self, master, **options)
        self.wksp_diag = wksp_diag
            
        self.btn_save_recent = tk.Button(self, text="Save Most Recent",
                                    command=lambda: self.save_most_recent())
        self.btn_save_recent.grid(row=0, column=0, padx=5)

        self.btn_save_num = tk.Button(self, text="Save Shot Number",
                                 command=lambda: self.save_by_number())
        self.btn_save_num.grid(row=0, column=1, padx=5)

        self.btn_screenshot = tk.Button(self, text="Save Screenshot",
                                        command=Helpers.take_screenshot)
        self.btn_screenshot.grid(row=0, column=2, padx=5)

        self.entry_num = tk.Entry(self)
        self.entry_num.insert(0, "0")
        self.entry_num.grid(row=1, column=1)
