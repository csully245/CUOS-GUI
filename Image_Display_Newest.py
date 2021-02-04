import Helpers
import Image_Options_Menu

import os
import tkinter as tk

class Diagnostic_Display(tk.LabelFrame):
    '''
    Frame for displaying the most recent data from each diagnostic
    '''
    def update_image(self):
        '''Checks for more recent data for the diagnostic and updates image'''
        if (self.diag == ""):
            path = Helpers.default_img_path
        else:
            diag_path = os.path.join(self.shotrundir, self.diag)
            files = []
            for file in os.listdir(diag_path):
                filename = os.path.join(diag_path, file)
                if (os.path.isfile(filename)):
                    files.append(filename)
            if files:
                path = max(files, key=os.path.getctime)
            else:
                path = Helpers.default_img_path
            self.img_path = path
        if (self.img_path == Helpers.default_img_path):
            recolor = False
        else:
            recolor = True
        self.wgt_img.grid_forget()
        vmin, vmax = self.fr_options.get()
        self.wgt_img, self.img = Helpers.plot_image(self.img_path,
                                                self, recolor=recolor, vmin=vmin, vmax=vmax)
        self.wgt_img.grid(row=0, column=0)
    
    def update_diagnostic(self, diag, shotrundir):
        self.config(text = diag)
        self.diag = diag
        self.shotrundir = shotrundir
        self.update_image()

    def __init__(self, master, diag, shotrundir, **options):
        tk.LabelFrame.__init__(self, master, text=diag, **options)
        self.diag = diag
        self.shotrundir = shotrundir

        self.img_path = Helpers.default_img_path
        self.wgt_img, self.img = Helpers.load_image(self.img_path,
                                                    self)

        self.fr_options = Image_Options_Menu.UI(self)

        # Gridding
        self.wgt_img.grid(row=0, column=0)
        self.fr_options.grid(row=1, column=0)

#-------------------------------------------------
# Top-level GUI
#------------------------------------------------- 

class UI(tk.Frame):
    '''
    Container for each diagnostic frame. Shows the most recent data from each diagnostic.
    '''
    def load_from_workspace(self, workspace):
        '''
        Loads default data from input values generated from selected workspace
        .json file
        Workspace: list containing saved workspaced
        '''
        for fr, wksp in zip(self.frames, workspace):
            fr.load_from_workspace(wksp)

    def get_workspace(self):
        '''
        Returns all variables needed to later recreate an identical frame
        '''
        workspace = []
        for fr in self.frames:
            workspace.append(fr.get_workspace())
        return workspace

    def get_diagnostics(self):
        '''
        Returns a list of enabled diagnostic names
        '''
        out = []
        lst = os.listdir(self.shotrundir)
        for item in lst:
            if (item == "Aggregated Plots"):
                continue
            path = os.path.join(self.shotrundir, item)
            if os.path.isdir(path):
                out.append(item)
        return out
    
    def update_diagnostics(self):
        self.shotrundir = Helpers.get_from_file("shotrundir", "setup.json")
        diags = self.get_diagnostics()
        for frame in self.frames:
            if (diags):
                    diag = diags[0]
                    del diags[0]
            else:
                diag = ""
            frame.update_diagnostic(diag, self.shotrundir)
    
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)

        # Get diagnostics
        self.shotrundir = Helpers.get_from_file("shotrundir", "setup.json")
        diags = self.get_diagnostics()

        # Display tiled images
        rows = 2
        columns = 3
        self.frames = []
        for c in range(columns):
            for r in range(rows):
                if (diags):
                    diag = diags[0]
                    del diags[0]
                else:
                    diag = ""
                fr = Diagnostic_Display(self, diag, self.shotrundir)
                fr.grid(row=r, column=c, padx=10, pady=5)
                self.frames.append(fr)

        self.btn_update = tk.Button(self, text="Update", command=lambda: self.update_diagnostics())
        self.btn_update.grid(row=rows, column=1)

#-------------------------------------------------
# Execution
#-------------------------------------------------

def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()