import Helpers
import Image_Options_Menu

import os
import tkinter as tk


class UI(tk.Frame):
    """
    Container for each diagnostic frame. Shows the most recent data from each diagnostic.
    """

    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)

        self.lbl_shot_num = tk.Label(self, text="Shot #000")
        self.lbl_shot_num.grid(row=0, column=0)
        self.lbl_shot_num.config(font=("Arial", 24))

        # Get diagnostics
        self.shotrundir = Helpers.get_from_file("shotrundir")
        diagnostics = self.get_diagnostics()

        # Display tiled images
        self.fr_tiled = tk.Frame(self)
        self.fr_tiled.grid(row=1, column=0)
        rows = 2
        columns = 3
        self.frames = []
        for c in range(columns):
            for r in range(rows):
                if diagnostics:
                    diagnostic = diagnostics[0]
                    del diagnostics[0]
                else:
                    diagnostic = ""
                fr = DiagnosticDisplay(self.fr_tiled, diagnostic, self.shotrundir)
                fr.grid(row=r, column=c, padx=10, pady=5)
                self.frames.append(fr)

        self.btn_update = tk.Button(self, text="Update", command=lambda: self.update_diagnostics())
        self.btn_update.grid(row=2, column=0)

    def load_from_workspace(self, workspace):
        '''
        Loads default data from input values generated from selected workspace
        .json file
        Workspace: list containing saved workspaced
        '''
        for fr, wksp in zip(self.frames, workspace):
            fr.load_from_workspace(wksp)

    def get_workspace(self):
        '''
        Returns all variables needed to later recreate an identical frame
        '''
        workspace = []
        for fr in self.frames:
            workspace.append(fr.get_workspace())
        return workspace

    def get_diagnostics(self):
        '''
        Returns a list of enabled diagnostic names
        '''
        out = []
        diagnostic_data = Helpers.get_from_file("diagnostics", "diagnostic_data.json")
        for diagnostic in diagnostic_data:
            path = diagnostic["dir_temp"]
            if os.path.isdir(path) and diagnostic["enabled"]:
                out.append(diagnostic)
        return out

    def update_diagnostics(self):
        self.shotrundir = Helpers.get_from_file("shotrundir", "setup.json")
        diagnostics = self.get_diagnostics()
        for frame in self.frames:
            if diagnostics:
                diagnostic = diagnostics[0]
                del diagnostics[0]
            else:
                diagnostic = {
                    "diagnostic": "",
                    "dir_temp": "./",
                    "file_extension": ".tif",
                    "process": "Raw Image",
                    "enabled": True}
            frame.update_diagnostic(diagnostic, self.shotrundir)
        shot_num = Helpers.get_from_file("shot_num", "setup.json")
        shot_num = Helpers.to_3_digit(shot_num)
        text = "Shot #" + shot_num
        self.lbl_shot_num.config(text=text)


class DiagnosticDisplay(tk.LabelFrame):
    """
    Frame for displaying the most recent data from each diagnostic
    """

    def __init__(self, master, diagnostic, shotrundir, **options):
        tk.LabelFrame.__init__(self, master, text=diagnostic, **options)
        self.diagnostic = diagnostic
        self.shotrundir = shotrundir

        self.img_path = Helpers.default_img_path
        self.wgt_img, self.img = Helpers.plot_image(self.img_path, self,
                                                    display_process="Raw Image")

        self.fr_options = Image_Options_Menu.UI(self)

        # Gridding
        self.wgt_img.grid(row=0, column=0)
        self.fr_options.grid(row=1, column=0)

    def update_image(self):
        """Checks for more recent data for the diagnostic and updates image"""
        if self.diagnostic == "":
            path = Helpers.default_img_path
        else:
            files = []
            for file in os.listdir(self.diagnostic_path):
                filename = os.path.join(self.diagnostic_path, file)
                extensions = [".png", ".jpg", ".jpeg", ".tif", ".tiff"]
                if not os.path.isfile(filename):
                    continue
                for extension in extensions:
                    if extension in filename.lower():
                        files.append(filename)
                        break
            if files:
                path = max(files, key=os.path.getctime)
            else:
                path = Helpers.default_img_path
        self.img_path = path
        if not (os.path.isfile(self.img_path)):
            error_text = "Image path does not exist: " + self.img_path
            Helpers.ErrorWindow(error_text)
            self.img_path = Helpers.default_img_path

        # Plot
        vmin, vmax, flipud = self.fr_options.get()
        self.wgt_img.grid_forget()
        Helpers.delete_img(self.img)
        if self.img_path == Helpers.default_img_path:
            self.wgt_img, self.img = Helpers.plot_image(self.img_path,
                                                        self, display_process="Raw Image")
        else:
            self.wgt_img, self.img = Helpers.plot_image(self.img_path,
                                                        self, display_process=self.display_process,
                                                        vmin=vmin, vmax=vmax,
                                                        flipud=flipud)
        self.wgt_img.grid(row=0, column=0)

    def update_diagnostic(self, diagnostic, shotrundir):
        """ Updates all diagnostic-based internal data """
        self.config(text=diagnostic["diagnostic"])
        self.diagnostic = diagnostic["diagnostic"]
        self.diagnostic_path = diagnostic["dir_temp"]
        self.display_process = diagnostic["process"]
        self.shotrundir = shotrundir
        self.update_image()


# -------------------------------------------------
# Execution
# -------------------------------------------------

def test():
    root = tk.Tk()
    gui = UI(root)
    gui.pack()
    root.attributes('-topmost', True)
    root.mainloop()
