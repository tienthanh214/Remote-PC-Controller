from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from threading import Thread
from src.mysocket import MySocket
import tkinter as tk
from tkinter import ttk
import io
import src.textstyles as textstyle
import src.themecolors as THEMECOLOR


class Filesystem(tk.Frame):
    cols = ('Name', 'Type')

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self._image_bytes = None
        self.grid()
        self.create_widgets()

    def clean_activity(self):
        pass

    def create_widgets(self):
        # Create top left padding for the frame
        self.spacer = tk.Label(self, bg=THEMECOLOR.body_bg,
                               highlightthickness=0, height=2, width=12, anchor=tk.E)
        self.spacer.grid(row=0, column=0)
        # Define these scrollbar before hand
        self.scb_vertical = tk.Scrollbar(self,)
        self.scb_vertical.grid(row=1, column=2, sticky=tk.N+tk.S)
        # Display the file system tree
        self.tbl_container = ttk.Treeview(
            self, columns=Filesystem.cols, show="headings", yscrollcommand=self.scb_vertical.set, selectmode="browse", height=24)
        self.tbl_container.grid(
            row=1, column=1, sticky=tk.N+tk.S+tk.W+tk.E, padx=0, pady=0)
        # Scrollbars config
        self.scb_vertical.config(command=self.tbl_container.yview)
        # Table title
        for col in Filesystem.cols:
            self.tbl_container.heading(col, text=col)
            self.tbl_container.column(col, width=400, stretch=True)