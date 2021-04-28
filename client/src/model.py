import socket as sk
import time
from enum import Enum
from threading import Thread


Cmd = {"connect": "connect",
       "process": "process",
       "app": "app",
       "shutdown": "shutdown",
       "screenshot": "screenshot",
       "keystroke": "keystroke",
       "registry": "registry",
       "exit": "exit"}

def recvall(sock):
    data = bytearray()
    while True:
        packet = sock.recv(BUFF_SIZE)
        if not packet:  # Important!!
            break
        data.extend(packet)
    return data

def receive():
    # Handle data from the server
    try:
        response = client_socket.recv(BUFF_SIZE).decode("utf8")
        print("> response: ", response)
    except OSError:
        exit


def send(command="exit"):
    client_socket.sendall(bytes(command, "utf8"))
    print("> request: " + str(command))


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

client_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
client_socket.connect(ADDR)
print('> connected to port ' + str(PORT))


for i in range(10):
    receive_thread = Thread(target=receive)
    receive_thread.start()
    cmd = input("> choose a command: ")
    send(command=Cmd[cmd])
    receive_thread.join()
    #print("> returned response ", response)
    #response.pop()

client_socket.close()
