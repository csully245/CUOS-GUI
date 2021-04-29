import Startup

import tkinter as tk


class UI(tk.Frame):
    """
    Frame for quick user questions.
    """

    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)
        self.frames = []
        self.fr_startup_menu = Startup.StartupMenu(self)
        self.fr_startup_menu.grid(row=0, column=0)
        self.frames.append(self.fr_startup_menu)

    def clear(self):
        """ Removes all frames. Still available for data access """
        for frame in self.frames:
            frame.grid_forget()


def test():
    root = tk.Tk()
    fr = UI(root)
    fr.pack()
    root.mainloop()
