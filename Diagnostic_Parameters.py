import Helpers

from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk
import os

class Diagnostic_Frame(tk.LabelFrame):
    """
    Sub-frame for options for each unique diagnostic
    Interactive widgets:
    -entry_diagnostic: enter name of diagnostic, used for shotrundir file name
    -btn_dir: select source directory for diagnostic's raw data
    -entry_ext: enter file extension, to unpack data if plt.imread() fails
    -checkbtn_raw: no functionality
    -checkbtn_enabled: determines whether the diagnostic is ready to transmit
    """
    def __init__(self, master, num, update_funcs):
        self.update_funcs = update_funcs
        tk.LabelFrame.__init__(self, master, text="Diagnostic " + str(num))

        # Public-access data
        self.enabled = tk.BooleanVar()
        self.enabled.set(False)
        
        # Widgets
        self.lbl_1 = tk.Label(self, text="Enter Diagnostic Name")
        self.entry_diagnostic = tk.Entry(self, width=20)
        self.entry_dir = tk.Entry(self, width=20)
        self.lbl_2 = tk.Label(self, text="Enter File Extension")
        self.entry_ext = tk.Entry(self, width=20)
        self.entry_ext.insert(0, ".tif")

        self.process_options = [
            "Raw Image"
            ]
        self.process = tk.StringVar()
        self.process.set(self.process_options[0])
        self.drop_process = ttk.Combobox(self, textvariable=self.process)
        self.drop_process['values'] = tuple(self.process_options)
        
        def select_dir(self):
            '''
            Opens directory menu and stores selection
            '''
            title_text = "Select Diagnostic Source Directory"
            if (os.path.exists(self.entry_dir.get())):
                initial_dir = self.entry_dir.get()
            else:
                initial_dir = "./"
            dir_temp = fd.askdirectory(initialdir=initial_dir,
                                        title=title_text)
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, dir_temp)
        self.btn_dir = tk.Button(self, text="Select Directory",
                            command=lambda: select_dir(self))

        def enable_diagnostic(self):
            '''
            Manages data source and destination folders for diagnostic
            Adds folder for diagnostic in shot_run_dir if setting to enable
            '''
            path = Helpers.get_from_file("shotrundir")
            perm=os.path.join(path, self.entry_diagnostic.get())
            if (self.enabled.get()):
                if not (os.path.isdir(perm)):
                    os.mkdir(perm)
                else:
                    Helpers.Notice_Window("Directory already exists")
            else:
                if (os.path.isdir(perm)):
                    try:
                        os.rmdir(perm)
                    except OSError:
                        self.checkbtn_enabled.select()
                        text = "Cannot disable, destination contains files."
                        Helpers.Notice_Window(text)
            for func in self.update_funcs:
                func()
                # ERROR: enabling diagnostic attempts to update image
                # but by definition the destination has no files
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
        self.drop_process.grid(row=3, column=0, pady=2, padx=2)
        self.checkbtn_enabled.grid(row=3, column=1, pady=2)
    
    def load_from_workspace(self, workspace):
        '''
        Loads default data from input values generated from selected workspace
        .json file
        Workspace: dict containing diagnostic name, file extension, raw image
        Enabling is set to false (will need error handling)
        '''
        # Enabling
        self.enabled.set(False)

        # Loading
        try:
            self.entry_diagnostic.delete(0, tk.END)
            self.entry_diagnostic.insert(0, workspace["diagnostic"])
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, workspace["dir_temp"])
            self.entry_ext.delete(0, tk.END)
            self.entry_ext.insert(0, workspace["file_extension"])
            self.drop_process.set(workspace["process"])
        except KeyError:
            Helpers.Error_Window("Incompatible workspace file.")

    def get_workspace(self):
        '''
        Returns all variables needed to later recreate an identical frame
        '''
        workspace = {
                "diagnostic": self.entry_diagnostic.get(),
                "dir_temp" : self.entry_dir.get(),
                "file_extension" : self.entry_ext.get(),
                "process" : self.drop_process.get()
            }
        return workspace

class UI(tk.Frame):
    '''
    Frame for basic data management commands.
    Appears regardless of selected tab.
    Creates an instance of Diagnostic_Frame for each possible diagnostic.
    '''
    def __init__(self, master, updater=None, **options):
        tk.Frame.__init__(self, master, **options)

        def null():
            return
        if (updater == None):
            updater = [null]

        rows = 5
        columns = 4
        count = 1
        self.frames = []
        for c in range(columns):
            for r in range(rows):
                fr = Diagnostic_Frame(self, count, updater)
                fr.grid(row=r, column=c, padx=10, pady=5)
                self.frames.append(fr)
                count += 1
    
    def load_from_workspace(self, workspace):
        '''
        Sets all diagnostics to values stored in workspace
        Workspace: list containing dicts of diagnostic values
        '''
        default_workspace = {
                "dir_temp" : "",
                "file_extension" : ".tif",
                "process" : "Select a Process"
            }
        for frame, i in zip(self.frames, range(len(self.frames))):
            if (len(workspace) <= i):
                frame.load_from_workspace(default_workspace)
            else:
                frame.load_from_workspace(workspace[i])

    def get_workspace(self):
        workspace = []
        for frame in self.frames:
            workspace.append(frame.get_workspace())
        return workspace

    def get_source_paths(self):
        paths = []
        for fr in self.frames:
            if (fr.enabled.get()):
                paths.append(fr.entry_dir.get())
        return paths

def test():
    root = tk.Tk()
    fr = UI(root)
    fr.pack()

    btn = tk.Button(root, text="Take data",
                    command=lambda: print(fr.get_workspace()))
    btn.pack()
    root.mainloop()