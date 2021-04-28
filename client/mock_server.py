# Used to test commands sent to the server

# The client sends the command to the this server, the server
# will print the command and send back fake text data and image


import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 54321        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("> waiting for connection...")
s.listen(1)

my_data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sollicitudin euismod lacus, congue faucibus dolor aliquet eget. Morbi luctus, magna dignissim dignissim blandit, leo quam hendrerit sem, eget lobortis felis mauris nec elit. Pellentesque pellentesque diam est, at cursus nisl semper ut. Mauris tincidunt, neque auctor feugiat porttitor, nibh elit volutpat tellus, vel tristique augue massa a dolor. Cras et scelerisque felis, vitae commodo ex. Maecenas elementum nunc ac eros dignissim, non rutrum nulla ornare. Morbi scelerisque dignissim scelerisque. Nunc commodo, metus nec consectetur placerat, nisl ligula pellentesque nulla, a pellentesque neque sem vulputate eros. Vivamus et odio a arcu vestibulum pretium. Aliquam tempor justo eu nunc pulvinar elementum eu id dui. Donec rhoncus sem eu dui consectetur, sed consectetur mi aliquam. Donec massa justo, posuere sit amet porta ut, fermentum vel nunc. Maecenas elementum ultricies massa in eleifend. In interdum rutrum tempus. Aliquam dictum, nisl ac condimentum vulputate, lorem velit lobortis est, interdum dictum quam magna a ipsum. Phasellus consectetur ullamcorper ultrices. In hac habitasse platea dictumst. Donec in ex finibus, elementum ex vitae, egestas enim. Aenean semper mattis dolor, nec sagittis ligula. Maecenas et ipsum diam. Vivamus fringilla suscipit lorem tempus faucibus. Quisque sed imperdiet augue. Quisque lobortis neque et orci eleifend dapibus. Proin iaculis magna lectus, nec placerat elit consectetur vitae. Nullam et diam ac massa feugiat fermentum. Sed vulputate tempor blandit. Etiam turpis velit, lacinia vitae aliquet quis, laoreet eu lectus. Morbi sit amet aliquam lectus, sed cursus nulla. Phasellus et sem vel neque rutrum convallis vel sed turpis."

while True:
    conn, addr = s.accept()
    # count += 1
    try:
        print('> connected by', addr)
        while True:
            data = conn.recv(1024)
            str_data = data.decode("utf8")

            print("> client: " + str_data)

            if str_data == "exit":
                # exit and close this connection 
                break
            elif str_data == "screenshot":
                # send a image data to the client
                f = open('./_server_assets/screenshot.png','rb')
                l = f.read(1024)
                while l:
                    conn.send(l)
                    l = f.read(1024)
                print("> image sent")
                conn.shutdown(socket.SHUT_WR)
                f.close()
            else:
                # send a text to be displayed by the GUI
                conn.sendall(bytes(my_data, "utf8"))
    finally:
        # Clean up the connection
        conn.close()
        print('> connection closed')
        # if count == 2:
        #     break
s.close()
