import os
import socket
import tkinter as tk
import platform
import pickle
from uuid import getnode as get_mac
from threading import Thread
from src.folder import Folder
from src.serversocket import ServerSocket
from src.screenshot import Screenshot
from src.process import Process
from src.application import Application
from src.keystroke import KeyLogger
from src.registry import Registry
from PIL import Image, ImageTk
from tkinter import PhotoImage

class Server:
    def __init__(self):
        super().__init__()
        # Private attributes
        self.server = None
        self.client = None
        self.IP = (socket.gethostbyname(socket.gethostname()), 54321)
        # Initialize UI
        self._root = tk.Tk()
        self._root.geometry('450x250')
        self._root.title("Server")
        # self._root.config(bg = '#444e50')
        self.load_icon()

        self._root.btn_open_server = tk.Button(self._root, text = "OPEN SERVER", bg = "#5DADE2", 
                                            width = 200, anchor = tk.CENTER,
                                            font = ("Consolas 20 bold"), command = self.open_close_server,
                                            image = self.icons['open'], compound = tk.TOP)
        self._root.btn_open_server.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)
        
        self._root.lbl_server_address = tk.Label(self._root, text = "IP: " + str(self.IP[0]), width = 25,
                                            font = ("Consolas 20 bold"), fg = "#ff0000")
        self._root.lbl_server_address.place(relx = 0.5, rely = 0.10, anchor = tk.CENTER)

        # self._root.bind("<Destroy>", self.on_exit)

    def load_icon(self):
        self.icons = {}
        self.icons['open'] = self.create_sprite('assets\ic_open.png')
        self.icons['opening'] = self.create_sprite('assets\ic_opening.png')

    def create_sprite(self, path):
        image = Image.open(path)
        image.mode = 'RGBA'
        return ImageTk.PhotoImage(image)

    def run(self):
        self._root.mainloop()

    def open_close_server(self):
        if (self._root.btn_open_server["text"] == "OPEN SERVER"):
            self.server = ServerSocket.getInstance()
            self.server.bind(self.IP) # only one server socket for all connect
            self.server.listen(1)
            print('SERVER address:', self.IP)

            self._root.btn_open_server.configure(image = self.icons['opening'])
            self._root.btn_open_server.configure(text = "OPENING")
            self._root.btn_open_server.configure(bg = "#8eff4c")

            Thread(target = self.accept_connect, daemon = True).start()
        
            
    def accept_connect(self):
        while True:
            # self.client = None
            self.client, addr = self.server.accept()
            print("Connected by", addr)
            handle_client_thread = Thread(target = self.handle_client, daemon = True)
            handle_client_thread.start()


    def handle_client(self): 
        while True:
            try:
                cmd = self.client.recv(16).decode('utf8')
            except:
                break
            if cmd == 'keystroke':
                self.keystroke()
            elif cmd == 'shutdown':
                self.shutdown()
            elif cmd == 'registry':
                self.registry()
            elif cmd == 'screenshot':
                self.screenshot()
            elif cmd == 'process':
                self.process()
            elif cmd == 'application':
                self.application()
            elif cmd == 'mac':
                self.get_MAC_address()
            elif cmd == 'logoff':
                self.logoff()
            elif cmd == 'folder':
                self.folder()
            elif cmd == 'quit':
                break
                
        if self.client:
            KeyLogger.unhook_key()
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()

    def on_exit(self, event = None):
        if self.client:
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
        if self.server:
            self.server.close() 

    def keystroke(self):
        doit = KeyLogger(self.client)
        doit.run()
        pass
    
    def shutdown(self):
        os.popen("shutdown -s -t 10")
        pass

    def registry(self):
        doit = Registry(self.client)
        doit.run()
        pass

    def screenshot(self):
        doit = Screenshot(self.client)
        doit.run()
        pass

    def process(self):
        doit = Process(self.client)
        doit.run()
        pass

    def application(self):
        doit = Application(self.client)
        doit.run()
        pass
    
    """------------- new features -----------"""

    def logoff(self):
        os.popen("shutdown -l")
        pass
    
    def get_MAC_address(self):
        # get mac address
        mac = []
        for bit in range(0, 8 * 6, 8):
            mac.append('{:02x}'.format((get_mac() >> bit) & 0xff))
        mac = ':'.join(mac[::-1])
        uname = platform.uname()
        info =  'MAC address:\n    ' + mac + '\n\n' + \
                'System:\n    ' + uname.system + '\n\n' +\
                'Node:\n    ' + uname.node + '\n\n' + \
                'Version:\n    ' + uname.version + '\n\n' + \
                'Machine:\n    ' + uname.machine + '\n\n' + \
                'Processor:\n    ' + uname.processor;
        # get other info of system
        self.client.sendall(bytes(info, "utf8"))
        pass
    
    def folder(self):
        doit = Folder(self.client)
        doit.run()
        pass

    pass
