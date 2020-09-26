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
    def __init(self, master, num):
        # ERROR: TypeError: argument of type 'int' is not iterable
        # Likely from trying to pass num to LabelFrame
        txt = "Diagnostic " + str(num)
        tk.LabelFrame.__init__(self, master, text=txt)
        self.dir = ".."
        
        # Widgets
        self.lbl_1 = tk.Label(self, text="Enter Diagnostic Name")
        self.entry_diagnostic = tk.Entry(self, width=20)
        self.entry_dir = tk.Entry(self, width=20)
        
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
        

        # Gridding
        self.lbl_1.grid(row=0, column=0)
        self.entry_diagnostic.grid(row=0, column=1)
        self.btn_dir.grid(row=1, column=0)
        self.entry_dir.grid(row=1, column=1)
        

class UI(tk.Frame):
    '''
    Frame for basic data management commands
    Appears regardless of selected tab
    '''
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)
        
        rows = 4
        columns = 3
        count = 1
        for r in range(rows):
            for c in range(columns):
                fr = Diagnostic_Frame(self, count)
                fr.grid(row=r, column=c)
                count += 1

def test():
    root = tk.Tk()
    fr = UI(root)
    fr.pack()
    root.mainloop()

        
