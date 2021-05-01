import tkinter as tk
import sys
import io
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk


LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


mock_data = [['1', 'Jim', '0.33'], ['2', 'Dave', '0.67'],
             ['3', 'James', '0.67'], ['4', 'Eden', '0.5']]


def messagebox(title="client", msg="Done", type="info"):
    # type are: warn, error, info
    if type == "error":
        tk.messagebox.showerror(title, msg)
    elif type == "warn":
        tk.messagebox.showwarning(title, msg)
    else:
        tk.messagebox.showinfo(title, msg)


class inputbox(tk.Frame):
    # Mainly used for killing and starting application or process
    def __init__(self, master, cmd="?", tl="?", btn="?"):
        super().__init__(master)
        self.master = master
        self.master.title(tl + " " + cmd)

        self.input_field = tk.Entry(
            self.master, textvariable="Nhập ID", width=30)
        self.input_field.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_get = tk.Button(self.master, text=btn, width=15)
        self.btn_get.pack(side=tk.LEFT, padx=10, pady=10)

    def getvalue(self):
        return self.input_field.get()
