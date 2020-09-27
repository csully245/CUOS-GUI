#import Helpers

from tkinter import filedialog as fd
import tkinter as tk
import os

#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------

class Diagnostic_Frame(tk.LabelFrame):
    '''
    Sub-frame for options for each unique diagnostic
    '''
    def __init__(self, master, num, root_dir):
        tk.LabelFrame.__init__(self, master, text="Diagnostic " + str(num))

        
        self.dir = ".." # Directory of diagnostic (temp storage)
        self.enabled = False
        self.root_dir = root_dir # Directory of permanent storage
        
        # Widgets
        self.lbl_1 = tk.Label(self, text="Enter Diagnostic Name")
        self.entry_diagnostic = tk.Entry(self, width=20)
        self.entry_dir = tk.Entry(self, width=20)
        self.lbl_2 = tk.Label(self, text="Enter File Extension")
        self.entry_ext = tk.Entry(self, width=20)
        self.entry_ext.insert(0, ".tif")

        self.raw_img = tk.BooleanVar()
        self.raw_img.set(False)
        self.checkbtn_raw = tk.Checkbutton(self, text="Raw Image",
                                        variable=self.raw_img)
        
        def select_dir(self):
            title_text = "Select Diagnostic Source Directory"
            if (os.path.exists(self.entry_dir.get())):
                initial_dir = self.entry_dir.get()
            else:
                initial_dir = ".."
            self.dir = fd.askdirectory(initialdir=initial_dir,
                                        title=title_text)
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, self.dir)
        self.btn_dir = tk.Button(self, text="Select Directory",
                            command=lambda: select_dir(self))

        self.enabled = tk.BooleanVar()
        self.enabled.set(False)
        def enable_diagnostic(self):
            perm = os.path.join(self.root_dir, self.entry_diagnostic.get())
            if (self.enabled.get()):
                os.mkdir(perm)
                # Error handling
                # Do I need to store the path somewhere?
            else:
                if (os.path.isdir(perm)):
                    os.remove(perm)
        self.checkbtn_enabled = tk.Checkbutton(self, text="Enable Diagnostic",
                                            variable=self.enabled,
                                            command=lambda: enable_diagnostic(self))
            

        # Gridding
        self.lbl_1.grid(row=0, column=0, pady=2)
        self.entry_diagnostic.grid(row=0, column=1, pady=2)
        self.btn_dir.grid(row=1, column=0, pady=2)
        self.entry_dir.grid(row=1, column=1, pady=2)
        self.lbl_2.grid(row=2, column=0, pady=2)
        self.entry_ext.grid(row=2, column=1, pady=2)
        self.checkbtn_raw.grid(row=3, column=0, pady=2)
        self.checkbtn_enabled.grid(row=3, column=1, pady=2)
        
class UI(tk.Frame):
    '''
    Frame for basic data management commands
    Appears regardless of selected tab
    '''
    def __init__(self, master, root_dir="..", **options):
        tk.Frame.__init__(self, master, **options)

        self.root_dir = root_dir
        rows = 4
        columns = 3
        count = 1
        self.frames = []
        for r in range(rows):
            for c in range(columns):
                fr = Diagnostic_Frame(self, count, self.root_dir)
                fr.grid(row=r, column=c, padx=5, pady=5)
                self.frames.append(fr)
                count += 1

    def get_paths(self):
        paths = []
        for fr in self.frames:
            if (fr.enabled.get()):
                paths.append(fr.dir)
        return paths
            

def test():
    root = tk.Tk()
    fr = UI(root)
    fr.pack()
    root.mainloop()
