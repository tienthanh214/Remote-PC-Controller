from threading import currentThread
from src.mysocket import MySocket
from tkinter import ttk, filedialog
import tkinter as tk
import src.textstyles as textstyle
import src.themecolors as THEMECOLOR
import pickle
import struct as stc
import os


class Filesystem(tk.Frame):
    cols = ('Name', 'Type')
    id = 0
    DOWNLOAD_FOLDER = '../downloads/'

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self._image_bytes = None
        self.grid()
        self._socket = MySocket.getInstance()
        self.create_widgets()
        self.initial_fecth()
        # Get path delim based on operating system
        self.path_delim = '\\'      # for window
        if os.name == 'posix':
            self.path_delim = '/'   # for linux

    def clean_activity(self):
        pass

    def create_widgets(self):
        # Create top left padding for the frame
        self.spacer = tk.Label(self, bg=THEMECOLOR.body_bg,
                               highlightthickness=0, height=2, width=12, anchor=tk.E)
        self.spacer.grid(row=0, column=0)
        # Define these scrollbar before hand
        self.scb_vertical = tk.Scrollbar(self,)
        self.scb_vertical.grid(row=1, column=2, sticky=tk.N+tk.S, rowspan=3)
        # Display the file system tree
        self.tbl_container = ttk.Treeview(
            self, yscrollcommand=self.scb_vertical.set, show='tree headings', height=24)
        self.tbl_container.grid(
            row=1, column=1, sticky=tk.N+tk.S+tk.W+tk.E, padx=0, pady=0, rowspan=3)
        # Scrollbars config
        self.scb_vertical.config(command=self.tbl_container.yview)
        # Table config
        self.tbl_container.heading('#0', text='Folder', anchor='w')
        self.tbl_container.column('#0', width=600, stretch=True)
        self.tbl_container.bind("<Double-1>", lambda e: self.onDoubleClick(e))
        # Retrieve file from server
        self.btn_retrieve = tk.Button(
            self, text='Retrieve', command=self.retrieve_file, width=10, height=2)
        self.btn_retrieve.grid(row=1, column=3, sticky=tk.E, padx=10, pady=10)
        # Send file to server
        self.btn_send = tk.Button(
            self, text="Send", command=self.send_file, width=10, height=2)
        self.btn_send.grid(row=2, column=3, sticky=tk.E, padx=10, pady=10)
        # Delete file or folder
        self.btn_send = tk.Button(
            self, text="Delete", command=self.delete_file, width=10, height=2)
        self.btn_send.grid(row=3, column=3, sticky=tk.E, padx=10, pady=10)

    def retrieve_file(self):
        # Get id of the source
        cur_item = self.tbl_container.focus()
        # Send command to server
        self._socket.send('folder,copy,{},?'.format(cur_item))
        # Retrieve the file from server
        filename = cur_item.split('\\')[-1]
        self.receive(filename=filename)

    def send_file(self):
        # Get the file from client
        source = filedialog.askopenfilename(
            title="Select file", filetypes=[("all files", "*.*")])
        # Send command to server
        cur_item = self.tbl_container.focus()
        dirs = cur_item.split('\\')
        path = None
        filename = source.split(self.path_delim)[-1]
        if '.' in cur_item[-1]:
            # A file is in focus
            path = '\\'.join(dirs[0:-1]) + self.path_delim + filename
        else:
            # A folder in focus
            path = cur_item + self.path_delim + filename
        self._socket.send('folder,copy,?,{}'.format(path))
        # Client send file by chunks
        self.send(filename=source)

    def delete_file(self):
        cur_item = self.tbl_container.focus()
        self._socket.send('folder,del,{}'.format(cur_item))

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
            self.tbl_container.insert(parent=parent, index=local_id, iid=this_id,
                                      text=item[0], open=False, values=item[1])
            local_id = local_id + 1

    def onDoubleClick(self, event):
        target = self.tbl_container.identify('item', event.x, event.y)
        if len(self.tbl_container.get_children(target)) != 0:
            return
        self._socket.send('folder,view,' + target)
        result = self._socket.receive()
        self.expand_dir(target, pickle.loads(result))

    def receive(self, filename):
        raw_msglen = self._socket._sock.recv(4)
        if not raw_msglen:
            return None
        msglen = stc.unpack('>I', raw_msglen)[0]
        f = open(filename, "wb")
        curlen = 0
        while curlen < msglen:
            packet = self._socket.receive()
            if not packet:
                break
            f.write(packet)
            curlen += len(packet)
            # use curlen/msglen to show progress bar
        f.close()

    def send(self, filename):
        try:
            f = open(filename, "rb")
        except:
            print("file not found")
            return
        filesize = os.path.getsize(filename)
        self._socket._sock.sendall(stc.pack('>I', filesize))
        prog = 0
        while True:
            bytes_read = f.read(4096 * 2)
            if not bytes_read:
                break
            self._socket._sock.sendall(bytes_read)
            prog += len(bytes_read)
            # use prog/filesize to show progress bar
        f.close()
