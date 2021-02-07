import Helpers

import tkinter as tk
from PIL import Image, ImageTk, ImageGrab, ImageOps
import time
import pyautogui
import threading
from numpy import median

class Example_UI:
    def __init__(self, func, safety_delay=0.5):
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.root.attributes('-topmost', True)
        self.safety_delay=safety_delay
        self.runtime=0.0
        self.btn = tk.Button(self.root, text="Test",
                             command=lambda: self.add_widget(func))
        self.btn.pack()
        self.root.mainloop()
    
    def add_widget(self, func):
        self.start_time = time.perf_counter()
        widget, img = func("./assets/CUOS-med.png", self.root, recolor=True,
                           k=1.5)
        widget.pack()
        self.runtime = time.perf_counter() - self.start_time
        
        time.sleep(self.safety_delay)
        self.root.quit()
        self.root.destroy()

def click_top_center(delay=0.1):
    time.sleep(delay)
    width, height = pyautogui.size()
    x, y = pyautogui.position()
    pyautogui.click(width*0.5, height*0.05, button="left")
    pyautogui.moveTo(x, y)

def test_runtime(test, runs=50, delay=0.1, safety_delay=0.5, verbose=False):
    '''
    Repeatedly runs a structured test to determine the runtime for image
    displaying and processing functions.
    
    Inputs:
    -test: function handle, returning a numeric runtime
    -runs: int, how many times to run the test
    -delay: numeral, how long in seconds to wait between opening and clicking
            the window. Increase if tests are stalling midway through. Does not
            affect runtime
    -safety_delay: numeral, how long in seconds to wait after each opening and
            closing of a window. Intended to prevent headaches and seizures
            due to the window flashing on the screen repeatedly
    -verbose: bool, whether or not to print results
    
    Outputs:
    -med: float, median runtime
    '''
    runtimes = []
    for _ in range(runs):
        t1 = threading.Thread(target=click_top_center, args=(delay,))
        t1.start()
        runtime = test(safety_delay)
        if (verbose):
            print(runtime)
        runtimes.append(runtime)
        time.sleep(safety_delay)
    med = round(median(runtimes), 4)
    if (verbose):
        print("Median runtime (%s runs): %s s" %(runs, med))
    return med
    
# Tests
def test_plot_image(safety_delay=0.0):
    ui = Example_UI(Helpers.plot_image, safety_delay)
    return ui.runtime

def test_load_image(safety_delay=0.0):
    ui = Example_UI(Helpers.load_image, safety_delay)
    return ui.runtime
