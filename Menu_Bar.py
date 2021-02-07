import Helpers

from tkinter import filedialog as fd
import tkinter as tk
import os
import json

class UI(tk.Menu):
    '''
    Menu bar with file dropdown menu
    Fills role of General Parameters in old MATLAB GUI

    Commands:
    -Select Shot Run Directory
    -Load From Workspace
    -Save Current Workspace
    '''
    def __init__(self, master, workspace_load=None, workspace_save=None,
                 update_funcs=None, tearoff=0, **options):
        tk.Menu.__init__(self, master, tearoff=tearoff, **options)
        
        '''
        workspace_load: list of functions to update a tab based on a json file.
        Should have parameters (self, workspace), where workspace is a
        json-friendly data type packaged by the tab's own workspace_save()

        workspace_save: list of functions to save a tab's settings into a
        json file. Should have parameters (self).
        '''

        def null(workspace):
            ''' Default blank function in case no functions are passed '''
            return
        
        # Load Workspace
        if (workspace_load == None or len(workspace_load) == 0):
            self.workspace_load = [null]
        else:
            self.workspace_load = workspace_load
        self.workspace_load.append(self.load_from_workspace)
        
        def load_workspace(self):
            # NOTE: Fix function naming conventions
            '''
            Pulls data from json file
            Calls load function for each tab
            '''
            path_load = fd.askopenfilename(initialdir = "./Workspaces",
                                      title = "Select Workspace",
                                      filetypes = (("json files","*.json"),))
            if not (os.path.isfile(path_load)):
                return
            with open(path_load,"r") as read_file:
                workspace = json.load(read_file)
            for wksp,funct in zip(workspace, self.workspace_load):
                funct(wksp)

        # Save Current Workspace
        ''' Assign null function if no functions are passed '''
        if (workspace_save == None or len(workspace_save) == 0):
            self.workspace_save = [null]
        else:
            self.workspace_save = workspace_save
        self.workspace_save.append(self.get_workspace)

        def save_workspace(self):
            '''
            Creates list 'workspace' to store data needed to load current
            option selections. Each element in workspace is whatever data
            each tab requires. Must all be json-friendly
            Stores workspace in json file
            '''
            path_save =  fd.asksaveasfilename(initialdir="./Workspaces",
                                              title="Save Workspace",
                                              defaultextension='.json',
                                              filetypes=(("json files","*.json"),))
            workspace = []
            for funct in self.workspace_save:
                workspace.append(funct())
            with open(path_save,"w") as write_file:
                json.dump(workspace,write_file)

        # Select Shot Run Directory
        if (os.path.exists("PermPathFile")):
            file = open("PermPathFile", "r")
            self.path_perm = file.read()
        else:
            self.path_perm = "./"

        def set_path_perm(self):
            '''
            Sets the directory for the permanent (destination) files
            '''
            self.path_perm = fd.askdirectory(initialdir="./Shot_Runs",
                                        title="Set Permanent Storage Directory")
            perm_dir_file = open("PermDirFile", "w")
            perm_dir_file.write(self.path_perm)
            Helpers.edit_file("shotrundir", self.path_perm)

            if (update_funcs):
                for func in update_funcs:
                    func() 

        # Assemble menu bar
        self.filemenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Select Shot Run Directory",
                                  command=lambda: set_path_perm(self))
        self.filemenu.add_command(label="Load Workspace",
                                  command=lambda: load_workspace(self))
        self.filemenu.add_command(label="Save Current Workspace",
                                  command=lambda: save_workspace(self))
    
    def load_from_workspace(self, workspace):
        return
        
    def get_workspace(self):
        return None

def test():
    root = tk.Tk()
    menubar = UI(root)
    root.config(menu=menubar)
    root.mainloop()