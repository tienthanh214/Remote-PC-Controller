from threading import currentThread
from src.mysocket import MySocket
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import tkinter as tk
import src.utils as utils
import src.textstyles as textstyle
import src.themecolors as THEMECOLOR
import pickle
import struct as stc
import os
import time


class Filesystem(tk.Frame):
    cols = ('Name', 'Type')
    id = 0
    DOWNLOAD_FOLDER = '../downloads/'

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self._image_bytes = None
        self.grid()
        self._socket = MySocket.getInstance()
        self.create_icons()
        self.create_widgets()
        self.initial_fetch()
        # Store path
        self.src_item = None
        # Get path delim based on operating system
        self.path_delim = '\\'      # for window
        if os.name == 'posix':
            self.path_delim = '/'   # for linux

    def clean_activity(self):
        pass

    def create_icons(self):
        self.icons = {}
        self.icons['disk'] = self.create_sprite(
            'assets/filesystem/ic_disk.png')
        self.icons['folder'] = self.create_sprite(
            'assets/filesystem/ic_folder.png')
        self.icons['file'] = self.create_sprite(
            'assets/filesystem/ic_file.png')
        self.icons['file_img'] = self.create_sprite(
            'assets/filesystem/ic_file_img.png')
        self.icons['file_pdf'] = self.create_sprite(
            'assets/filesystem/ic_file_pdf.png')

    def create_sprite(self, path):
        image = Image.open(path)
        image.mode = 'RGBA'
        return ImageTk.PhotoImage(image)

    def create_widgets(self):
        # Create top left padding for the frame
        self.spacer = tk.Label(self, bg=THEMECOLOR.body_bg,
                               highlightthickness=0, height=2, width=12, anchor=tk.E)
        self.spacer.grid(row=0, column=0)
        # Define these scrollbar before hand
        self.scb_vertical = tk.Scrollbar(self,)
        self.scb_vertical.grid(row=1, column=2, sticky=tk.N+tk.S, rowspan=5)
        # Display the file system tree
        self.tbl_container = ttk.Treeview(
            self, yscrollcommand=self.scb_vertical.set, show='tree headings', height=24)
        self.tbl_container.grid(
            row=1, column=1, sticky=tk.N+tk.S+tk.W+tk.E, padx=0, pady=0, rowspan=5)
        # Scrollbars config
        self.scb_vertical.config(command=self.tbl_container.yview)
        # Table config
        self.tbl_container.heading('#0', text='Folder', anchor='w')
        self.tbl_container.column('#0', width=600, stretch=True)
        self.tbl_container.bind('<Double-1>',
                                lambda e: self.on_double_click(e))
        self.tbl_container.bind('<ButtonRelease-1>',
                                lambda e: self.on_single_click(e))
        # Retrieve file from server
        self.btn_retrieve = tk.Button(
            self, text='Retrieve', command=self.retrieve_file, width=10, height=2)
        self.btn_retrieve.grid(row=1, column=3, sticky=tk.E, padx=10, pady=10)
        # Send file to server
        self.btn_send = tk.Button(
            self, text="Send", command=self.send_file, width=10, height=2)
        self.btn_send.grid(row=2, column=3, sticky=tk.E, padx=10, pady=10)
        # Delete file or folder
        self.btn_del = tk.Button(
            self, text="Delete", command=self.delete_file, width=10, height=2)
        self.btn_del.grid(row=3, column=3, sticky=tk.E, padx=10, pady=10)
        # Copy file in server
        self.btn_copy = tk.Button(
            self, text="Copy", command=self.copy_file, width=10, height=2)
        self.btn_copy.grid(row=4, column=3, sticky=tk.E, padx=10, pady=10)
        # Move file in server
        self.btn_move = tk.Button(
            self, text="Move", command=self.move_file, width=10, height=2)
        self.btn_move.grid(row=5, column=3, sticky=tk.E, padx=10, pady=10)

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
        print(cur_item)
        if '.' in dirs[-1]:
            # Handle if a file is in focus
            cur_item = '\\'.join(dirs[0:-1])
        path = cur_item + '\\' + filename
        self._socket.send('folder,copy,?,{}'.format(path))
        # Client send file by chunks
        self.send(filename=source)
        # Add that file to the treeview
        local_index = len(self.tbl_container.get_children(cur_item))
        self.tbl_container.insert(parent=cur_item, index=local_index, iid=path, text=filename,
                                  open=False, values=False, image=self.get_icon([filename, False]))

    def delete_file(self):
        cur_item = self.tbl_container.focus()
        self._socket.send('folder,del,{}'.format(cur_item))
        if self._socket._sock.recv(3).decode('utf8') == 'ok':
            self.tbl_container.delete(cur_item)

    def copy_file(self):
        if self.btn_copy.cget('text') == 'Copy':
            # Get src item
            self.src_item = self.tbl_container.focus()
            # Lock other btn, change copy to paste
            self.btn_retrieve.configure(state='disable')
            self.btn_send.configure(state='disable')
            self.btn_del.configure(state='disable')
            self.btn_copy.configure(text='Paste')
        else:
            # Get dst item
            self.dst_item = self.tbl_container.focus()
            # Send cmd to server
            self._socket.send('folder,copy,{},{}'.format(
                self.src_item, self.dst_item))
            # Response from server
            if self._socket._sock.recv(3).decode('utf8') == 'bad':
                # Copy not successful
                utils.messagebox(
                    'Filesystem', msg='Cannot copy', type='warn')
            else:
                # Get parent folder
                cur_item = self.dst_item
                dirs = cur_item.split('\\')
                path = None
                filename = self.src_item.split('\\')[-1]
                if '.' in dirs[-1]:
                    # Handle if a file is in focus
                    cur_item = '\\'.join(dirs[0:-1])
                path = cur_item + '\\' + filename
                # Add that file to the treeview
                local_index = len(self.tbl_container.get_children(cur_item))
                print(filename)
                self.tbl_container.insert(parent=cur_item, index=local_index, iid=path, text=filename,
                                          open=False, values=False, image=self.get_icon([filename, False]))
            # Enable other btn, change paste to copy
            self.btn_retrieve.configure(state='normal')
            self.btn_send.configure(state='normal')
            self.btn_del.configure(state='normal')
            self.btn_copy.configure(text='Copy')
            self.src_item = None

    def move_file(self):
        if self.btn_move.cget('text') == 'Move':
            # Get src item
            self.src_item = self.tbl_container.focus()
            # Lock other btn, change copy to paste
            self.btn_retrieve.configure(state='disable')
            self.btn_send.configure(state='disable')
            self.btn_del.configure(state='disable')
            self.btn_move.configure(text='Paste')
        else:
            # Get dst item
            self.dst_item = self.tbl_container.focus()
            # Send cmd to server
            self._socket.send('folder,move,{},{}'.format(
                self.src_item, self.dst_item))
            # Response from server
            if self._socket._sock.recv(3).decode('utf8') == 'bad':
                # Copy not successful
                utils.messagebox(
                    'Filesystem', msg='Cannot move', type='warn')
            else:
                # Get parent folder
                cur_item = self.dst_item
                dirs = cur_item.split('\\')
                path = None
                filename = self.src_item.split('\\')[-1]
                if '.' in dirs[-1]:
                    # Handle if a file is in focus
                    cur_item = '\\'.join(dirs[0:-1])
                path = cur_item + '\\' + filename
                # Add that file to the treeview
                local_index = len(self.tbl_container.get_children(cur_item))
                print(filename)
                self.tbl_container.delete(self.src_item)
                self.tbl_container.insert(parent=cur_item, index=local_index, iid=path, text=filename,
                                          open=False, values=False, image=self.get_icon([filename, False]))
            # Enable other btn, change paste to copy
            self.btn_retrieve.configure(state='normal')
            self.btn_send.configure(state='normal')
            self.btn_del.configure(state='normal')
            self.btn_move.configure(text='Move')
            self.src_item = None

    def next_id(self):
        id = Filesystem.id + 1
        return id

    def initial_fetch(self):
        result = self._socket.receive()
        disks = pickle.loads(result)
        for id, disk in enumerate(disks):
            this_id = disk[:-1]
            print(this_id)
            self.tbl_container.insert(parent='', index=id, iid=this_id+'\\', text=disk.replace(
                '\\', ''), open=False, values=True, image=self.icons['disk'])
        #self.expand_dir('\\', pickle.loads(result))

    def expand_dir(self, parent, subtree):
        local_id = 0
        for item in subtree:
            this_id = parent
            if parent != '\\':
                this_id += '\\'
            this_id += item[0]
            self.tbl_container.insert(parent=parent, index=local_id, iid=this_id,
                                      text=item[0], open=False, values=item[1], image=self.get_icon(item))
            local_id = local_id + 1

    def on_single_click(self, event):
        target = self.tbl_container.identify('item', event.x, event.y)
        if self.tbl_container.item(target)['values'][0] == 0:
            self.enable_btn('normal')
        else:
            self.enable_btn('disable')

    def on_double_click(self, event):
        # Get the clicked item
        target = self.tbl_container.identify('item', event.x, event.y)
        # Return if item is a file
        if self.tbl_container.item(target)['values'][0] == 0:
            return
        # Return if item is already expanded
        if len(self.tbl_container.get_children(target)) != 0:
            return
        # Send command to server
        self._socket.send('folder,view,' + target)
        result = self._socket.receive()
        if len(result) == 3:
            if result.decode('utf8') == 'bad':
                utils.messagebox(
                    'Filesystem', msg='Access denied', type='warn')
                return
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

    def get_icon(self, item):
        if item[1]:
            return self.icons['folder']
        ext = item[0].split('.')[-1]
        if ext in ['png', 'jpg', 'jpeg', 'bmp', 'gif']:
            return self.icons['file_img']
        if ext == 'pdf':
            return self.icons['file_pdf']
        return self.icons['file']

    def enable_btn(self, state):
        self.btn_retrieve.configure(state=state)
        self.btn_send.configure(state=state)
        self.btn_del.configure(state=state)
        if self.src_item == None:
            # if btn is in copy mode
            self.btn_copy.configure(state=state)
