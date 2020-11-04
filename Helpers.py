import tkinter as tk
import winsound
import numpy as np
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import json

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

def load_image(img_path, k=1, max_height=None, max_width=None):
    '''
    Input: filepath 'img' to plt.imread-acceptable source
    Output: tkinter PhotoImage
    '''

    # Read file
    img_arr = plt.imread(img_path)
    img_arr = (img_arr*255).astype(np.uint8)
    img = Image.fromarray(img_arr)

    # Scale based off k
    def scale(img, k):
        if (k != 1):
            return (int(img.width * k), int(img.height * k))
        else:
            return (img.width, img.height)
        
    width, height = scale(img, k)

    # Check max dimensions
    c = 1
    if (width > height and max_width != None):
        if (width > max_width):
            c = max_width / width
    elif (height > img.width and max_height != None):
        if (height > max_height):
            c = max_height / height
    size = scale(img, c)

    # Resize image
    img = img.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

def get_from_file(key, filename):
    '''
    Returns value of key in dict stored in filename
    File must be .json and contain only a dict
    '''
    with open(filename, "r") as read_file:
        data = json.load(read_file)
    if not key in data.keys():
        Error_Window('Key "' + key + '" does not exist.')
        return ""
    return data[key]

def edit_file(key, value, filename):
    '''
    Sets value of key in dict stored in filename
    File must be .json and contain only a dict
    '''
    with open(filename, "r") as read_file:
        data = json.load(read_file)
    if not key in data.keys():
        Error_Window('Key "' + key + '" does not exist.')
        return ""
    data[key] = value
    with open(filename, "w") as write_file:
        json.dump(data, write_file)
