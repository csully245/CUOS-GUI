import tkinter as tk
import winsound
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import threading

'''
Helper functions and classes
'''

class Notice_Window:
    '''
    GUI template for notice messages, such as progress updates
    '''
    def __init__(self, txt):
        self.root = tk.Tk()
        self.root.title("Notice")
        self.root.iconbitmap("assets/UM.ico")
        self.root.geometry("300x50")
        
        self.lbl = tk.Label(self.root, text=txt)
        self.lbl.pack(padx=10, pady=10)
        
        self.root.mainloop()

class Error_Window:
    '''
    GUI template for error messages
    '''
    def __init__(self, txt):
        self.root = tk.Tk()
        self.root.title("Error")
        self.root.iconbitmap("assets/UM.ico")
        self.root.geometry("300x50")
        
        self.lbl = tk.Label(self.root, text="Error: " + txt)
        self.lbl.pack()
        winsound.PlaySound("SystemExit", winsound.SND_ASYNC)
        
        self.root.mainloop()

def load_image(img_path, k=1):
    '''
    Input: filepath 'img' to plt.imread-acceptable source
    Output: tkinter PhotoImage
    '''

    img_arr = plt.imread(img_path)
    img_arr = (img_arr*255).astype(np.uint8)
    img = Image.fromarray(img_arr)

    if (k != 1):
        size = (int(img.width * k), int(img.height * k))
        img = img.resize(size, Image.ANTIALIAS)

    return ImageTk.PhotoImage(img)
