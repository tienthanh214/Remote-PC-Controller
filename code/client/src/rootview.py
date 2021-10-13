from src.frames.keystroke import Keystroke
from src.frames.manager import Manager
from src.frames.menu import Menu
from src.frames.registry import Registry
from src.frames.screenshot import Screenshot

from tkinter import constants
from src.mysocket import MySocket
import tkinter as tk
import pickle
import src.textstyles as textstyle
import src.themecolors as themecolor
import src.utils as utils
import time


DEFAULT_FRAME = 'Menu'


class RootView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Config window shape
        self.geometry("1280x840+50+50")
        self.title('Computer Network Project')
        self.resizable(False, False)
        self.grid()
        # Header
        self.head = tk.Frame(self, bg=themecolor.header_bg)
        self.head.pack(side="top", fill="both", expand=True)
        self.head.grid_rowconfigure(0, weight=1)
        self.head.grid_columnconfigure(1, weight=1)
        # Body
        self.body = tk.Frame(self, bg=themecolor.body_bg)
        self.body.pack(side="top", fill="both", expand=True)
        # Create widgets
        self.frame = None
        self.frames = {}
        self.create_header()
        self.create_frames()
        self.bind_actions()
        # Hold connecting IP address
        self.ip_addr = tk.StringVar()
        self.ip_addr.set('')

    def run(self):
        '''Run the UI loop and show the connect page'''
        self.show_frame(DEFAULT_FRAME)
        self.mainloop()

    def create_frames(self):
        '''Init instances of frames and store in a map'''
        for frame in (Keystroke, Manager, Menu, Registry, Screenshot):
            page_name = frame.__name__
            instance = frame(parent=self.body)
            instance.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = instance

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        socket = MySocket.getInstance()
        if socket._isconnected:
            socket._isconnected = socket.send(page_name.lower())

        if page_name == DEFAULT_FRAME:
            self.btn_back.grid_remove()
        else:
            self.btn_back.grid()

        self.title(page_name)
        self.frame = self.frames[page_name]
        self.frame.tkraise()

    def create_header(self):
        '''Init header element'''
        self.btn_back = tk.Button(
            self.head, text="<-", width=2, height=2, bg='#97c1a9', fg='#000000')
        self.btn_back.grid(row=0, column=0, sticky=tk.W,
                           pady=10, padx=10, columnspan=1, rowspan=2)

        self.lbl_app = tk.Label(
            self.head, text='PC Controller', height=1, font=textstyle.logo_font, bg="#f9cdad", fg="#ec2049")
        self.lbl_app.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10,
                          ipadx=10, ipady=10, columnspan=1, rowspan=2)

        # IP address label
        self.lbl_app = tk.Label(
            self.head, text='Enter IP address', height=1, font=textstyle.title_font, bg=themecolor.header_bg)
        self.lbl_app.grid(row=0, column=3, sticky=tk.S,
                          columnspan=1, rowspan=1)

        # Input text for target ip address
        self.etr_ip = tk.Entry(self.head, width=30)
        self.etr_ip.focus()
        self.etr_ip.grid(row=1, column=3, padx=10, pady=10,
                         ipady=4, sticky=tk.S, columnspan=1)

        # Connect button
        self.btn_connect = tk.Button(
            self.head, text="Connect", width=6, height=1, bg='#97c1a9', fg='#000000')
        self.btn_connect.grid(row=1, column=4, sticky=tk.N,
                              pady=10, padx=10)

    def bind_actions(self):
        self.bind("<Destroy>", lambda: self.exit_prog(isKilled=True))
        # self.bind("<Tab>", self.focus_next_widget)
        # self.bind("<Return>", lambda e: self.enterkey(e))
        self.btn_connect["command"] = self.connect
        self.btn_back["command"] = self.back
        self.frames[DEFAULT_FRAME].btn_process["command"] = lambda: self.show_frame(
            "Manager")
        self.frames[DEFAULT_FRAME].btn_app["command"] = lambda: self.show_frame(
            "Manager")
        self.frames[DEFAULT_FRAME].btn_shutdown["command"] = self.shutdown
        self.frames[DEFAULT_FRAME].btn_screenshot["command"] = lambda: self.show_frame(
            "Screenshot")
        self.frames[DEFAULT_FRAME].btn_keystroke["command"] = lambda: self.show_frame(
            "Keystroke")
        self.frames[DEFAULT_FRAME].btn_registry["command"] = lambda: self.show_frame(
            "Registry")
        self.frames[DEFAULT_FRAME].btn_quit["command"] = lambda: self.exit_prog(
            isKilled=False)

    def connect(self):
        ip = self.etr_ip.get().strip("\n")
        socket = MySocket.getInstance()

        if socket._isconnected:
            ans = tk.messagebox.askquestion(
                "New IP address", "Do you want to disconnect to the current server\n and reconnect to this IP ({})?".format(ip), icon="warning")
            if ans == "yes":
                try:
                    socket.send("quit")
                finally:
                    socket.close()
                    time.sleep(1)
            else:
                utils.messagebox("Client", "New connection cancelled", "error")
                return

        socket.connect(ip=ip)
        if socket._isconnected:
            utils.messagebox("Client", "Connected to the server", "info")
        else:
            utils.messagebox("Client", "Fail to connect to server", "error")

    def back(self):
        # Command to quit function
        self.exit_func(None)
        self.show_frame("Menu")
        exit

    def exit_prog(self, isKilled=True):
        socket = MySocket.getInstance()
        try:
            socket.send("quit", showerror=False)
        except OSError:
            pass
        finally:
            socket.close()
            if not isKilled:
                self.destroy()

    def exit_func(self, event):
        socket = MySocket.getInstance()
        socket.send("exit", showerror=False)

    def shutdown(self):
        socket = MySocket.getInstance()
        socket._isconnected = self._socket.send("shutdown")
        socket.shutdown()
