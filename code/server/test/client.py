import socket
import os
import struct as stc

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('localhost', 54321))

def receive(filename):
    raw_msglen = client.recv(4)
    if not raw_msglen:
        return None
    msglen = stc.unpack('>I', raw_msglen)[0]
    print(msglen)
    f = open(filename, "wb")
    curlen = 0
    while curlen < msglen:
        packet = client.recv(min(4096 * 2, msglen - curlen))
        if not packet:
            break
        f.write(packet)
        curlen += len(packet)
        # use curlen/msglen to show progress bar
    
    f.close()



def send_file(filename):
    print(filename)
    try:
        f = open(filename, "rb")
    except:
        print("file not found")
        return
    filesize = os.path.getsize(filename)
    client.send(stc.pack('>I', filesize))
    print(filesize)
    prog = 0
    while True:
        bytes_read = f.read(4096 * 2)
        if not bytes_read:
            break
        client.sendall(bytes_read)
        prog += len(bytes_read)
        # use prog/filesize to show progress bar
    f.close()


def handle_server():
    receive('ok.mp4')


handle_server()

client.close()