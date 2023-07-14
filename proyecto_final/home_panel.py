import tkinter as tk
from tkinter import filedialog

class HomePanel:

    def __init__(self, window, self_window):
        self.window = window
        self.window_self = self_window
        self.panel = tk.Frame(self.window)
        self.lblTitle = tk.Label(self.panel, text="Master Mind", bg="white", fg="black", font="none 12 bold")
        self.btnSelectFile = tk.Button(self.panel, text="Seleccionar archivo", command=self.open_file_chooser)
        self.lblTitle.pack()
        self.btnSelectFile.pack()
        self.panel.pack()
    
    def open_file_chooser(self):
        self.file = filedialog.askopenfilename(initialdir="/", title="Seleccione el CSV", filetypes=[("Archivo CSV", ".csv")])
        if self.file != "":
            self.window_self.file = self.file
            self.window_self.open_selecter_panel()