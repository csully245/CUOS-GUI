import Helpers

from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk
import os

class UI(tk.Frame):
    '''
    Frame for buttons that control saving shot data
    '''

    def save(self):
            ''' Saves most recent shot data '''
            diag_data = self.wksp_diag()
            paths = []
            names = []
            for diag in diag_data:
                paths.append(diag["dir_temp"])
                names.append(diag["diagnostic"])
            print(paths)
            shotrundir = Helpers.get_from_file("shotrundir", "setup.json")
            for path, name in zip(paths, names):
                dest = shotrundir + "/" + name
                if (os.path.isdir(path) and os.path.isdir(dest)):
                    Helpers.save_most_recent(path, dest)
    
    def __init__(self, master, wksp_diag, **options):
        tk.Frame.__init__(self, master, **options)
        self.wksp_diag = wksp_diag
            
        btn_save = tk.Button(self, text="Save", command=lambda: self.save())
        btn_save.pack()

def test():
    root = tk.Tk()
    fr = UI(root)
    fr.pack()
    root.mainloop()
