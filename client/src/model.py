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


# HOST = input('> Enter host: ')
# PORT = input('> Enter port: ')

HOST = '127.0.0.1'
PORT = 54321

if not PORT:
    PORT = 54321
else:
    PORT = int(PORT)

BUFF_SIZE = 1024
ADDR = (HOST, PORT)


class MySocket:
    def __init__(self, sock=None):
        super().__init__()
        if sock is None:
            self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, address):
        self.sock.connect(address)

    def send(self, command="exit"):
        # Send request to the server and the server return data
        self.sock.sendall(bytes(command, "utf8"))
        print("> request: " + str(command))

    def receive(self):
        try:
            response = self.recv_timeout(self.sock, BUFF_SIZE)
            print("> response received, data size:", sys.getsizeof(response))
            return response
        except OSError:
            return OSError

    def close(self):
        self.sock.close()

    def recv_timeout(self, the_socket, buff, timeout=2):
        # Accumulate all chunks of data sent by the server
        the_socket.setblocking(0)
        total_data = []
        data = ""
        begin = time.time()
        while True:
            # if you got some data, then break after wait sec
            if total_data and time.time() - begin > timeout:
                break
            # if you got no data at all, wait a little longer
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


s = MySocket()
s.connect(ADDR)
cmd = input("> choose a command: ")
s.send(Cmd[cmd])
print(s.receive().decode("utf8"))
s.close()
