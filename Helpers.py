import tkinter as tk
import winsound
import numpy as np
from PIL import Image, ImageTk, ImageGrab, ImageOps
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm
import json
import os
import shutil
from datetime import date
import time
import pyautogui
import threading

# -------------------------------------------------
# Constants
# -------------------------------------------------

default_img_path = "assets/CUOS-med.png"
date_default = {
    "year": "0001",
    "month": "01",
    "day": "01"
}
default_filename = "setup.json"


# -------------------------------------------------
# Generic Data Manipulation
# -------------------------------------------------

def get_suffix(word, delimeter):
    ''' Returns the part of word after the last instance of 'delimeter' '''
    while (delimeter in word):
        word = word.partition(delimeter)[2]
    return word


# -------------------------------------------------
# Message Windows
# -------------------------------------------------
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


# -------------------------------------------------
# Image display
# -------------------------------------------------

def rgb2gray(rgb):
    '''
    Converts the 3-channel rgb image into grayscale
    Developed by Yong Ma for Daq_Yong_v2.py
    '''
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.587 * g + 0.114 * b
    return gray


def resize_image(img, k, ratio, base):
    '''
    Resizes PIL image

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
    Plots image using ImageTk.PhotoImage
    
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


def plot_image(img_path, root, k=1.0, ratio=1.5, base=-1, recolor=False,
               colormap=cm.magma, vmin=0, vmax=255, flipud=False):
    '''
    Plots image using plt.imshow and tk.Canvas
    Still in development and to be tested
    
    Input:
        -img_path: string, filepath to plt.imread-acceptable source
        -k: float, scale factor
        -ratio: float, aspect ratio (W:H)
        -base: int, W/H dimensions at k=1.0
        -flipud: bool, whether or not to flip img vertically
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
                              figsize=(ratio * base_size, base_size))
    xleft, xright = plot1.get_xlim()
    ybottom, ytop = plot1.get_ylim()
    plot1.set_aspect(abs((xright - xleft) / (ybottom - ytop)) * ratio)
    plot1.tick_params(axis='both', which='both',
                      bottom=False, left=False, labelbottom=False,
                      labelleft=False)
    img_arr = np.asarray(img)
    if len(img_arr.shape) > 2:
        img_arr = rgb2gray(img_arr)
    if flipud:
        img_arr = np.flipud(img_arr)
    if recolor:
        plot1.imshow(img_arr, vmin=vmin, vmax=vmax, cmap=colormap,
                     rasterized=True, aspect='auto')
    else:
        plot1.imshow(img_arr, rasterized=True, aspect='auto')

    # Return tk.Canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas = canvas.get_tk_widget()
    if base == -1:
        dimensions = get_from_file("dimensions", "assets/dimensions.json")
        base = dimensions["img_size"]
    canvas.configure(width=ratio * base, height=base)
    return canvas, fig


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


# -------------------------------------------------
# File management
# -------------------------------------------------

def get_from_file(key, filename=default_filename):
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


def edit_file(key, value, filename=default_filename):
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


def save_most_recent(src, dest, diag, num,
                     extensions=["png", "jpg", "jpeg", "tif", "tiff"]):
    '''
    Copies the most recently edited file in the source directory into the
    destination
    
    Inputs:
    -src: string, source file
    -dest: string, destination directory
    -diag: string, name of diagnostic
    -num: int/string, shot number
    -extensions: list of strings, supported file types
    '''
    # Identify most recent file
    files = os.listdir(src)
    new_files = []
    for file in files:
        ext = get_suffix(file, ".").lower()
        if ext in extensions:
            new_files.append(src + "/" + file)
    path = max(new_files, key=os.path.getctime)
    num = to_3_digit(num)

    # Copy raw data
    ext = get_suffix(path, ".")
    today = get_today()
    name = diag + "_" + today.strftime("%Y%m%d")
    name += "_s" + to_3_digit(num) + "." + ext
    shutil.copy(path, os.path.join(dest, name))


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

def save_plots(num, shotrundir, delay=0.8):
    '''
    Saves a screenshot, cropped to include only the recent display

    Inputs:
    -num: int/str, shot number
    -shotrundir: str, shot run directory
    -delay: numeral, seconds to delay before taking screenshot
    '''

    # Define threads
    def thread_a(x_button, y_button):
        """ Switches tab to Recent Image Display """
        width, height = pyautogui.size()
        width *= x_button
        height *= y_button
        x, y = pyautogui.position()
        pyautogui.click(width, height, button="left")
        pyautogui.moveTo(x, y)

    def thread_b(num, shotrundir, delay, x_button, y_button):
        """ Saves screenshot """
        # Delay to leave time for tab switching
        time.sleep(delay)

        # Take and crop screenshot
        img = ImageGrab.grab()
        '''
        width, height = img.size
        left = int(width * left)
        right = int(width * right)
        top = int(height * top)
        bottom = int(height * bottom)
        img = img.crop((left, top, right, bottom))
        '''

        # Save screenshot
        dest = os.path.join(shotrundir, "Aggregated Plots")
        if not (os.path.isdir(dest)):
            os.mkdir(dest)
        filename = "plot_agg_s" + to_3_digit(num)
        ext = ".png"
        # Check for duplicates
        tag = "_v"
        if os.path.isfile(os.path.join(dest, filename) + ext):
            # Add "_v#" tag for alternate save
            base = os.path.join(dest, filename)
            base = base.partition(ext)[0]
            tag = "_v"
            num = 1
            while os.path.isfile(base + tag + str(num) + ext):
                num += 1
            filename += tag + str(num)
        filename += ext
        # Save
        img.save(os.path.join(dest, filename), format="PNG")

    # Get dimensions
    '''
    -x_button, y_button: float, ration of screen to use to press the button
        for Recent Image Display
    
    dimensions.json must be adjusted to match the settings of a particular
    computer screen. Using pyautogui.position() is a good way to get the
    coordinates of a certain mouse position
    '''
    dimensions = get_from_file("dimensions", "./assets/dimensions.json")
    x_button = dimensions["x_button"]
    y_button = dimensions["y_button"]

    # Operate
    t1 = threading.Thread(target=thread_b, args=(num, shotrundir, delay,
                                                 x_button, y_button))
    t1.start()
    thread_a(x_button, y_button)