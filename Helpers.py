import tkinter as tk
import winsound
import numpy as np
from PIL import Image, ImageTk, ImageGrab
from matplotlib import pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib import cm
import json
import os
import shutil
from datetime import date
from time import strftime

#-------------------------------------------------
# Generic Data Manipulation
#-------------------------------------------------

def get_suffix(word, delimeter):
    ''' Returns the part of word after the last instance of 'delimeter' '''
    while (delimeter in word):
        word = word.partition(delimeter)[2]
    return word

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
        self.root.geometry("500x50")
        
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
        self.root.geometry("500x50")
        
        self.lbl = tk.Label(self.root, text="Error: " + txt)
        self.lbl.pack()
        winsound.PlaySound("SystemExit", winsound.SND_ASYNC)
        
        self.root.mainloop()

#-------------------------------------------------
# Image display
#-------------------------------------------------
def rgb2gray(rgb):
    '''
    Convert the 3-channel rgb image into grayscale
    Developed by Yong Ma for Daq_Yong_v2.py
    '''
    '''
    if ((len(rgb.shape)) == 3):
        r, g, b = rgb[:,:,0] , rgb[:,:,1] , rgb[:,:,2]
    elif ((len(rgb.shape)) == 2):
        r, g, b = rgb[:,:,0] , rgb[:,:,1] , rgb[:,:,0]
    else:
        r, g, b = rgb[:,:,0] , rgb[:,:,0] , rgb[:,:,0]
    gray  = 0.2989 * r + 0.587 * g + 0.114 * b
    return gray
    '''
    r, g, b = rgb[:,:,0] , rgb[:,:,1] , rgb[:,:,2]
    gray  = 0.2989 * r + 0.587 * g + 0.114 * b
    return gray

def resize_image(img, k, ratio, base):
    if (k == 0):
        k = 1
    shape = (int(ratio * k * base), int(k * base))
    return img.resize(shape, Image.ANTIALIAS)

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
    img = Image.open(img_path)
    img = resize_image(img, k, ratio, base)
    return ImageTk.PhotoImage(img)
    '''
    # Read file
    img = plt.imread(img_path)
    img = Image.fromarray(img.astype('uint8'))
    # Fit to shape
    
    if (k == 0):
        k = 1
    shape = (int(k * base), int(ratio * k * base))
    img = np.resize(img0, shape)
    img = Image.fromarray(img.astype('uint8'))
    # vmin and vmax depends on diagnostic
    #img = plt.imshow(img)
    
    #img.pcolormesh(np.flipud(img),  vmin=0, vmax=255, cmap = cm.magma, rasterized = True)
    
    return ImageTk.PhotoImage(img)
    '''
def plot_image(img_path, root, k=1.0, ratio=2.0, base=200):
    '''
    Input:
        -img_path: string, filepath to plt.imread-acceptable source
        -k: float, scale factor
        -ratio: float, aspect ratio (W:H)
        -base: int, W/H dimensions at k=1.0
    Output:
        -tkinter Canvas of plt Figure
    '''
    img = plt.imread(img_path)

    img = rgb2gray(img)
    plt.pcolormesh(np.flipud(img),  vmin=0, vmax=255, cmap = cm.magma, rasterized = True)
    
    img = Image.fromarray(img.astype('uint8'))
    if (k == 0):
        k = 1
    shape = (int(ratio * k * base), int(k * base))
    img = img.resize(shape, Image.ANTIALIAS)
    
    np.array(img)
    
    # Place on canvas
    fig = Figure()
    plot1 = fig.add_subplot(111)
    # DEV NOTE: have in-GUI feature to edit vmin and vmax
    plot1.imshow(img, vmin=0, vmax=255)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    #toolbar = NavigationToolbar2Tk(canvas, root)
    #toolbar.update()
    return canvas.get_tk_widget()

    '''
    # Read file
    img0 = plt.imread(img_path)

    # Fit to shape
    if (k == 0):
        k = 1
    shape = (int(k * base), int(ratio * k * base), 3)
    img0 = np.resize(img0, shape)
    #img = Image.fromarray(img.astype('uint8'))
    # vmin and vmax depends on diagnostic

    # Place on canvas
    fig = Figure()
    plot1 = fig.add_subplot(111)
    # DEV NOTE: have in-GUI feature to edit vmin and vmax
    plot1.imshow(img0, vmin=0, vmax=255)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    #toolbar = NavigationToolbar2Tk(canvas, root)
    #toolbar.update()
    return canvas.get_tk_widget()
    '''
    

def test_plot():
    root = tk.Tk()
    text = ".\\Old Working Code\\Hercules Data\\Hercules Data for 4 shots\\ESPEC\\20201119_ESPEC_s019.tif"
    img = plot_image(text, root)
    img.pack()
    root.mainloop()

def max_num_in_dir(path):
    '''
    Returns the max numbered file in a given directory
    Expects all files in directory to be pics in convention:
    YYYYMMDD_diagnostic_s###
    '''
    pic_names = os.listdir(path)
    nums = []
    for name in pic_names:
        if not ".tif" in name:
            continue
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

def check_saved(dest, filename):
    ''' Checks whether file saving functions completed and creates
        appropriate message window
    '''
    if (os.path.isfile(dest + "/" + filename)):
        return True
    else:
        return False

def copy_raw_data(src, dest, num, diag):
    '''
    Copies file at location 'src' to directory 'dest'
    with naming convention: diagnostic_date_s###
    '''
    ext = get_suffix(src, ".")
    today = date.today()
    name = diag + "_" + today.strftime("%Y%m%d")
    name += "_s" + to_3_digit(num) + "." + ext
    shutil.copy(src, dest + "/" + name)

def save_most_recent(src, dest, diag):
    '''
    Copies the most recently edited file in the source directory into the
    destination
    src: string, source file
    dest: string, destination directory
    diag: string, name of diagnostic
    '''
    # Identify most recent file
    files = os.listdir(src)
    new_files = []
    for file in files:
        new_files.append(src + "/" + file)
    path = max(new_files, key=os.path.getctime)
    
    # Isolate shot number from src
    filename = path.partition(src)[2]
    if ("_s" in filename):
        num = filename.partition("_s")[2]
    elif ("shot" in filename):
        num = filename.partition("shot")[2]
    else:
        Error_Window("Bad filename: " + filename)
        return
    num = num.partition(".")[0]
    try:
        num = int(num)
    except:
        Error_Window("Bad filename: " + filename)
        return

    # Copy file
    copy_raw_data(path, dest, num, diag)

def save_by_number(src, dest, num, diag):
    '''
    Copies file including 's###' or 'shot#' in the source directory into the
    destination, then renames to naming convention:
    diagnostic_date_s###
    src: string, source file
    dest: string, destination directory
    num: string or int, minimum-digit number (no leading zeros)
    diag: string, name of diagnostic
    '''
    files = os.listdir(src)
    for file in files:
        convention_1 = "s" + to_3_digit(num)
        convention_2 = "shot" + str(num)
        if (convention_1 in file) or (convention_2 in file):
            path = src + "/" + file
            copy_raw_data(path, dest, num, diag)

date_default = {
        "year": "0001",
        "month": "01",
        "day": "01"
        }

def get_today():
    '''
    Returns a datetime.date object representing today.
    If there has been a date set manually, it uses that.
    Otherwise, it uses date.today()
    '''
    today = get_from_file("date", "setup.json")
    if (today != date_default):
        y = int(today["year"])
        m = int(today["month"])
        d = int(today["day"])
        return date(y, m, d)
    else:
        return date.today()
    
def take_screenshot():
    img = ImageGrab.grab()
    dest = "./Screenshots"
    timestamp = strftime("%Y-%m-%d_%H.%M.%S")
    name = dest + "/" + timestamp + ".png"
    img.save(name, format="PNG")

def test_screenshots(period):
    import time
    baseline = time.perf_counter()
    elapsed = time.perf_counter() - baseline
    iterations = 0
    while (elapsed < period):
        take_screenshot()
        iterations += 1
        elapsed = time.perf_counter() - baseline
    print(iterations / period)
