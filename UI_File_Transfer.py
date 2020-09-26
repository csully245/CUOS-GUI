import Helpers

from tkinter import filedialog as fd
import tkinter as tk
from datetime import datetime
import os
import shutil
import sys

#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------

class UI(tk.Frame):
    '''
    Frame for file transfer
    '''
    def __init__(self, master=None, **options):
        tk.Frame.__init__(self, master=None, **options)
        
        # Source and destination filepaths
        if (os.path.exists("TempDirFile")):
            file = open("TempDirFile", "r")
            self.path_temp = file.read()
        else:
            self.path_temp = ".."
            
        if (os.path.exists("PermDirFile")):
            file = open("PermDirFile", "r")
            self.path_perm = file.read()
        else:
            self.path_perm = ".."

        # Frames
        self.fr_options = tk.Frame(self)
        self.fr_filepath = tk.LabelFrame(self)
        
        self.fr_options.grid(row=0, column=0)
        self.fr_filepath.grid(row=1, column=0)

        # fr_options
        '''
        Menu
        Current options: set temporary/permanent storage directories
        '''
        def set_temp_dir(self):
            '''
            Sets the directory for the temporary (source) files
            '''
            self.path_temp = fd.askdirectory(initialdir="..",
                                        title="Set Temporary Storage Directory")
            temp_dir_file = open("TempDirFile", "w")
            temp_dir_file.write(self.path_temp)

        def set_perm_dir(self):
            '''
            Sets the directory for the permanent (destination) files
            '''
            self.path_perm = fd.askdirectory(initialdir="..",
                                        title="Set Permanent Storage Directory")
            perm_dir_file = open("PermDirFile", "w")
            perm_dir_file.write(self.path_perm)
     
        self.btn_set_temp = tk.Button(self.fr_options,
                                      text="Set Temporary Storage Directory",
                                      command=lambda: set_temp_dir(self))
        
        self.btn_set_perm = tk.Button(self.fr_options,
                                      text="Set Permanent Storage Directory",
                                      command=lambda: set_perm_dir(self))
        self.btn_set_temp.grid(row=0, column=0, padx=5, pady=5)
        self.btn_set_perm.grid(row=0, column=1, padx=5, pady=5)
        
        # fr_filepath
        '''
        Frame for actual filepath button(s)
        '''
        def _get_dir_name():
            '''
            Returns an appropriate name for a data destination folder
            Format: ZEUS-Data--yyyy-mm-dd--hh-mm-ss
            '''
            now = datetime.now()
            name = "ZEUS-Data--"
            name += str(now.year)
            digits = [now.month, now.day] 
            for digit in digits:
                name += '-'
                if (len(str(digit)) == 1):
                    name += '0'
                name += str(digit)
            name += '-'
            digits = [now.hour, now.minute, now.second]
            for digit in digits:
                name += '-'
                if (len(str(digit)) == 1):
                    name += '0'
                name += str(digit)
            return name

        def _transfer_data(self):
            '''
            Copies all files from source to new folder in destination
            Handling:
            -Naming
            -Checking source and destination
            '''
            source = self.path_temp
            dest_parent = self.path_perm
            
            ''' Checks paths are valid '''
            if not (os.path.isdir(source)):
                Helpers.Notice_Window("Error: Invalid source path")
                return
            if not (os.path.isdir(dest_parent)):
                Helpers.Notice_Window("Error: Invalid destination path")
                return

            ''' Preps for transfer check '''
            file_count_start = len(os.listdir(source))
            
            ''' Creates destination '''
            destination = dest_parent + '\\' + _get_dir_name()
            if (os.path.isdir(destination)):
                num_copies = 1
                while (os.path.isdir(destination+'\\'"(" + str(num_copies) + ")")):
                    num_copies += 1
                destination+= "(" + str(num_copies) + ")"
            os.mkdir(destination)

            ''' Checks destination was created '''
            if not (os.path.isdir(destination)):
                Helpers.Notice_Window("Error: Could not create destination")
                return
            
            ''' Transfers data '''
            files = os.listdir(source)
            for f in files:
                shutil.move(source + '\\' + f, destination)

            ''' Checks data was transferred (number of files) '''
            file_count_end = len(os.listdir(destination))
            if (file_count_start == file_count_end):
                disp_text = "Files successfully transferred"
                error = False
            else:
                disp_text = "Error: Files not successfully transferred"
                error = True
            Helpers.Notice_Window(disp_text, error)
        '''
        Widgets
        '''
        self.btn_transfer = tk.Button(self.fr_filepath, text="Transfer Data",
                          command=lambda: _transfer_data(self))
        self.btn_transfer.pack()
