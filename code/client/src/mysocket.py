from socket import AF_INET, SOCK_STREAM
import socket as sk
import struct as stc
import src.utils as utl


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
        MySocket.__instance = self

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
            utl.messagebox("Socket", "Failed to connect", "error")

    def send(self, msg="exit", showerror=True):
        """Prefix each message with a 4-byte length (network byte order)"""
        try:
            byte_msg = bytes(msg, "utf8")
            byte_msg = stc.pack('>I', len(byte_msg)) + byte_msg
            self._sock.sendall(byte_msg)
            print('client:', msg)
            return True
        except:
            if showerror:
                utl.messagebox("Socket", "Not connected to server", "error")
            return False

    def send_immediate(self, msg="exit"):
        """Send raw byte string without header, used for commands"""
        try:
            self._sock.sendall(bytes(msg, 'utf8'))
            return True
        except:
            return False

    def receive(self, callback=None):
        """Read message length and unpack it into an integer"""
        try:
            raw_msglen = self._sock.recv(4)
            if not raw_msglen:
                return None
            msglen = stc.unpack('>I', raw_msglen)[0]
            data = bytearray()
            while len(data) < msglen:
                packet = self._sock.recv(min(4096, msglen - len(data)))
                if not packet:
                    break
                if not packet == None:
                    data.extend(packet)
                if callback != None:
                    callback(len(data) * 80 / msglen)
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
