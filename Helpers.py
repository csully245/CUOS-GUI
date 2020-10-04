import tkinter as tk
import winsound
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageTk

'''
Helper functions and classes
'''

class Notice_Window:
    '''
    GUI template for notice messages, such as progress updates and errors
    '''
    def __init__(self, txt, error=True):
        self.root = tk.Tk()
        self.root.title("Notice")
        self.root.iconbitmap("assets/UM.ico")
        self.root.geometry("300x50")
        
        self.lbl = tk.Label(self.root, text=txt)
        self.lbl.pack(padx=10, pady=10)
        if (error):
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

        '''
        self.btn = tk.Button(self.root, text="Close", width=20, height=10,
                             command=self.root.destroy)
        self.btn.pack()
        '''

def load_image(img_path):
    '''
    Input: filepath 'img' to plt.imread-acceptable source
    Output: tkinter PhotoImage
    '''
    img_arr = plt.imread(img_path)
    img_arr = (img_arr*255).astype(np.uint8)
    return ImageTk.PhotoImage(Image.fromarray(img_arr))
