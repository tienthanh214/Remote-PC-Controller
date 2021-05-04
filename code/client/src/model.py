import socket as sk
import time
import sys
import src.views.utilities as utl

# Text-based ommands are sent to the server
# The server than perform operation with window API accordingly


class MySocket:
    def __init__(self, sock=None):
        super().__init__()
        self._isconnected = False
        if sock is None:
            self._sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        else:
            self._sock = sock

    def connect(self, ip, port=54321):
        self._isconnected = True
        try:
            address = (ip, port)
            self._sock.connect(address)
        except:
            self._isconnected = False

    def send(self, command = "exit"):
        # Send request to the server and the server return data
        self._sock.sendall(bytes(command, "utf8"))
        print("> request: " + str(command))

    def receive(self, length = 2048):
        try:
            data = bytearray()
            while len(data) < length:
                packet = self._sock.recv(length - len(data))
                if not packet:
                    return None
                print(len(data))
                data.extend(packet)
            return data
        except OSError:
            utl.messagebox("Screenshot", "Failed to receive image", "Error")
            pass

    def close(self):
        # Close the socket file descriptor
        # Both sends and receives are disallowed
        self._sock.close()

    def shutdown(self):
        # Shutdown one halves of the connection
        # Further sends are disallowed
        self._sock.shutdown(sk.SHUT_WR)

    def recv_timeout(self, the_socket, buff, timeout=0.5):
        # Collect chunk of data from the server
        # We know that evrything has been received when THE CONNECTION IS CLOSED
        the_socket.setblocking(0)
        total_data = []
        data = ""
        begin = time.time()
        while True:
            if total_data and time.time() - begin > timeout:
                break
            elif time.time() - begin > timeout * 2:
                break
            try:
                data = the_socket.recv(buff)
                if data:
                    total_data.append(data)
                    begin = time.time()
                else:
                    time.sleep(0.02)
            except:
                pass
        return b"".join(total_data)
