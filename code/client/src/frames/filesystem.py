from threading import Thread
from tkinter.constants import HORIZONTAL, VERTICAL
from typing import Counter
from src.mysocket import MySocket
from tkinter import Text, ttk, filedialog
from PIL import Image, ImageTk
import tkinter as tk
import src.utils as utils
import src.textstyles as textstyle
import src.themecolors as THEMECOLOR
import src.utils as util
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
        self.icons['download'] = self.create_sprite(
            'assets/filesystem/ic_download.png')
        self.icons['send'] = self.create_sprite(
            'assets/filesystem/ic_send.png')
        self.icons['delete'] = self.create_sprite(
            'assets/filesystem/ic_delete.png')
        self.icons['copy'] = self.create_sprite(
            'assets/filesystem/ic_copy.png')
        self.icons['move'] = self.create_sprite(
            'assets/filesystem/ic_move.png')
        self.icons['paste'] = self.create_sprite(
            'assets/filesystem/ic_paste.png')
        self.icons['cancel'] = self.create_sprite(
            'assets/filesystem/ic_cancel.png')

    def create_sprite(self, path):
        image = Image.open(path)
        image.mode = 'RGBA'
        return ImageTk.PhotoImage(image)

    def create_widgets(self):

        self.vertical_pane = ttk.PanedWindow(self, orient=VERTICAL, height=720)
        self.vertical_pane.grid(row=0, column=0, sticky="nsew")
        self.horizontal_pane = ttk.PanedWindow(
            self.vertical_pane, orient=HORIZONTAL, width=1024)
        self.vertical_pane.add(self.horizontal_pane)
        self.button_frame = ttk.Labelframe(
            self.horizontal_pane, text="My Button")
        self.button_frame.columnconfigure(0, weight=1)
        self.horizontal_pane.add(self.button_frame, weight=1)
        self.console_frame = ttk.Labelframe(
            self.horizontal_pane, text="Console")
        self.console_frame.columnconfigure(1, weight=6)
        self.console_frame.rowconfigure(0, weight=1)
        self.horizontal_pane.add(self.console_frame, weight=1)

        # Define these scrollbar before hand
        self.scb_vertical = tk.Scrollbar(self.console_frame, orient=tk.VERTICAL)
        self.scb_vertical.grid(
            row=0, column=1, sticky=tk.W+tk.N+tk.S, rowspan=5)
        self.scb_horizontal = tk.Scrollbar(self.console_frame, orient=tk.HORIZONTAL)
        self.scb_horizontal.grid(
            row=5, column=0, sticky=tk.E+tk.W, columnspan=1)
        
        # Display the file system tree
        self.trv_dirlist = ttk.Treeview(
            self.console_frame, yscrollcommand=self.scb_vertical.set, xscrollcommand=self.scb_horizontal.set, show='tree headings', height=24)
        self.trv_dirlist.grid(
            row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E, padx=0, pady=0, rowspan=5)

        # Scrollbars config
        self.scb_vertical.config(command=self.trv_dirlist.yview)
        self.scb_horizontal.config(command=self.trv_dirlist.xview)

        # Table config
        self.trv_dirlist.heading('#0', text='Folder', anchor='w')
        self.trv_dirlist.column('#0', width=700, stretch=True)
        self.trv_dirlist.bind('<Double-1>',
                              lambda e: self.on_double_click(e))
        self.trv_dirlist.bind('<ButtonRelease-1>',
                              lambda e: self.on_single_click(e))
        # Show source file
        self.lbl_srcdir = tk.Label(
            self.console_frame, text='', bg=THEMECOLOR.body_bg, fg='white', width=60)
        self.lbl_srcdir.grid(row=6, column=0, sticky=tk.W +
                             tk.S+tk.E+tk.N, padx=1, pady=1, columnspan=1)

        # Retrieve file from server
        self.btn_download = tk.Button(
            self.button_frame, text='Download', image=self.icons['download'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="white", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.retrieve_file)
        self.btn_download.grid(row=0, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                               padx=30, pady=15, rowspan=2)
        self.btn_download.config(width=20, height=40)

        # Send file to server
        self.btn_send = tk.Button(
            self.button_frame, text='Send', image=self.icons['send'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="white", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.send_file)
        self.btn_send.grid(row=2, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                           padx=30, pady=15, rowspan=2)
        self.btn_send.config(width=20, height=40)

        # Delete file or folder
        self.btn_del = tk.Button(
            self.button_frame, text='Delete', image=self.icons['delete'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="white", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.delete_file)
        self.btn_del.grid(row=4, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                          padx=30, pady=15, rowspan=2)
        self.btn_del.config(width=20, height=40)

        # Copy file in server
        self.btn_copy = tk.Button(
            self.button_frame, text='Copy', image=self.icons['copy'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="white", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.copy_file)
        self.btn_copy.grid(row=6, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                           padx=30, pady=15, rowspan=2)
        self.btn_copy.config(width=20, height=40)

        # Move file in server
        self.btn_move = tk.Button(
            self.button_frame, text='Move', image=self.icons['move'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="white", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.move_file)
        self.btn_move.grid(row=8, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                           padx=30, pady=15, rowspan=2)
        self.btn_move.config(width=20, height=40)

        # Cancel process
        self.btn_cancel = tk.Button(
            self.button_frame, text='Cancel', image=self.icons['cancel'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="#d22b2b", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.cancel_action)
        self.btn_cancel.grid(row=10, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                             padx=30, pady=15, rowspan=2)
        self.btn_cancel.config(width=20, height=40)
        self.btn_cancel.grid_remove()

    def retrieve_file(self):
        # Get id of the source
        cur_item = self.trv_dirlist.focus()
        # Get the file from client
        destination = filedialog.askdirectory(title='Save to this location')
        if len(destination) == 0:
            return
        # Send command to server
        self._socket.send('folder,copy,{},?'.format(cur_item))
        # Retrieve the file from server
        filename = cur_item.split('\\')[-1]
        # self.receive(filename=destination + self.path_delim + filename)
        Thread(target = self.receive, args = (destination + self.path_delim + filename,), daemon = True).start()

    def send_file(self):
        # Get the file from client
        source = filedialog.askopenfilename(
            title="Send this file to server", filetypes=[("all files", "*.*")])
        if len(source) == 0:
            return
        # Send command to server
        cur_item = self.trv_dirlist.focus()
        dirs = cur_item.split('\\')
        path = None
        filename = os.path.basename(source)
        print(cur_item)
        if '.' in dirs[-1]:
            # Handle if a file is in focus
            cur_item = '\\'.join(dirs[0:-1])
        path = cur_item + '\\' + filename
        self._socket.send('folder,copy,?,{}'.format(path))
        # Client send file by chunks
        # self.send(filename=source)
        Thread(target = self.send, args = (source, ), daemon = True).start()
        # Add that file to the treeview
        local_index = len(self.trv_dirlist.get_children(cur_item))
        self.trv_dirlist.insert(parent=cur_item, index=local_index, iid=path, text=filename,
                                open=False, values=False, image=self.get_icon([filename, False]))

    def delete_file(self):
        selected_items = self.trv_dirlist.selection()
        for cur_item in selected_items:
            self._socket.send('folder,del,{}'.format(cur_item))
            if self._socket._sock.recv(3).decode('utf8') == 'ok':
                self.trv_dirlist.delete(cur_item)

    def copy_file(self):
        if self.btn_copy.cget('text') == 'Copy':
            # Get src item
            self.src_item = self.trv_dirlist.focus()
            self.lbl_srcdir.configure(text=self.src_item)
            # Lock other btn, change copy to paste
            self.btn_download.configure(state='disable')
            self.btn_send.configure(state='disable')
            self.btn_del.configure(state='disable')
            self.btn_copy.configure(text='Paste', image=self.icons['paste'])
            self.btn_move.configure(state='disable')
            self.clear_selection()
            # Show cancel btn
            self.btn_cancel.grid(row=8, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                                 padx=30, pady=15, rowspan=2)
            self.btn_move.grid(row=10, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                               padx=30, pady=15, rowspan=2)
        else:
            # Get dst item
            self.dst_item = self.trv_dirlist.selection()
            for cur_item in self.dst_item:
                # Send cmd to server
                self._socket.send('folder,copy,{},{}'.format(
                    self.src_item, cur_item))
                # Response from server
                if self._socket._sock.recv(3).decode('utf8') == 'bad':
                    # Copy not successful
                    utils.messagebox(
                        'Filesystem', msg='Cannot copy', type='warn')
                else:
                    # Get parent folder
                    dirs = cur_item.split('\\')
                    path = None
                    filename = os.path.basename(self.src_item)
                    if '.' in dirs[-1]:
                        # Handle if a file is in focus
                        cur_item = '\\'.join(dirs[0:-1])
                    path = cur_item + '\\' + filename
                    # Add that file to the treeview
                    local_index = len(
                        self.trv_dirlist.get_children(cur_item))
                    print(filename)
                    self.trv_dirlist.insert(parent=cur_item, index=local_index, iid=path, text=filename,
                                            open=False, values=False, image=self.get_icon([filename, False]))
            # Enable other btn, change paste to copy
            self.btn_download.configure(state='normal')
            self.btn_send.configure(state='normal')
            self.btn_del.configure(state='normal')
            self.btn_copy.configure(text='Copy', image=self.icons['copy'])
            self.btn_move.configure(state='normal')
            # Hide cancel btn
            self.btn_move.grid(row=8, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                               padx=30, pady=15, rowspan=2)
            self.btn_cancel.grid_remove()
            self.src_item = None
            self.lbl_srcdir.configure(text='')

    def move_file(self):
        if self.btn_move.cget('text') == 'Move':
            # Get src item
            self.src_item = self.trv_dirlist.focus()
            self.lbl_srcdir.configure(text=self.src_item)
            # Lock other btn, change copy to paste
            self.btn_download.configure(state='disable')
            self.btn_send.configure(state='disable')
            self.btn_del.configure(state='disable')
            self.btn_copy.configure(state='disable')
            self.btn_move.configure(text='Paste', image=self.icons['paste'])
            self.clear_selection()
            # Show cancel btn
            self.btn_move.grid(row=8, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                               padx=30, pady=15, rowspan=2)
            self.btn_cancel.grid(row=10, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                                 padx=30, pady=15, rowspan=2)
        else:
            # Get dst item
            self.dst_item = self.trv_dirlist.selection()
            for cur_item in self.dst_item:
                # Send cmd to server
                self._socket.send('folder,move,{},{}'.format(
                    self.src_item, cur_item))
                # Response from server
                if self._socket._sock.recv(3).decode('utf8') == 'bad':
                    # Copy not successful
                    utils.messagebox(
                        'Filesystem', msg='Cannot move', type='warn')
                else:
                    # Get parent folder
                    dirs = cur_item.split('\\')
                    path = None
                    filename = os.path.basename(self.src_item)
                    if '.' in dirs[-1]:
                        # Handle if a file is in focus
                        cur_item = '\\'.join(dirs[0:-1])
                    path = cur_item + '\\' + filename
                    # Add that file to the treeview
                    local_index = len(
                        self.trv_dirlist.get_children(cur_item))
                    print(filename)
                    self.trv_dirlist.delete(self.src_item)
                    self.trv_dirlist.insert(parent=cur_item, index=local_index, iid=path, text=filename,
                                            open=False, values=False, image=self.get_icon([filename, False]))
            # Enable other btn, change paste to copy
            self.btn_download.configure(state='normal')
            self.btn_send.configure(state='normal')
            self.btn_del.configure(state='normal')
            self.btn_copy.configure(state='normal')
            self.btn_move.configure(text='Move', image=self.icons['move'])
            # Hide cancel btn
            self.btn_cancel.grid_remove()
            self.src_item = None
            self.lbl_srcdir.configure(text='')

    def cancel_action(self):
        self.dst_item = None
        self.src_item = None
        self.lbl_srcdir.configure(text='')
        self.clear_selection()
        # Reset button
        self.enable_btn('normal')
        self.btn_copy.configure(text='Copy', image=self.icons['copy'])
        self.btn_move.configure(text='Move', image=self.icons['move'])
        self.btn_cancel.grid_remove()

    def next_id(self):
        id = Filesystem.id + 1
        return id

    def initial_fetch(self):
        result = self._socket.receive()
        disks = pickle.loads(result)
        for id, disk in enumerate(disks):
            this_id = disk[:-1]
            print(this_id)
            self.trv_dirlist.insert(parent='', index=id, iid=this_id+'\\', text=disk.replace(
                '\\', ''), open=False, values=True, image=self.icons['disk'])

    def expand_dir(self, parent, subtree):
        local_id = 0
        for item in subtree:
            this_id = parent
            if parent != '\\':
                this_id += '\\'
            this_id += item[0]
            self.trv_dirlist.insert(parent=parent, index=local_id, iid=this_id,
                                    text=item[0], open=False, values=item[1], image=self.get_icon(item))
            local_id = local_id + 1

    def on_single_click(self, event):
        target = self.trv_dirlist.identify('item', event.x, event.y)
        if self.trv_dirlist.item(target)['values'][0] == 0:
            self.enable_btn('normal')
            self.btn_send.configure(state='disable')
        else:
            self.enable_btn('disable')
            self.btn_send.configure(state='normal')

    def on_double_click(self, event):
        # Get the clicked item
        target = self.trv_dirlist.identify('item', event.x, event.y)
        # Return if item is a file
        if self.trv_dirlist.item(target)['values'][0] == 0:
            return
        # Return if item is already expanded
        if len(self.trv_dirlist.get_children(target)) != 0:
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
        self._progressbar = util.ProgressBar(tk.Toplevel(
            self), title='Loading...', mode='determinate', max_length=500)
        raw_msglen = self._socket._sock.recv(4)
        if not raw_msglen:
            return None
        msglen = stc.unpack('>I', raw_msglen)[0]
        # only update progressBar for 60 times
        log_interval = ((4096 * 2 + msglen - 1) // (4096 * 2)) // 60
        if log_interval == 0: log_interval = 1
        num_step = 0
        f = open(filename, "wb")
        curlen = 0
        while curlen < msglen:
            packet = self._socket.receive()
            if not packet:
                break
            f.write(packet)
            curlen += len(packet)
            # Update progressbar
            if num_step % log_interval == 0:
                pass
                self._progressbar.update(curlen * 100 / msglen)
                self.update_idletasks()
            num_step += 1
            # use curlen/msglen to show progress bar
        f.close()
        self._progressbar.killbox()
        self._progressbar = None

    def send(self, filename):
        try:
            f = open(filename, "rb")
        except:
            print("file not found")
            return
        self._progressbar = util.ProgressBar(tk.Toplevel(
            self), title='Loading...', mode='determinate', max_length=500)
        filesize = os.path.getsize(filename)
        self._socket._sock.sendall(stc.pack('>I', filesize))
        prog = 0
        num_step = 0
        # only update progressBar for 60 times
        log_interval = ((4096 * 2 + filesize - 1) // (4096 * 2)) // 60
        if log_interval == 0: log_interval = 1
        print(log_interval)
        
        while True:
            bytes_read = f.read(4096 * 2)
            if not bytes_read:
                break
            self._socket._sock.sendall(bytes_read)
            prog += len(bytes_read)
            # Update progressbar
            
            if num_step % log_interval == 0:
                self._progressbar.update(prog * 100 / filesize)
                self.update_idletasks()
            num_step += 1

            # use prog/filesize to show progress bar
        f.close()
        self._progressbar.killbox()
        self._progressbar = None

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
        self.btn_download.configure(state=state)
        # self.btn_send.configure(state=state)
        # self.btn_del.configure(state=state)
        if self.src_item == None:
            # if btn is in copy mode
            self.btn_copy.configure(state=state)
            self.btn_move.configure(state=state)

    def clear_selection(self):
        for item in self.trv_dirlist.selection():
            self.trv_dirlist.selection_remove(item)
