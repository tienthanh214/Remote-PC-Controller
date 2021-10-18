from src.mysocket import MySocket
from tkinter import ttk
import tkinter as tk
import src.textstyles as textstyle
import src.themecolors as THEMECOLOR


class Filesystem(tk.Frame):
    cols = ('Name', 'Type')

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self._image_bytes = None
        self.grid()
        self._socket = MySocket.getInstance()
        self.create_widgets()
        # self._socket.send_immediate('folder,')

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
        # Table config
        self.tbl_container.heading('Name', text='Name')
        self.tbl_container.column('Name', width=600, stretch=True)
        self.tbl_container.heading('Type', text='Type')
        self.tbl_container.column('Type', width=200, stretch=True)
        self.tbl_container.insert("", "end", values=['..', ''])
        self.show_result(
            [['binh', 'folder'], ['Thanh', 'folder'], ['Thi.txt', 'file'], ])

    def show_result(self, table):
        if len(table) == 0:
            table = [["N/A"] * 2]
        for row in table:
            self.tbl_container.insert("", "end", values=row)

    def clear_result(self):
        for rowid in self.tbl_container.get_children():
            self.tbl_container.delete(rowid)
