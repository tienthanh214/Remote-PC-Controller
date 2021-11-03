from tkinter.constants import HORIZONTAL, VERTICAL
from src.mysocket import MySocket
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk
import tkinter as tk
import src.utils as util
import src.themecolors as THEMECOLOR
import multiprocessing as mp
import time


class Manager(tk.Frame):
    def __init__(self, parent, type):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self.create_widgets()
        self._type = type
        self._socket = MySocket.getInstance()
        self._inputbox = None

    def clean_activity(self):
        pass

    def create_sprite(self, path):
        image = Image.open(path)
        image.mode = 'RGBA'
        return ImageTk.PhotoImage(image)

    def create_icons(self):
        self.icons = {}
        self.icons['kill'] = self.create_sprite('assets/manager/ic_kill.png')
        self.icons['refresh'] = self.create_sprite(
            'assets/manager/ic_refresh.png')
        self.icons['delete'] = self.create_sprite(
            'assets/manager/ic_delete.png')
        self.icons['start'] = self.create_sprite('assets/manager/ic_start.png')

    def create_widgets(self):

        self.create_icons()

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

        # Prompt the inputbox
        # User will input the application or process id they want to kill
        self.btn_kill = tk.Button(
            self.button_frame, text="Kill", image=self.icons['kill'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="white", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.kill)
        self.btn_kill.grid(row=0, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                           padx=30, pady=25, rowspan=2)
        self.btn_kill.config(width=20, height=40)

        # Refresh and show running process or application from the server
        self.btn__view = tk.Button(
            self.button_frame, text="Refresh", image=self.icons['refresh'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="white", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.view_async)
        self.btn__view.grid(row=2, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                            padx=30, pady=25, rowspan=2)
        self.btn__view.config(width=20, height=40)

        # Clear the running process or application table
        self.btn__clear = tk.Button(
            self.button_frame, text="Delete", image=self.icons['delete'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="white", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.clear)
        self.btn__clear.grid(row=4, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                             padx=30, pady=25, rowspan=2)
        self.btn__clear.config(width=20, height=40)

        # Similar to btn_kill, but this will take the name of the application and start it instead
        self.btn__start = tk.Button(
            self.button_frame, text="Start", image=self.icons['start'], compound=tk.LEFT, bg=THEMECOLOR.body_bg, fg="white", activebackground="black",
            activeforeground="darkgreen", borderwidth=2, cursor="hand2", command=self.start)
        self.btn__start.grid(row=6, column=0, sticky=tk.W+tk.S+tk.E+tk.N,
                             padx=30, pady=25, rowspan=2)
        self.btn__start.config(width=20, height=40)

        # Display info of running process or application from the server
        cols = ("Name", "ID", "Count thread")
        self.table = ttk.Treeview(
            self.console_frame, columns=cols, show="headings")
        self.table.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)

        for col in cols:
            self.table.heading(col, text=col)

        for i in range(20):
            self.table.insert("", "end", values=("?", "?", "?"))

    def view_async(self):
        self._progressbar = util.ProgressBar(tk.Toplevel(
            self), title='Loading...', mode='determinate', max_length=500)
        Thread(target=self.view, args=()).start()

    def exec_command_async(self, cmd, act):
        Thread(target=self.exec_command, args=(cmd, act)).start()

    def populate_data(self, data):
        # for testing data will be in 2d list
        self.clear()
        if (data):
            data = data.split('\n')[3:-3]  # bo dong title, bo 2 dong \n\n cuoi
            data.sort(key=lambda x: x[0].upper())  # sort de tim theo ten thoi

        num_line = 0
        log_interval = len(data) // 5 + 1 
        for current_process in data:
            (name_process, id_process, count_thread) = current_process.rsplit(maxsplit=2)
            self.table.insert("", "end", values=(
                name_process, id_process, count_thread))
            # update progress bar
            num_line += 1
            if num_line == log_interval:
                self._progressbar.concat(num_line * 20 / len(data))
                num_line = 0

    def clear(self):
        # clear data in the tabel before updating
        for rowid in self.table.get_children():
            self.table.delete(rowid)

    def kill(self):
        if self._inputbox != None:
            self.reset_inputbox()
            return

        self._inputbox = util.inputbox(
            tk.Toplevel(self), tl=self._type, cmd="kill")

        # binding...
        self._inputbox.btn_get["command"] = lambda: self.exec_command_async(
            cmd=self._type, act="kill")
        self._inputbox.bind(
            "<Destroy>", lambda e: self.reset_inputbox())
        self._inputbox.mainloop()

        exit

    def view(self):
        self._socket._isconnected = self._socket.send_immediate(
            self._type + ',view')

        if not self._socket._isconnected:
            return

        data = self._socket.receive(self._progressbar.update).decode("utf8")
        self.populate_data(data=data)

        self._progressbar.killbox()

    def start(self):
        if self._inputbox != None:
            self.reset_inputbox()
            return

        self._inputbox = util.inputbox(
            tk.Toplevel(self), tl=self._type, cmd="start")

        # binding...
        self._inputbox.btn_get["command"] = lambda: self.exec_command_async(
            cmd=self._type, act="start")
        self._inputbox.bind(
            "<Destroy>", lambda e: self.reset_inputbox())
        self._inputbox.mainloop()
        exit

    def exec_command(self, cmd, act):
        target = self._inputbox.getvalue()
        # Send command to the server
        self._socket._isconncted = self._socket.send_immediate(
            ','.join([cmd, act, target]))
        self._inputbox.clear()

        if not self._socket._isconnected:
            return

        # Get response from server
        response = self._socket._sock.recv(32).decode("utf8")
        util.messagebox(title=cmd, msg=response,
                        type="info" if response == "SUCCESS" else "error")
        self.reset_inputbox()

    def reset_inputbox(self):
        self._inputbox.killbox()
        self._inputbox = None
