import tkinter as tk
import winsound
import numpy as np
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import json
import os
import shutil

#-------------------------------------------------
# Message Windows
#-------------------------------------------------
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

#-------------------------------------------------
# Image display
#-------------------------------------------------
def load_image(img_path, k=1.0, ratio=2.0, base=200):
    '''
    Input:
        -img_path: string, filepath to plt.imread-acceptable source
        -k: float, scale factor
        -ratio: float, aspect ratio (W:H)
        -base: int, W/H dimensions at k=1.0
    Output:
        -tkinter PhotoImage
    '''

    # Read file
    img_arr = plt.imread(img_path)
    img_arr = (img_arr*255).astype(np.uint8)
    img = Image.fromarray(img_arr)

    # Fit to shape
    if (k == 0):
        k = 1
    shape = (int(ratio * k * base), int(k * base))
    img = img.resize(shape, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

def max_num_in_dir(path):
    '''
    Returns the max numbered file in a given directory
    Expects all files in directory to be pics in convention: name-xxxx
    with xxxx representing number
    '''
    pic_names = os.listdir(path)
    nums = []
    for name in pic_names:
        pic = name.partition(".")[0]
        pic = pic.partition("-")[2]
        try:
            pic = int(pic)
            nums.append(pic)
        except:
            Helpers.Error_Window("Bad filename: " + name)
    if (len(nums) == 0):
        return None
    else:
        return max(nums)

def to_4_digit(num):
    '''
    Returns a 4-digit string of the input positive int
    Returns '9999' if num is more than four digits
    Returns '-001' if num is negative
    '''
    if (num < 0):
        return "-001"
    elif (num >= 9999):
        return "9999"
    elif (num > 999):
        return str(num)
    elif (num > 99):
        return "0" + str(num)
    elif (num > 9):
        return "00" + str(num)
    else:
        return "000" + str(num)

#-------------------------------------------------
# File management
#-------------------------------------------------

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

def save_most_recent(src, dest):
    '''
    Copies the most recent file in the source directory into the destination
    Assumes alphabetically last will be most recent, as is true for convention:
    YYYYMMDD_diagnostic_s###
    '''
    files = os.listdir(src)
    files = sorted(files)
    path = src + "/" + files[-1]
    shutil.copy(path, dest)
    

    
