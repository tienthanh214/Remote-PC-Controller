from src.mysocket import MySocket
from tkinter import ttk
import tkinter as tk
import src.textstyles as textstyle
import src.themecolors as THEMECOLOR
import pickle


class Filesystem(tk.Frame):
    cols = ('Name', 'Type')
    id = 0

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self._image_bytes = None
        self.grid()
        self._socket = MySocket.getInstance()
        self.create_widgets()
        self.initial_fecth()

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
            self, yscrollcommand=self.scb_vertical.set, show='tree headings', height=24)
        self.tbl_container.grid(
            row=1, column=1, sticky=tk.N+tk.S+tk.W+tk.E, padx=0, pady=0)
        # Scrollbars config
        self.scb_vertical.config(command=self.tbl_container.yview)
        # Table config
        # self.tbl_container.heading('Name', text='Name',  anchor='w')
        # self.tbl_container.column('Name', width=400, stretch=True)
        # self.tbl_container.heading('Type', text='Type',  anchor='w')
        # self.tbl_container.column('Type', width=200, stretch=True)
        self.tbl_container.heading('#0', text='Folder', anchor='w')
        self.tbl_container.column('#0', width=800, stretch=True)

    def show_result(self, table):
        if len(table) == 0:
            table = [["N/A"] * 2]
        for row in table:
            self.tbl_container.insert("", "end", values=row)

    def clear_result(self):
        for rowid in self.tbl_container.get_children():
            self.tbl_container.delete(rowid)

    def next_id(self):
        id = Filesystem.id + 1
        return id

    def initial_fecth(self):
        self._socket.send('folder,view,\\')
        result = self._socket.receive()
        self.tbl_container.insert(
            parent='', index=0, iid='\\', text='\\', open=False)
        self.expand_dir('\\', pickle.loads(result))

    def expand_dir(self, parent, subtree):
        id = 0
        for item in subtree:
            self.tbl_container.insert(
                parent=parent, index=id, iid=item[0], text=item[0], open=False)
            id = id + 1
