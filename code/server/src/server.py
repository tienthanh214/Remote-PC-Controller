import os
import socket
import tkinter as tk
from uuid import getnode as get_mac
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
        self.IP = (socket.gethostbyname(socket.gethostname()), 54321)
        # Initialize UI
        self._root = tk.Tk()
        self._root.geometry('450x200')
        self._root.title("Server")

        self._root.btn_open_server = tk.Button(self._root, text = "OPEN SERVER", bg = "#5DADE2", 
                                            height = 2, width = 15, anchor = tk.CENTER, 
                                            font = ("Consolas 25 bold"), command = self.open_close_server)
        self._root.btn_open_server.place(relx = 0.5, rely = 0.55, anchor = tk.CENTER)

        self._root.lbl_server_address = tk.Label(self._root, text = "IP: " + str(self.IP[0]), width = 25,
                                            font = ("Consolas 20 bold"), fg = "#ff0000")
        self._root.lbl_server_address.place(relx = 0.5, rely = 0.15, anchor = tk.CENTER)

        # self._root.bind("<Destroy>", self.on_exit)

    def run(self):
        self._root.mainloop()

    def open_close_server(self):
        if (self._root.btn_open_server["text"] == "OPEN SERVER"):
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.IP) # only one server socket for all connect
            self.server.listen(1)
            print('SERVER address:', self.IP)

            self._root.btn_open_server.configure(text = "SERVER IS\nOPENING")
            self._root.btn_open_server.configure(bg = "#00ff00")

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
            elif cmd == 'logoff':
                self.logoff()
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
    
    """------------- new features -----------"""

    def logoff(self):
        os.popen("shutdown -l")
        pass
    
    def get_MAC_address(self):
        mac = []
        for bit in range(0, 8 * 6, 8):
            mac.append('{:02x}'.format((get_mac() >> bit) & 0xff))
        mac = ':'.join(mac[::-1])
        self.client.sendall(bytes(mac))
        pass

    pass
