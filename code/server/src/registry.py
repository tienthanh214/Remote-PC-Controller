import winreg
import os

class Registry:
    def __init__(self, sock = None):
        self.client = sock
        pass

    def run(self):
        while True:
            cmd = self.client.recv(512).decode('utf8')
            if cmd == "exit":
                return

    
    def update_file_reg(self):
        file_len = int(self.client.recv(64).decode("utf8"))
        
