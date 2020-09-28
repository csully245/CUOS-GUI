import Helpers
import config

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
    def __init__(self, master, num):
        tk.LabelFrame.__init__(self, master, text="Diagnostic " + str(num))

        # Public-access data
        self.dir_temp = ".."
        self.enabled = False
        self.raw_img = tk.BooleanVar()
        self.raw_img.set(False)
        self.enabled = tk.BooleanVar()
        self.enabled.set(False)
        
        # Widgets
        self.lbl_1 = tk.Label(self, text="Enter Diagnostic Name")
        self.entry_diagnostic = tk.Entry(self, width=20)
        self.entry_dir = tk.Entry(self, width=20)
        self.lbl_2 = tk.Label(self, text="Enter File Extension")
        self.entry_ext = tk.Entry(self, width=20)
        self.entry_ext.insert(0, ".tif")
        self.checkbtn_raw = tk.Checkbutton(self, text="Raw Image",
                                        variable=self.raw_img)
        
        def select_dir(self):
            '''
            Opens directory menu and stores selection
            '''
            title_text = "Select Diagnostic Source Directory"
            if (os.path.exists(self.entry_dir.get())):
                initial_dir = self.entry_dir.get()
            else:
                initial_dir = ".."
            self.dir_temp = fd.askdirectory(initialdir=initial_dir,
                                        title=title_text)
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, self.dir_temp)
        self.btn_dir = tk.Button(self, text="Select Directory",
                            command=lambda: select_dir(self))

        def enable_diagnostic(self):
            '''
            Manages data source and destination folders for diagnostic
            Adds folder for diagnostic in shot_run_dir if setting to enable
            '''
            perm=os.path.join(config.shot_run_dir,self.entry_diagnostic.get())
            if (self.enabled.get()):
                if not (os.path.isdir(perm)):
                    os.mkdir(perm)
                else:
                    Helpers.Notice_Window("Directory already exists",
                                          error=False)
            else:
                if (os.path.isdir(perm)):
                    # WARNING: Be careful in testing, this can delete dirs
                    # lol access denied, thanks windows
                    os.remove(perm)
        self.checkbtn_enabled = tk.Checkbutton(self, text="Enable Diagnostic",
                                            variable=self.enabled,
                                            command=lambda: \
                                               enable_diagnostic(self))

        # Gridding
        self.lbl_1.grid(row=0, column=0, pady=2)
        self.entry_diagnostic.grid(row=0, column=1, pady=2, padx=10)
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
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)

        rows = 4
        columns = 3
        count = 1
        self.frames = []
        for c in range(columns):
            for r in range(rows):
                fr = Diagnostic_Frame(self, count)
                fr.grid(row=r, column=c, padx=10, pady=5)
                self.frames.append(fr)
                count += 1

    def get_source_paths(self):
        paths = []
        for fr in self.frames:
            if (fr.enabled.get()):
                paths.append(fr.dir_temp)
        return paths

def test():
    root = tk.Tk()
    fr = UI(root)
    fr.pack()

    btn = tk.Button(root, text="Take data",
                    command=lambda: print(fr.get_source_paths()))
    btn.pack()
    root.mainloop()
