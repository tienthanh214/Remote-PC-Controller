import socket as sk
import time
from enum import Enum
from threading import Thread
import sys

Cmd = {"connect": "connect",
       "process": "process",
       "app": "app",
       "shutdown": "shutdown",
       "screenshot": "screenshot",
       "keystroke": "keystroke",
       "registry": "registry",
       "exit": "exit"}

# Text-based ommands are sent to the server
# The server than perform operation with window API accordingly


class MySocket:
    def __init__(self, sock=None):
        super().__init__()
        if sock is None:
            self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, ip, port=54321):
        address = (ip, port)
        self.sock.connect(address)

    def send(self, command="exit"):
        # Send request to the server and the server return data
        self.sock.sendall(bytes(command, "utf8"))
        print("> request: " + str(command))

    def receive(self, buff_size=2048):
        try:
            response = self.recv_timeout(self.sock, buff_size)
            print("> response received, data size:", sys.getsizeof(response))
            return response
        except OSError:
            return OSError

    def close(self):
        # Close the socket file descriptor
        # Both sends and receives are disallowed
        self.sock.close()

    def shutdown(self):
        # Shutdown one halves of the connection
        # Further sends are disallowed
        self.sock.shutdown(sk.SHUT_WR)

    def recv_timeout(self, the_socket, buff, timeout=2):
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
                    time.sleep(0.01)
            except:
                pass
        return b"".join(total_data)


# test case
for i in range(3):
    s = MySocket()
    s.connect(ip='localhost', port=54321)
    cmd = input("> choose a command: ")
    if cmd != "exit":
        break
    s.send(Cmd[cmd])
    s.receive()
    s.shutdown()

s.close()
