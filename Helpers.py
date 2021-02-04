import tkinter as tk
import winsound
import numpy as np
from PIL import Image, ImageTk, ImageGrab, ImageOps
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
import time
import pyautogui

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

default_img_path = "./assets/CUOS-med.png"

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
    '''
    Inputs:
    -img: PIL Image
    -k: float, scale factor
    -ratio: float, aspect ratio (W:H)
    -base: int, W/H dimensions at k=1.0

    Outputs:
    PIL Image, resized
    '''
    if (k == 0):
        k = 1
    shape = (int(ratio * k * base), int(k * base))
    try:
        out = img.resize(shape, Image.ANTIALIAS)
    except ValueError:
        out = np.resize(np.asarray(img), shape)
        out = Image.fromarray(out)
    return out

def load_image(img_path, root, k=1.0, ratio=2.0, base=200, recolor=False,
                vmin=0, vmax=255):
    '''
    Plots image using Image.open and ImageTk.PhotoImage
    
    Input:
        -img_path: string, filepath to plt.imread-acceptable source
        -k: float, scale factor
        -ratio: float, aspect ratio (W:H)
        -base: int, W/H dimensions at k=1.0
        -recolor: bool, whether or not to recolor the image
        -black: color to use for black pixels in recolor
        -white: color to use for white pixels in recolor
    Output:
        -tuple: (tkinter Label, tkinter PhotoImage)
    '''
    img = Image.open(img_path)
    img = resize_image(img, k, ratio, base)
    if (recolor):
        black = "black"
        white = "white"
        img = np.asarray(img)
        img = np.clip(img, vmin, vmax)
        img = Image.fromarray(img)
        img = ImageOps.colorize(img.convert("L"), black=black, white=white)
    img = ImageTk.PhotoImage(img)
    return (tk.Label(root, image=img), img)

def plot_image(img_path, root, k=1.0, ratio=2.0, base=200, recolor=False,
               colormap=cm.magma, vmin=0, vmax=255, flipud=False):
    '''
    Plots image using plt.imread and tk.Canvas
    Still in development and to be tested
    
    Input:
        -img_path: string, filepath to plt.imread-acceptable source
        -k: float, scale factor
        -ratio: float, aspect ratio (W:H)
        -base: int, W/H dimensions at k=1.0
    Output:
        -tuple: (tkinter Canvas of plt Figure, plt subplot)
    
    Note: plt subplot garbage collection must be handled on application end
    '''
    
    # Create image plot
    img = Image.open(img_path)
    fig = Figure()

    # Edit plot settings
    base_size = 2.5
    fig, plot1 = plt.subplots(1, subplot_kw={'aspect': 'auto'},
                    figsize=(ratio*base_size,base_size))
    xleft, xright = plot1.get_xlim()
    ybottom, ytop = plot1.get_ylim()
    plot1.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
    plot1.tick_params(axis='both', which='both',
                    bottom=False, left=False, labelbottom=False,
                    labelleft=False)
    img_arr = np.asarray(img)
    if (len(img_arr.shape) > 2):
        img_arr = rgb2gray(img_arr)
    if (flipud.get()):
        img_arr = np.flipud(img_arr)
    if (recolor):
        plot1.imshow(img_arr, vmin=vmin, vmax=vmax, cmap=colormap,
                                    rasterized=True, aspect='auto')
    else:
        plot1.imshow(img_arr, rasterized=True, aspect='auto')

    # Return tk.Canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas = canvas.get_tk_widget()
    return (canvas, fig)

def delete_img(img):
    '''
    Handles cleanly deleting image sources across types:
    -plt.Figure
    -PIL.PhotoImage
    -tkinter.Canvas
    -np.ndarray
    '''
    if type(img) == Figure:
        plt.close(img)
    else:
        del img

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

def get_shot_num(path):
    ''' Returns the shot number (in str) of an image at path 'path' '''
    if ("_s" in path):
        out = path.partition("_s")[2]
    elif ("shot" in path):
        out = path.partition("shot")[2]
    else:
        out = path
    out = out.partition(".")[0]
    return out

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

def save_most_recent(src, dest, diag, num):
    '''
    Copies the most recently edited file in the source directory into the
    destination
    src: string, source file
    dest: string, destination directory
    diag: string, name of diagnostic
    num: int/string, shot number
    '''
    # Identify most recent file
    files = os.listdir(src)
    new_files = []
    for file in files:
        new_files.append(src + "/" + file)
    path = max(new_files, key=os.path.getctime)
    num = to_3_digit(num)
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

def save_plots(num, shotrundir, delay=0.5):
    '''
    Saves a screenshot, cropped to include only the recent display
    num: int/str, shot number
    shotrundir: str, shot run directory
    delay: numeral, seconds to delay before taking screenshot
    '''
    time.sleep(delay)
    width, height = pyautogui.size()
    width *= 0.20
    height *= 0.063
    pyautogui.click(width, height, button="left")

    img = ImageGrab.grab()
    width, height = img.size
    left = int(width * 0.01)
    right = int(width * 0.82)
    top = int(height * 0.079)
    bottom = int(height * 0.65)
    img = img.crop((left, top, right, bottom))

    dest = os.path.join(shotrundir, "Aggregated Plots")
    if not (os.path.isdir(dest)):
        os.mkdir(dest)
    filename = "plots_shot" + to_3_digit(num) + ".png"
    img.save(os.path.join(dest, filename), format="PNG")

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
