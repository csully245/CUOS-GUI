import os
import json
from datetime import date
import tkinter as tk

import Helpers
'''
class Startup_Menu:
    def set_status(self, status):
        self.status = status
        self.root.destroy()
    def __init__(self):
        self.status = False
        
        self.root = tk.Tk()
        self.root.title("Startup")
        self.root.iconbitmap("assets/UM.ico")
        self.root.geometry("300x80")

        txt = "Would you like to generate a new shot run directory?"
        self.lbl = tk.Label(self.root, text=txt)
        self.lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.btn_yes = tk.Button(self.root, text="Yes", command=lambda:
                            self.set_status(True))
        self.btn_yes.grid(row=1, column=0, padx=5, pady=10)

        self.btn_no = tk.Button(self.root, text="No", command=lambda:
                            self.set_status(False))
        self.btn_no.grid(row=1, column=1, padx=5, pady=10)
    def start(self):
        self.root.mainloop()
        
'''
def startup():
    ''' Ensures all necessary files and data exist before proceeding '''
    
    ''' Checks if each default directory exists '''
    paths = ["./Shot_Runs",
             "./Shot_Runs/Shot_Run_Default",
             "./Workspaces",
             "./assets",
             "./assets/Example_Diagnostic"
             ]
    for path in paths:
        while not (os.path.isdir(path)):
            error_text = 'Required path "' + path + '" does not exist'
            error_text += "\n Check that expected files exist"
            Helpers.Error_Window(error_text)
            # NOTE: This will only check if the path exists, not if the
            # data inside them is valid
    
    ''' Handles shot run directory in file structure'''
    #startup_menu = Startup_Menu()
    #startup_menu.start()
    status = True
    # NOTE: Startup menu disabled, should be enabled in final product
    if (status):
        ''' Generates a new shot run directory '''
        today = date.today()
        shot_run_name = "./Shot_Runs/Shot_Run_" + today.strftime("%Y_%m_%d")
        if not (os.path.isdir(shot_run_name)):
            os.mkdir(shot_run_name)
    else:
        ''' Uses default shot run directory '''
        shot_run_name = "./Shot_Runs/Shot_Run_Default"

    ''' Stores shot_run_name in setup.json '''
    filename = "setup.json"
    data = {
            "shotrundir": shot_run_name
            }
    with open(filename,"w") as write_file:
            json.dump(data,write_file)
