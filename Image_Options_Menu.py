import tkinter as tk

class UI(tk.Frame):
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)

        self.lbl_vmin = tk.Label(self, text="vmin:")
        self.entry_vmin = tk.Entry(self, width=5)
        self.entry_vmin.insert(0, 0)

        self.lbl_vmax = tk.Label(self, text="vmax:")
        self.entry_vmax = tk.Entry(self, width=5)
        self.entry_vmax.insert(0, 255)

        self.flipud = tk.BooleanVar()
        self.flipud.set(False)
        self.lbl_flipud = tk.Label(self, text="Flip U/D:")
        self.cbtn_flipud = tk.Checkbutton(self, variable=self.flipud,
                                onvalue=True, offvalue=False)

        # Gridding
        self.lbl_vmin.grid(row=0, column=0)
        self.entry_vmin.grid(row=0, column=1, padx=2)
        self.lbl_vmax.grid(row=0, column=2)
        self.entry_vmax.grid(row=0, column=3, padx=2)
        self.lbl_flipud.grid(row=0, column=4)
        self.cbtn_flipud.grid(row=0, column=5, padx=2)

    def get(self):
        vmin = int(self.entry_vmin.get())
        vmax = int(self.entry_vmax.get())
        flipud = self.flipud
        return (vmin, vmax, flipud)

def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()