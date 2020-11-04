import os
import json

import Helpers

def is_files_made():
    ''' Checks if necessary files have been created '''

def startup():
    ''' Ensures all necessary files and data exist before proceeding '''
    
    ''' Checks if each default directory exists '''
    paths = ["./Shot_Run_Default",
             "./Shot_Run_Default/Example",
             "./Workspaces",
             "./assets"
             ]
    for path in paths:
        while not (os.path.isdir(path)):
            error_text = 'Required path "' + path + '" does not exist'
            error_text += "\n Check that expected files exist"
            Helpers.Error_Window(error_text)
            # NOTE: This will only check if the path exists, not if the
            # data inside them is valid

    ''' Attempts to read file. If fails, opens file with default data '''
    filename = "setup.json"
    try:
        with open(filename,"r") as read_file:
            data = json.load(read_file)
        path = data["shotrundir"]
        if not(os.path.isdir(path)):
            data = {
            "shotrundir": "./Shot_Run_Default"
            }
            with open(filename,"w") as write_file:
                json.dump(data,write_file)
    except FileNotFoundError:
        data = {
            "shotrundir": "./Shot_Run_Default"
            }
        with open(filename,"w") as write_file:
            json.dump(data,write_file)

    
    
        
        
    
    
