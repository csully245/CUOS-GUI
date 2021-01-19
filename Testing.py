import tkinter as tk
from PIL import Image, ImageTk, ImageGrab, ImageOps
import time
import pyautogui
import threading
from numpy import median

import Helpers

class Example_UI:
    def add_widget(self, func):
        self.start_time = time.perf_counter()
        widget, img = func("./assets/CUOS-med.png", self.root, k=1.5)
        widget.pack()
        self.runtime = time.perf_counter() - self.start_time
        
        time.sleep(self.safety_delay)
        self.root.quit()
        self.root.destroy()

    def __init__(self, func, safety_delay=0.5):
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.root.attributes('-topmost', True)
        self.safety_delay=safety_delay
        self.btn = tk.Button(self.root, text="Test",
                             command=lambda: self.add_widget(func))
        self.btn.pack()
        self.root.mainloop()

def click_top_center(delay=0.1):
    time.sleep(delay)
    width, height = pyautogui.size()
    x, y = pyautogui.position()
    pyautogui.click(width*0.5, height*0.05, button="left")
    pyautogui.moveTo(x, y)

def start(test, runs=30, delay=0.1, safety_delay=0.5):
    runtimes = []
    for _ in range(runs):
        t1 = threading.Thread(target=click_top_center, args=(delay,))
        t1.start()
        runtime = test(safety_delay)
        print(runtime)
        runtimes.append(runtime)
        time.sleep(safety_delay)
    med = round(median(runtimes), 4)
    print("Median runtime (%s runs): %s s" %(runs, med))
    
# Tests
def test_plot_image(safety_delay=0.0):
    ui = Example_UI(Helpers.plot_image, safety_delay)
    return ui.runtime
