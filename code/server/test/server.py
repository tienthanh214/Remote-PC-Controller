import socket
import os
import struct as stc


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 54321))
server.listen(1)

client, addr = server.accept()
print("Connected by: ", addr)

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
    f.close()

def handle_client():
    send_file(r"C:\Users\ninhh\Videos\Captures\Zoom Meeting 2020-05-14 08-02-10.mp4")
    pass

handle_client()
client.close()
server.close()