import tkinter as tk
import winsound

'''
Helper functions and classes
'''

class Notice_Window:
    '''
    GUI template for notice messages, such as progress updates and errors
    '''
    def __init__(self, txt, error=True):
        self.root = tk.Tk()
        self.root.title("Notice")
        self.root.iconbitmap("assets/UM.ico")
        self.root.geometry("300x50")
        
        self.lbl = tk.Label(self.root, text=txt)
        self.lbl.pack(padx=10, pady=10)
        if (error):
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

        '''
        self.btn = tk.Button(self.root, text="Close", width=20, height=10,
                             command=self.root.destroy)
        self.btn.pack()
        '''
