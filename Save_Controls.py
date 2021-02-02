import Helpers

from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk
import os
import threading

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
                num = int(self.entry_num.get())
                Helpers.save_most_recent(path, dest, name, num)
                num += 1
                self.entry_num.delete(0, tk.END)
                self.entry_num.insert(0, str(num))
        for func in self.update_funcs:
            func()
        t1 = threading.Thread(target=Helpers.save_plots,
                    args=(self.entry_num.get(), shotrundir))
        t1.start()
    
    def __init__(self, master, wksp_diag, update_funcs, **options):
        tk.Frame.__init__(self, master, **options)
        self.wksp_diag = wksp_diag
        self.update_funcs = update_funcs
            
        self.btn_save_recent = tk.Button(self, text="Save Most Recent",
                                    command=lambda: self.save_most_recent())
        self.btn_save_recent.grid(row=0, column=0)

        self.entry_num = tk.Entry(self)
        self.entry_num.insert(0, "0")
        self.entry_num.grid(row=1, column=0)