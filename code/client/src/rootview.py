from os import access
from src.frames.keystroke import Keystroke
from src.frames.manager import Manager
from src.frames.menu import Menu
from src.frames.registry import Registry
from src.frames.screenshot import Screenshot
from src.frames.filesystem import Filesystem

from PIL import Image, ImageTk
from src.mysocket import MySocket
import tkinter as tk
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
ACT_FILESYSTEM = 'folder'
ACT_QUIT = 'quit'


class RootView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.socket = MySocket.getInstance()
        # Config window shape
        self.geometry("1024x720")
        self.resizable(0, 0)
        self.title('Computer Network Project')
        self.config(bg=themecolor.root_bg_red)
        self.grid()
        # Header
        self.head = tk.Frame(self, bg=themecolor.header_bg)
        self.head.pack(side="top", fill="both", expand=False, padx=10, pady=10)
        #self.head.grid_rowconfigure(0, weight=1)
        self.head.grid_columnconfigure(1, weight=1)
        # Body
        self.body = tk.Frame(self, bg=themecolor.body_bg)
        self.body.pack(side="top", fill="both", expand=True)
        # Object holders
        self.menu = None
        self.activity = None
        # Create widgets
        self.create_icons()
        self.create_header()
        self.create_menu()
        self.bind_actions()

    def run(self):
        '''Run the UI loop and show the connect page'''
        self.menu.tkraise()
        self.mainloop()

    def create_icons(self):
        self.icons = {}
        self.icons['icon'] = self.create_sprite('assets/ic_app_icon.png')
        self.icons['back'] = self.create_sprite('assets/ic_back.png')

    def create_sprite(self, path):
        image = Image.open(path)
        image.mode = 'RGBA'
        return ImageTk.PhotoImage(image)

    def create_menu(self):
        instance = Menu(parent=self.body)
        instance.grid(row=0, column=0, sticky="nsew")
        self.menu = instance
        self.btn_back.grid_remove()

    def create_activity(self, activity_name):
        '''Show a frame for the given page name'''
        if self.socket._isconnected:
            self.socket._isconnected = self.socket.send_immediate(
                activity_name.lower())
        else:
            utils.messagebox("Client", "Please connect to a PC", "warn")
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
        elif activity_name == ACT_FILESYSTEM:
            self.activity = Filesystem(parent=self.body)
        # Display that activity
        self.activity.grid(row=0, column=0, sticky="nsew")
        self.activity.tkraise()

    def create_header(self):
        '''Init header element'''
        self.btn_back = tk.Button(
            self.head, image=self.icons['back'], width=50, height=50, bg=themecolor.back_btn)
        self.btn_back.grid(row=0, column=0, sticky=tk.W+tk.E,
                           pady=10, padx=10, columnspan=1, rowspan=2)
        # Application logo
        self.lbl_app = tk.Canvas(
            self.head, width=300, height=80, bg=themecolor.header_bg, highlightthickness=0)
        self.lbl_app.grid(row=0, column=1, sticky=tk.W, padx=10,
                          pady=10, ipadx=10, ipady=10, columnspan=1, rowspan=2)
        self.lbl_app.create_image(130, 50, image=self.icons['icon'])
        # IP address label
        self.lbl_app = tk.Label(
            self.head, text='Enter IP address', height=1, font=textstyle.btn_font, bg=themecolor.header_bg)
        self.lbl_app.grid(row=0, column=3, sticky=tk.S,
                          columnspan=1, rowspan=1)
        # Input text for target ip address
        self.etr_ip = tk.Entry(self.head, width=30)
        self.etr_ip.focus()
        self.etr_ip.grid(row=1, column=3, padx=0, pady=10,
                         ipady=4, sticky=tk.N, columnspan=1)
        # Connect button
        self.btn_connect = tk.Button(
            self.head, text="Connect", width=12, height=1, bg=themecolor.connect_btn, fg='#000000')
        self.btn_connect.grid(row=1, column=4, sticky=tk.N,
                              pady=10, padx=0)
        # # Padding right
        self.spacer = tk.Label(self.head, height=2, width=2,
                               anchor=tk.E, bg=themecolor.header_bg)
        self.spacer.grid(row=0, column=5)

    def bind_actions(self):
        # self.bind("<Destroy>", lambda e: self.exit_prog(isKilled=True))
        # self.bind("<Tab>", self.focus_next_widget)
        # self.bind("<Return>", lambda e: self.enterkey(e))
        self.btn_connect["command"] = self.connect
        self.btn_back["command"] = self.back_to_menu
        self.menu.btn_process["command"] = lambda: self.create_activity(
            "process")
        self.menu.btn_app["command"] = lambda: self.create_activity(
            "application")
        self.menu.btn_shutdown["command"] = self.shutdown
        self.menu.btn_logout["command"] = self.logout
        self.menu.btn_info["command"] = self.get_info
        self.menu.btn_screen["command"] = lambda: self.create_activity(
            "screenshot")
        self.menu.btn_keyboard["command"] = lambda: self.create_activity(
            "keystroke")
        self.menu.btn_registry["command"] = lambda: self.create_activity(
            "registry")
        self.menu.btn_filesys["command"] = lambda: self.create_activity(
            "folder")
        self.menu.btn_quit["command"] = lambda: self.exit_prog(isKilled=False)

    def connect(self):
        ip = self.etr_ip.get().strip("\n")
        self.socket.connect(ip=ip)
        if self.socket._isconnected:
            utils.messagebox("Client", "Connected to the server", "info")
            self.config(bg=themecolor.root_bg_lime)
            self.btn_connect.config(bg=themecolor.disconnect_btn)
            self.btn_connect.config(text='Disconnect')
            self.btn_connect["command"] = self.disconnect
            self.etr_ip.configure(state="disable")

    def disconnect(self):
        if self.socket._isconnected:
            ans = tk.messagebox.askquestion(
                "Disconnect", "Do you want to disconnect to the current PC?", icon="warning")
            if ans == "yes":
                try:
                    self.socket.send_immediate("quit")
                finally:
                    self.socket.close()
                    time.sleep(0.5)
                    self.config(bg=themecolor.root_bg_red)
                    self.btn_connect.config(bg=themecolor.connect_btn)
                    self.btn_connect.config(text='Connect')
                    self.btn_connect["command"] = self.connect
                    self.etr_ip.configure(state="normal")
                    self.back_to_menu()
            else:
                return

    def back_to_menu(self):
        # Command to quit function
        self.exit_func()
        self.menu.tkraise()
        self.title('Computer Network Project')
        self.btn_back.grid_remove()
        exit

    def exit_prog(self, isKilled=True):
        try:
            self.socket.send_immediate("quit")
        except OSError:
            pass
        finally:
            self.socket.close()
            if not isKilled:
                self.destroy()

    def exit_func(self):
        self.activity.clean_activity()
        self.activity.destroy()
        self.socket.send_immediate("exit")

    def shutdown(self):
        self.socket._isconnected = self.socket.send_immediate("shutdown")
        self.socket.shutdown()

    def logout(self):
        self.socket._isconnected = self.socket.send_immediate("logoff")
        self.socket.shutdown()

    def get_info(self):
        self.socket._isconnected = self.socket.send_immediate("mac")
        data = self.socket._sock.recv(17).decode('utf8')
        utils.messagebox('MAC address', msg=data, type='info')
