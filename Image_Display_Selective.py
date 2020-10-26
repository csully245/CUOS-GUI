import config
import Helpers
import Image_Display_Single

import tkinter as tk
    
#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------  

class UI(tk.Frame):
    '''
    Frame for displaying multiple images, to be individually selected.
    Each image is a Image_Display_Single UI
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
    
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)

        # Display tiled images
        rows = 3
        columns = 3
        self.frames = []
        for c in range(columns):
            for r in range(rows):
                fr = Image_Display_Single.UI(self)
                fr.grid(row=r, column=c, padx=10, pady=5)
                self.frames.append(fr)

        

#-------------------------------------------------
# Execution
#-------------------------------------------------

def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()
        
