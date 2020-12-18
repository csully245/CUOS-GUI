import os
import json
from datetime import date
import tkinter as tk

import Helpers

class Startup_Menu(tk.Frame):
    '''
    Asks user for info needed to create shotrundir
    Instantiated in Sidebar_Dialog
    '''
    def get_data(self):
        date = {
            "year": self.entry_year.get(),
            "month": self.entry_month.get(),
            "day": self.entry_day.get()
            }
        return {
            "run_name": self.entry_run_name.get(),
            "date": date,
            "run_num": self.entry_run_num.get()
            }
    def ok(self):
        '''
        Handles 'ok' button:
        -Checks if shotrundir already exists
        -Loads new UI if necessary
        -Updates shotrundir if necessary
        -Removes UI
        '''
        
        # Checks if shotrundir already exists
        menu_data = self.get_data()
        date = menu_data["date"]
        shotrundir = "./Shot_Runs" + "/" 
        shotrundir += menu_data["run_name"] + "_" + menu_data["run_num"]
        shotrundir += date["year"] + date["month"] + date["day"]
        if (os.path.isdir(shotrundir)):
            # Asks if there should be a new dir made
            # TODO: create UI for this
            shotrundir += "(Copy)"
            os.mkdir(shotrundir)
            Helpers.edit_file("shotrundir", shotrundir, "setup.json")
        else:
            # Makes a new dir
            os.mkdir(shotrundir)
            Helpers.edit_file("shotrundir", shotrundir, "setup.json")
        self.grid_forget()
        
    def __init__(self, master, **options):
        self.master = master
        tk.Frame.__init__(self, master, **options)

        # Shot Run Directory
        txt="Enter shot run directory name"
        self.lbl_run_name = tk.Label(self, text=txt)
        
        self.entry_run_name = tk.Entry(self, width=30)
        self.entry_run_name.insert(0, "Shotrundir_Default")

        # Date
        txt="Enter date"
        self.lbl_date = tk.Label(self, text=txt)

        self.frame_date_entries = tk.Frame(self)
        today = date.today()
        
        self.entry_year = tk.Entry(self.frame_date_entries, width=15)
        self.entry_year.insert(0, today.strftime("%Y"))
        self.entry_year.grid(row=0, column=0)
        
        self.entry_month = tk.Entry(self.frame_date_entries, width=7)
        self.entry_month.insert(0, today.strftime("%m"))
        self.entry_month.grid(row=0, column=1)
        
        self.entry_day = tk.Entry(self.frame_date_entries, width=7)
        self.entry_day.insert(0, today.strftime("%d"))
        self.entry_day.grid(row=0, column=2)

        # Run number
        txt="Enter run number"
        self.lbl_run_num = tk.Label(self, text=txt)
        
        self.entry_run_num = tk.Entry(self, width=30)
        self.entry_run_num.insert(0, "0")

        # OK button
        self.btn_ok = tk.Button(self, text="Ok", command=lambda: self.ok())
        
        # Gridding
        #self.lbl_run_name.grid(row=0, column=0)
        self.entry_run_name.grid(row=0, column=1)
        #self.lbl_date.grid(row=1, column=0)
        self.frame_date_entries.grid(row=1, column=1)
        #self.lbl_run_num.grid(row=2, column=0)
        self.entry_run_num.grid(row=2, column=1)
        self.btn_ok.grid(row=3, column=1)







def startup_2():
    menu = Startup_Menu()
    menu_data = menu.get_data()
    date = menu_data["date"]

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
    shotrundir = "./Shot_Runs" + "/" 
    shotrundir += menu_data["run_name"] + "_" + menu_data["run_num"]
    shotrundir += date["year"] + date["month"] + date["day"]
    if (os.path.isdir(shotrundir)):
        # Run GUI to check if they want to save into the same folder or not
        pass
    os.mkdir(shotrundir)
    
    ''' Stores shot_run_name in setup.json '''
    filename = "setup.json"
    data = {
            "shotrundir": shotrundir,
            "date": date
            }
    with open(filename,"w") as write_file:
            json.dump(data,write_file)
    
