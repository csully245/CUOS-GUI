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
    img = Image.open(img_path)

    # Fit to shape
    if (k == 0):
        k = 1
    shape = (int(ratio * k * base), int(k * base))
    img = img.resize(shape, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

def rgb2gray(rgb):
	'''
        Convert the 3-channel rgb image into grayscale
        Developed by Yong Ma for Daq_Yong_v2.py
	'''
	r, g, b = rgb[:,:,0] , rgb[:,:,1] , rgb[:,:,2]
	gray  = 0.2989 * r + 0.587 * g + 0.114 * b
	return gray

def max_num_in_dir(path):
    '''
    Returns the max numbered file in a given directory
    Expects all files in directory to be pics in convention:
    YYYYMMDD_diagnostic_s###
    '''
    pic_names = os.listdir(path)
    nums = []
    for name in pic_names:
        pic = name.partition(".")[0]
        pic = pic.partition("_s")[2]
        try:
            pic = int(pic)
            nums.append(pic)
        except:
            Error_Window("Bad filename: " + name)
    if (len(nums) == 0):
        return None
    else:
        return max(nums)

def to_3_digit(num):
    '''
    Returns a 3-digit string of the input positive int
    Returns '999' if num is more than three digits
    Returns '000' if num is negative
    '''
    num = int(num)
    if (num < 0):
        return "000"
    elif (num >= 999):
        return "999"
    elif (num > 99):
        return str(num)
    elif (num > 9):
        return "0" + str(num)
    else:
        return "00" + str(num)

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

def save_by_number(src, dest, num):
    '''
    Copies file including 's###' in the source directory into the destination
    '''
    files = os.listdir(src)
    for file in files:
        if ("s" + num) in file:
            path = src + "/" + file
            shutil.copy(path, dest)
    

    
