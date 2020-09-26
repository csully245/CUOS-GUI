import UI_File_Transfer
import Helpers

from tkinter import filedialog as fd
import tkinter as tk

#-------------------------------------------------
# GUI
#-------------------------------------------------

class Acquisition_Display:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Acquisition and Display")
        self.root.iconbitmap("UM.ico")

        self.fr_transfer = UI_File_Transfer.UI(self.root)
        self.fr_transfer.pack()

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
