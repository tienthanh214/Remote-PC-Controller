import socket as sk
import time
import src.utils as utl
from socket import AF_INET, SOCK_STREAM


# Text-based ommands are sent to the server
# The server than perform operation with window API accordingly
# Singleton design

class MySocket:
    __instance = None

    @staticmethod
    def getInstance():
        if MySocket.__instance == None:
            MySocket()
        return MySocket.__instance

    def __init__(self):
        super().__init__()
        self._reset()
        self._currentip = 0

    def _reset(self):
        self._isconnected = False
        MySocket.__instance = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    def connect(self, ip, port=54321):
        self._isconnected = True
        try:
            self._currentip = ip
            address = (ip, port)
            MySocket.__instance.connect(address)
        except:
            self._reset()

    def send(self, command="exit", showerror=True):
        try:
            MySocket.__instance.sendall(bytes(command, "utf8"))
            return True
        except:
            if showerror:
                utl.messagebox("Socket", "Not connected to server", "error")
            return False

    def receive(self, length=2048):
        try:
            data = bytearray()
            while len(data) < length:
                packet = MySocket.__instance.recv(4096)
                if not packet:
                    break
                if not packet == None:
                    data.extend(packet)
            return data
        except OSError:
            utl.messagebox("Socket", "Failed to receive data", "error")
            pass

    def close(self):
        # Close the socket file descriptor
        # Both sends and receives are disallowed
        MySocket.__instance.close()
        self._reset()

    def shutdown(self):
        # Shutdown one halves of the connection
        # Further sends are disallowed
        MySocket.__instance.shutdown(sk.SHUT_WR)
        self._reset()
