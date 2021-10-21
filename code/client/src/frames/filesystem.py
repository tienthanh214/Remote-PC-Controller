from src.mysocket import MySocket
from tkinter import ttk
import tkinter as tk
import src.textstyles as textstyle
import src.themecolors as THEMECOLOR
import pickle
import struct as stc
import os


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
        self.tbl_container.heading('#0', text='Folder', anchor='w')
        self.tbl_container.column('#0', width=800, stretch=True)
        self.tbl_container.bind("<Double-1>", lambda e: self.onDoubleClick(e))

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
        local_id = 0
        for item in subtree:
            this_id = parent
            if parent != '\\':
                this_id += '\\'
            this_id += item[0]
            self.tbl_container.insert(
                parent=parent, index=local_id, iid=this_id, text=item[0], open=False)
            local_id = local_id + 1

    def onDoubleClick(self, event):
        target = self.tbl_container.identify('item', event.x, event.y)
        self._socket.send('folder,view,' + target)
        result = self._socket.receive()
        self.expand_dir(target, pickle.loads(result))

    def receive(self, filename):
        raw_msglen = self._socket.recv(4)
        if not raw_msglen:
            return None
        msglen = stc.unpack('>I', raw_msglen)[0]
        f = open(filename, "wb")
        curlen = 0
        while curlen < msglen:
            packet = self._socket.recv(min(4096 * 2, msglen - curlen))
            if not packet:
                break
            f.write(packet)
            curlen += len(packet)
            # use curlen/msglen to show progress bar
        f.close()

    def send_file(self, filename):
        print(filename)
        try:
            f = open(filename, "rb")
        except:
            print("file not found")
            return
        filesize = os.path.getsize(filename)
        self._socket.send(stc.pack('>I', filesize))
        print(filesize)
        prog = 0
        while True:
            bytes_read = f.read(4096 * 2)
            if not bytes_read:
                break
            self._socket.sendall(bytes_read)
            prog += len(bytes_read)
            # use prog/filesize to show progress bar
        f.close()
