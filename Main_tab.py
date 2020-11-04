import tkinter as tk

class UI(tk.Frame):
    '''
    Frame for displaying use instructions
    '''
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)
        
        self.lbl_title = tk.Label(self, text="Welcome to CUOS!")
        self.lbl_title.pack()

        instructions = ''' How To Use This GUI
Quick Start:
Go to File >> Load Workspace, then select a workspace to load

Otherwise:
1) Select a shot run directory in the File tab
2) Enable the appropriate diagnostics
3) Use the various display tabs to view the data


Display Tabs:

Single Image Display:
1) Select a diagnostic
2) Press the Load button
3) Use the buttons or text entry box to select an image

Image Montage Display:
1) Each column displays three images from one diagnostic
2) Set each column's diagnostic
3) Press the Load button for each diagnostic
4) (Coming soon) use the commands at the bottom to select images
5) Use the Add/Remove Diagnostic buttons to customize the display

Selective Image Display:
1) For each image, follow the steps in Single Image Display


Workspaces:
In the File menu, you can save or load all settings for each interface
        ''' 
        self.lbl_instructions = tk.Label(self, text=instructions)
        self.lbl_instructions.pack()

#-------------------------------------------------
# Execution
#-------------------------------------------------

def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()
        
