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
    title = title.capitalize()
    if type == "error":
        tk.messagebox.showerror(title, msg)
    elif type == "warn":
        tk.messagebox.showwarning(title, msg)
    else:
        tk.messagebox.showinfo(title, msg)


class inputbox(tk.Frame):
    # Mainly used for killing and starting application or process
    def __init__(self, master, tl="?", cmd="?"):
        super().__init__(master)
        tl = tl.capitalize()
        cmd = cmd.capitalize()
        self.master = master
        self.master.title(tl + " " + cmd)
        self.master.resizable(False, False)

        self.input_field = tk.Entry(
            self.master, textvariable="Nhập ID", width=30)
        self.input_field.focus()
        self.input_field.pack(side=tk.LEFT, padx=20, pady=20)

        self.btn_get = tk.Button(self.master, text=cmd, width=15)
        self.btn_get.pack(side=tk.LEFT, padx=20, pady=20)

    def getvalue(self):
        return self.input_field.get()

    def killbox(self):
        self.master.destroy()
