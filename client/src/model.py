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


def recv_timeout(the_socket, buff, timeout=2):
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
            data = the_socket.recv(buff).decode("utf8")
            if data:
                total_data.append(data)
                begin = time.time()
            else:
                time.sleep(0.01)
        except:
            pass
    return "".join(total_data)


def receive_txt():
    # Handle response from the server
    try:
        response = recv_timeout(client_socket, BUFF_SIZE)
        print("> response: ", response)
    except OSError:
        exit


def receive_img():
    try:
        file = open('./screenshot.png', 'wb')
        chunk = client_socket.recv(1024)
        while chunk:
            print("> receiving...")
            file.write(chunk)
            chunk = client_socket.recv(1024)
        print("> image downloaded")
        file.close()
    except OSError:
        exit


def send(command="exit"):
    # Send request to the server and the server return data
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


for i in range(5):
    cmd = input("> choose a command: ")

    targ = receive_txt
    if cmd == "screenshot":
        targ = receive_img
    receive_thread = Thread(target=targ)
    receive_thread.start()

    send(command=Cmd[cmd])
    receive_thread.join()

client_socket.close()
