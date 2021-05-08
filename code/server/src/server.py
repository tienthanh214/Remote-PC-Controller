import os
import socket
import tkinter as tk
import time
from threading import Thread
from src.screenshot import Screenshot
from src.process import Process
from src.application import Application
from src.keystroke import KeyLogger
from src.registry import Registry


class Server:
    def __init__(self):
        super().__init__()
        # Private attributes
        self.server = None
        self.client = None
        # Initialize UI
        self._root = tk.Tk()
        self._root.title("Server")
        self._root.geometry("400x210")
        self._root.resizable(False, False)
        self._root.btn_open_server = tk.Button(
            self._root, bg="#5DADE2", text="OPEN SERVER", font=("Consolas 30 bold"), padx=20, pady=20)

        self._root.btn_open_server.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self._root.btn_open_server.bind("<Button>", self.open_server)
        self._root.bind("<Destroy>", self.close_server)

    def run(self):
        self._root.mainloop()

    def open_server(self, event):
        IP = (socket.gethostbyname('localhost'), 54321)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(IP)
        self.server.listen(1)

        self.ACCEPT_THREAD = Thread(target=self.accept_connect)
        self.ACCEPT_THREAD.start()

    def close_server(self, event):
        try:
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            self.server.close()
        except:
            pass

    def accept_connect(self):
        self.client, addr = self.server.accept()
        print("Connected by", addr)
        Thread(target=self.handle_client).start()

    def handle_client(self):
        try:
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
        except:
            pass

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
