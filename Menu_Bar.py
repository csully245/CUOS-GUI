import Helpers

from tkinter import filedialog as fd
import tkinter as tk
import os
import json


class UI(tk.Menu):
    """
    Menu bar with file dropdown menu
    Fills role of General Parameters in old MATLAB GUI

    Commands:
    -Select Shot Run Directory
    -Load From Workspace
    -Save Current Workspace
    """

    def __init__(self, master, workspace_load=None, workspace_save=None,
                 update_funcs=None, tearoff=0, **options):
        tk.Menu.__init__(self, master, tearoff=tearoff, **options)

        self.update_funcs = update_funcs
        '''
        workspace_load: list of functions to update a tab based on a json file.
        Should have parameters (self, workspace), where workspace is a
        json-friendly data type packaged by the tab's own workspace_save()

        workspace_save: list of functions to save a tab's settings into a
        json file. Should have parameters (self).
        '''

        def null(workspace):
            """ Default blank function in case no functions are passed """
            return

        # Load Workspace
        if workspace_load is None or len(workspace_load) == 0:
            self.workspace_load = [null]
        else:
            self.workspace_load = workspace_load
        self.workspace_load.append(self.load_from_workspace)

        # Save Current Workspace
        ''' Assign null function if no functions are passed '''
        if workspace_save is None or len(workspace_save) == 0:
            self.workspace_save = [null]
        else:
            self.workspace_save = workspace_save
        self.workspace_save.append(self.get_workspace)

        # Select Shot Run Directory
        if os.path.exists("PermPathFile"):
            file = open("PermPathFile", "r")
            self.path_perm = file.read()
        else:
            self.path_perm = "./"

        # Assemble menu bar
        self.file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Select Shot Run Directory",
                                   command=lambda: self.set_path_perm())
        self.file_menu.add_command(label="Select Base of Shot Run Directory",
                                   command=lambda: self.set_base_shotrundir())
        self.file_menu.add_command(label="Zip Shot Run Directory",
                                   command=lambda: self.zip_shotrundir())
        self.file_menu.add_command(label="Load Workspace",
                                   command=lambda: self.load_workspace())
        self.file_menu.add_command(label="Save Current Workspace",
                                   command=lambda: self.save_workspace())

    def load_workspace(self):
        """
        File menu option for "Load Workspace"
        Pulls data from json file
        Calls load function for each tab
        """
        path_load = fd.askopenfilename(initialdir="./Workspaces",
                                       title="Select Workspace",
                                       filetypes=(("json files", "*.json"),))
        if not (os.path.isfile(path_load)):
            return
        with open(path_load, "r") as read_file:
            workspace = json.load(read_file)
        for wksp, funct in zip(workspace, self.workspace_load):
            funct(wksp)

    def save_workspace(self):
        """
        File menu option for "Save Current Workspace"
        Creates list 'workspace' to store data needed to load current
        option selections. Each element in workspace is whatever data
        each tab requires. Must all be json-friendly
        Stores workspace in json file
        """
        path_save = fd.asksaveasfilename(initialdir="./Workspaces",
                                         title="Save Workspace",
                                         defaultextension='.json',
                                         filetypes=(("json files", "*.json"),))
        workspace = []
        for func in self.workspace_save:
            workspace.append(func())
        with open(path_save, "w") as write_file:
            json.dump(workspace, write_file)

    def set_path_perm(self):
        """
        File menu option for "Select Shot Run Directory"
        Sets the directory for the permanent (destination) files
        """
        initial_dir = Helpers.get_from_file("base_shotrundir", "setup.json")
        self.path_perm = fd.askdirectory(initialdir=initial_dir,
                                         title="Set Permanent Storage Directory")
        if self.path_perm == "":
            pass
        else:
            perm_dir_file = open("PermDirFile", "w")
            perm_dir_file.write(self.path_perm)
            Helpers.edit_file("shotrundir", self.path_perm)

        if self.update_funcs:
            for func in self.update_funcs:
                func()

    def set_base_shotrundir(self):
        """ File menu option for "Select Base of Shot Run Directory """
        initial_dir = Helpers.get_from_file("base_shotrundir", "dimensions.json")
        initial_dir = fd.askdirectory(initialdir=initial_dir,
                                      title="Set Base of Permanent Storage Directory")
        Helpers.edit_file("base_shotrundir", initial_dir, "dimensions.json")

    def zip_shotrundir(self):
        """
        File menu option for "Zip Shot Run Directory"
        Compresses the shot run directory into .zip files by shot num
        Folder: ./(shotrundir)/Zipped_Shots_(shotrundir name)
        .zip files: (shotrundir name)_shot###
        Files within .zip files: diagnostic_shot### (same name as origin)
        """
        print(Helpers.zip_shot_run_dir())

    def load_from_workspace(self, workspace):
        return

    def get_workspace(self):
        return None


def test():
    root = tk.Tk()
    menu_bar = UI(root)
    root.config(menu=menu_bar)
    root.mainloop()
