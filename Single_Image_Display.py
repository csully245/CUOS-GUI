import tkinter as tk
from PIL import Image, ImageTk

#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------

class UI(tk.Frame):
    '''
    Frame for displaying a single image
    '''
    def __init__(self, master, **options):
        tk.LabelFrame.__init__(self, master, **options)

        self.img = ImageTk.PhotoImage(Image.open("assets/default-image"))
        self.img.pack()

        self.fr_controls = tk.Frame(self)
        self.fr_controls.pack()

        self.diagnostic = tk.StringVar()
        self.diagnostic.set("")
        self.options = [""]
        self.drop_diag = tk.OptionMenu(fr_controls, self.diagnostic,
                                       self.options)

    def update_options(self):
        '''
        Updates diagnostic options
        '''
        pass

        
