from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk

import UI_File_Transfer
import Helpers
import General_Parameters
import Diagnostic_Parameters

#-------------------------------------------------
# GUI
#-------------------------------------------------

class Acquisition_Display:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Acquisition and Display")
        self.root.iconbitmap("UM.ico")

        # General Parameters
        '''
        Frame for basic data management commands
        Appears regardless of selected tab
        '''
        self.fr_gen_param = General_Parameters.UI(self.root)
        self.fr_gen_param.grid(row=0, column=0)

        # Organization
        self.bookframe = tk.Frame()
        self.bookframe.grid(row=0, column=1)
        self.book = ttk.Notebook(self.bookframe)
        
        self.tab_main = ttk.Frame(self.book)
        self.tab_diag_params = ttk.Frame(self.book)
        self.tab_single_image = ttk.Frame(self.book)
        self.tab_montage1 = ttk.Frame(self.book)
        self.tab_montage2 = ttk.Frame(self.book)
        self.tab_montage3 = ttk.Frame(self.book)
        self.tab_montage4 = ttk.Frame(self.book)
        
        self.book.add(self.tab_main, text="Main")
        self.book.add(self.tab_diag_params, text="Diagnostic Parameters")
        self.book.add(self.tab_single_image, text="Single Image Display")
        self.book.add(self.tab_montage1, text="Image Montage Display 1")
        self.book.add(self.tab_montage2, text="Image Montage Display 2")
        self.book.add(self.tab_montage3, text="Image Montage Display 3")
        self.book.add(self.tab_montage4, text="Image Montage Display 4")
        
        self.book.pack(expand=1, fill="both")

        # Imported Widgets
        self.fr_diag_params = Diagnostic_Parameters.UI(self.tab_diag_params)
        self.fr_diag_params.pack()

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
        error_message = "Unexpected Error: " + str(sys.exc_info()[0])
        error_message += "\nClosed Data Acquisition and Display"
        Helpers.Notice_Window(error_message)
        
run()
