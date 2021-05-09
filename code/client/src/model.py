import socket as sk
import time
import sys
import src.views.utilities as utl

# Text-based ommands are sent to the server
# The server than perform operation with window API accordingly


class MySocket:
    def __init__(self):
        super().__init__()
        self._reset()
        self._currentip = 0

    def _reset(self):
        self._isconnected = False
        self._sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    def connect(self, ip, port=54321):
        self._isconnected = True
        try:
            self._currentip = ip
            address = (ip, port)
            self._sock.connect(address)
        except:
            self._reset()

    def send(self, command="exit", showerror=True):
        try:
            self._sock.sendall(bytes(command, "utf8"))
            print("> request: " + str(command))
            return True
        except:
            if showerror:
                utl.messagebox("Socket", "Not connected to server", "error")
            return False

    def receive(self, length = 2048):
        try:
            data = bytearray()
            while len(data) < length:
                packet = self._sock.recv(4096)
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
        self._sock.close()
        self._reset()

    def shutdown(self):
        # Shutdown one halves of the connection
        # Further sends are disallowed
        self._sock.shutdown(sk.SHUT_WR)
        self._reset()
