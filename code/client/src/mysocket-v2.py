import socket as sk
import struct as stc


class MySocket(sk.socket):
    def __init__(self, *args, **kwargs):
        super(MySocket, self).__init__(*args, **kwargs)

    @classmethod
    def copy(cls, sock):
        fd = sk.dup(sock.fileno())
        copy = cls(sock.family, sock.type, sock.proto, fileno=fd)
        copy.settimeout(sock.gettimeout())
        return copy

    def accept(self):
        con, addr = sk.socket.accept(self)
        return MySocket.copy(con), addr

    def send(self, msg):
        """Prefix each message with a 4-byte length (network byte order)"""
        msg = stc.pack('>I', len(msg)) + msg
        self.sendall(msg)

    def receive(self):
        """Read message length and unpack it into an integer"""
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = stc.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen)

    def recvall(self, n):
        """Helper function to recv n bytes or return None if EOF is hit"""
        data = bytearray()
        while len(data) < n:
            packet = self.recv(n - len(data))
            if not packet:
                break
            if not packet == None:
                data.extend(packet)
        return data
