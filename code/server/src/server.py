import os
import sys
import socket
import tkinter as tk
from threading import Thread, Event
from src.screenshot import Screenshot
from src.process import Process
from src.application import Application
from src.keystroke import KeyLogger
from src.registry import Registry

class Server:
    def __init__(self):
        super().__init__()
        self._root = tk.Tk()
        self._root.geometry('400x200')
        self._root.title("Server")
        self._root.btn_open_server = tk.Button(self._root, text = "OPEN SERVER", bg = "#5DADE2", height = 2, width = 15, anchor = tk.CENTER,
                                        font = ("Consolas 25 bold"), command = self.open_close_server)
        self._root.btn_open_server.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)
        # self._root.bind("<Destroy>", self.on_exit)
        self.server = None


    def run(self):
        self._root.mainloop()

    def open_close_server(self):
        if (self._root.btn_open_server["text"] == "OPEN SERVER"):
            IP = (socket.gethostbyname('localhost'), 54321)
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(IP) # only one server socket for all connect
            self.server.listen(1)

            self._root.btn_open_server.configure(text = "SERVER IS\nOPENING")
            self._root.btn_open_server.configure(bg = "#79fa00")

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
            cmd = self.client.recv(32).decode('utf8')
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
            elif cmd == 'quit':
                break
                
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
        os.popen("shutdown -s")
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

    pass