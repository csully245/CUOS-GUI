import Helpers

from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk
import os

class UI(tk.Frame):
    '''
    Frame for buttons that control saving shot data
    '''
    def __init__(self, master, wksp_diag, update_funcs, **options):
        tk.Frame.__init__(self, master, **options)
        self.wksp_diag = wksp_diag
        self.update_funcs = update_funcs
            
        self.btn_save_recent = tk.Button(self, text="Save Most Recent",
                                    command=lambda: self.save_most_recent())
        self.btn_save_recent.grid(row=0, column=0)

        self.btn_save_current = tk.Button(self, text="Save With These Settings",
                                    command=lambda: self.save_most_recent(increment=False))
        self.btn_save_current.grid(row=0, column=1)

        self.entry_num = tk.Entry(self)
        self.entry_num.insert(0, "0")
        self.entry_num.grid(row=1, column=0)
    
    def save_most_recent(self, increment=True):
        ''' Saves most recent shot data '''
        diag_data = Helpers.get_from_file("diagnostics", "diagnostic_data.json")
        paths = []
        names = []
        enabled_states = []
        for diag in diag_data:
            paths.append(diag["dir_temp"])
            names.append(diag["diagnostic"])
            enabled_states.append(diag["enabled"])
        shotrundir = Helpers.get_from_file("shotrundir")
        num = int(self.entry_num.get())
        if increment:
            num += 1
            self.entry_num.delete(0, tk.END)
            self.entry_num.insert(0, str(num))
        for path, name, enabled in zip(paths, names, enabled_states):
            dest = os.path.join(shotrundir, name)
            if (os.path.isdir(path) and os.path.isdir(dest)
                    and name != "" and enabled):
                Helpers.save_most_recent(path, dest, name, num)
        Helpers.edit_file("shot_num", self.entry_num.get(), "setup.json")
        for func in self.update_funcs:
            func()
        Helpers.save_plots(self.entry_num.get(), shotrundir)