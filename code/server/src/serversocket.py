import socket as sk
import struct as stc

class ServerSocket(sk.socket):
    __instance = None

    @staticmethod
    def getInstance():
        if ServerSocket.__instance == None:
            ServerSocket(sk.AF_INET, sk.SOCK_STREAM)
        return ServerSocket.__instance

    def __init__(self, *args, **kwargs):
        # super().__init__()
        super(ServerSocket, self).__init__(*args, **kwargs)
        self._reset()
        ServerSocket.__instance = self

    def _reset(self):
        self._isconnected = False
        # self = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    @classmethod
    def copy(cls, sock):
        fd = sk.dup(sock.fileno())
        copy = cls(sock.family, sock.type, sock.proto, fileno = fd)
        copy.settimeout(sock.gettimeout())
        return copy

    def accept(self):
        con, addr = sk.socket.accept(self)
        return ServerSocket.copy(con), addr

    def sendall(self, msg):
        """Prefix each message with a 4-byte length (network byte order)"""
        byte_msg = stc.pack('>I', len(msg)) + msg
        super().sendall(byte_msg)

    def receive(self):
        """Read message length and unpack it into an integer"""
        raw_msglen = self._sock.recv(4)
        if not raw_msglen:
            return None
        if raw_msglen == b'exit':
            return b'exit'
            
        msglen = stc.unpack('>I', raw_msglen)[0]
        data = bytearray()
        while len(data) < msglen:
            packet = self._sock.recv(4096)
            if not packet:
                break
            if not packet == None:
                data.extend(packet)
        return data
        

    # def close(self):
    #     # Close the socket file descriptor
    #     # Both sends and receives are disallowed
    #     self._sock.close()
    #     self._reset()

    # def shutdown(self):
    #     # Shutdown one halves of the connection
    #     # Further sends are disallowed
    #     self._sock.shutdown(sk.SHUT_WR)
    #     self._reset()
