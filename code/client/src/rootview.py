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


ACT_PROCESS = 'process'
ACT_APPLICATION = 'application'
ACT_KEYSTROKE = 'keystroke'
ACT_SHUTDOWN = 'process'
ACT_REGISTRY = 'registry'
ACT_SCREENSHOT = 'screenshot'
ACT_QUIT = 'quit'


class RootView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.socket = MySocket.getInstance()
        # Config window shape
        self.geometry("1280x840+50+50")
        self.title('Computer Network Project')
        self.resizable(False, False)
        self.grid()
        # Header
        self.head = tk.Frame(self, bg=themecolor.header_bg)
        self.head.pack(side="top", fill="both", expand=False)
        self.head.grid_rowconfigure(0, weight=1)
        self.head.grid_columnconfigure(1, weight=1)
        # Body
        self.body = tk.Frame(self, bg=themecolor.body_bg)
        self.body.pack(side="top", fill="both", expand=True)
        # Create widgets
        self.menu = None
        self.activity = None
        self.create_header()
        self.create_menu()
        self.bind_actions()

    def run(self):
        '''Run the UI loop and show the connect page'''
        self.menu.tkraise()
        self.mainloop()

    def create_menu(self):
        instance = Menu(parent=self.body)
        instance.grid(row=0, column=0, sticky="nsew")
        self.menu = instance
        self.btn_back.grid_remove()

    def create_activity(self, activity_name):
        '''Show a frame for the given page name'''
        if self.socket._isconnected:
            self.socket._isconnected = self.socket.send(activity_name.lower())
        else:
            utils.messagebox("Client", "Not connected to a PC", "error")
            return
        # Show return button only in activity
        self.btn_back.grid()
        # Create activity screen
        self.title(activity_name)
        if activity_name == ACT_KEYSTROKE:
            self.activity = Keystroke(parent=self.body)
        elif activity_name == ACT_PROCESS:
            self.activity = Manager(parent=self.body, type='process')
        elif activity_name == ACT_APPLICATION:
            self.activity = Manager(parent=self.body, type='application')
        elif activity_name == ACT_SCREENSHOT:
            self.activity = Screenshot(parent=self.body)
        elif activity_name == ACT_REGISTRY:
            self.activity = Registry(parent=self.body)
        # Display that activity
        self.activity.grid(row=0, column=0, sticky="nsew")
        self.activity.tkraise()

    def create_header(self):
        '''Init header element'''
        self.btn_back = tk.Button(
            self.head, text="Back", width=2, height=2, bg='#97c1a9', fg='#000000')
        self.btn_back.grid(row=0, column=0, sticky=tk.W,
                           pady=10, padx=10, columnspan=1, rowspan=2)
        # Application logo
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
        self.bind("<Destroy>", lambda e: self.exit_prog(isKilled=True))
        # self.bind("<Tab>", self.focus_next_widget)
        # self.bind("<Return>", lambda e: self.enterkey(e))
        self.btn_connect["command"] = self.connect
        self.btn_back["command"] = self.back_to_menu
        self.menu.btn_process["command"] = lambda: self.create_activity(
            "process")
        self.menu.btn_app["command"] = lambda: self.create_activity(
            "application")
        self.menu.btn_shutdown["command"] = self.shutdown
        self.menu.btn_screenshot["command"] = lambda: self.create_activity(
            "screenshot")
        self.menu.btn_keystroke["command"] = lambda: self.create_activity(
            "keystroke")
        self.menu.btn_registry["command"] = lambda: self.create_activity(
            "registry")
        self.menu.btn_quit["command"] = lambda: self.exit_prog(isKilled=False)

    def connect(self):
        ip = self.etr_ip.get().strip("\n")
        if self.socket._isconnected:
            ans = tk.messagebox.askquestion(
                "New IP address", "Do you want to disconnect to the current server\n and reconnect to this IP ({})?".format(ip), icon="warning")
            if ans == "yes":
                try:
                    self.socket.send("quit")
                finally:
                    self.socket.close()
                    time.sleep(1)
            else:
                utils.messagebox("Client", "New connection cancelled", "error")
                return

        self.socket.connect(ip=ip)
        if self.socket._isconnected:
            utils.messagebox("Client", "Connected to the server", "info")
        else:
            utils.messagebox("Client", "Fail to connect to server", "error")

    def back_to_menu(self):
        # Command to quit function
        self.exit_func(None)
        self.menu.tkraise()
        self.title('Computer Network Project')
        self.btn_back.grid_remove()
        exit

    def exit_prog(self, isKilled=True):
        try:
            self.socket.send("quit", showerror=False)
        except OSError:
            pass
        finally:
            self.socket.close()
            if not isKilled:
                self.destroy()

    def exit_func(self, event):
        self.socket.send("exit", showerror=False)
        self.activity.destroy()

    def shutdown(self):
        self.socket._isconnected = self.socket.send("shutdown")
        self.socket.shutdown()
