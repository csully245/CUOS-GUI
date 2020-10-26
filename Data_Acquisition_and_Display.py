from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk
import sys
import json

import config
import UI_File_Transfer
import Helpers
import Main_tab
import General_Parameters
import Diagnostic_Parameters
import Image_Display_Single
import Image_Display_Montage
import Image_Display_Selective

#-------------------------------------------------
# GUI
#-------------------------------------------------

class Acquisition_Display:
    '''
    Master top-level GUI for data acquisition and display
    '''
    def add_wksp_funcs(self, frame):
        '''
        Adds functions for saving and loading workspace data for a
        particular tab's frame
        '''
        load = frame.load_from_workspace
        self.workspace_load_funcs.append(load)
        save = frame.get_workspace
        self.workspace_save_funcs.append(save)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Acquisition and Display")
        self.root.iconbitmap("assets/UM.ico")

        self.update_funcs = []
        self.workspace_load_funcs = []
        self.workspace_save_funcs = []

        # Organization
        self.bookframe = tk.Frame()
        self.bookframe.grid(row=0, column=1)
        self.book = ttk.Notebook(self.bookframe)
        
        self.tab_main = ttk.Frame(self.book)
        self.tab_diag_params = ttk.Frame(self.book)
        self.tab_single_image = ttk.Frame(self.book)
        self.tab_montage = ttk.Frame(self.book)
        self.tab_selective = ttk.Frame(self.book)
        
        self.book.add(self.tab_main, text="Main")
        self.book.add(self.tab_diag_params, text="Diagnostic Parameters")
        self.book.add(self.tab_single_image, text="Single Image Display")
        self.book.add(self.tab_montage, text="Image Montage Display")
        self.book.add(self.tab_selective, text="Selective Image Display")
        
        self.book.pack(expand=1, fill="both")

        # Imported Widgets
        self.fr_main = Main_tab.UI(self.tab_main)
        self.fr_main.pack()

        self.fr_single_image = Image_Display_Single.UI(self.tab_single_image)
        self.fr_single_image.pack()
        self.update_funcs.append(self.fr_single_image.update_all)
        self.add_wksp_funcs(self.fr_single_image)

        self.fr_multi_image = Image_Display_Montage.UI(self.tab_montage)
        self.fr_multi_image.pack()

        self.fr_selective_image = Image_Display_Selective.UI(self.tab_selective)
        self.fr_selective_image.pack()
        self.add_wksp_funcs(self.fr_selective_image)

        ''' Parameter frames loaded last to allow passing full update_funcs '''
        self.fr_diag_params = Diagnostic_Parameters.UI(self.tab_diag_params,
                                                       self.update_funcs)
        self.fr_diag_params.pack()
        self.add_wksp_funcs(self.fr_diag_params)
        
        # General Parameters
        '''
        Frame for basic data management commands
        Appears regardless of selected tab
        Shot run directory function must be in top-level to ensure data access
        '''
        self.fr_gen_param = General_Parameters.UI(self.root,
                                                  self.workspace_load_funcs,
                                                  self.workspace_save_funcs)
        self.fr_gen_param.grid(row=0, column=0)

    def open(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()

#-------------------------------------------------
# Execution
#-------------------------------------------------

def run():
    '''
    Example code for running the GUI
    '''
    acq = Acquisition_Display()
    try:
        acq.open()
    except:
        acq.close()
        # Doesn't catch errors inside mainloop
        error_message = "(unhandled) " + str(sys.exc_info()[0])
        error_message += "\nClosed Data Acquisition and Display"
        Helpers.Error_Window(error_message)
        
run()
