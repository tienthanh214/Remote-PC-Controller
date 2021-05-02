import tkinter as tk
import socket

class Server:
    def __init__(self):
        super().__init__()
        self._root = tk.Tk()
        self._root.geometry('300x200')
        self._root.title("Server")
        self._root.btn_open_server = tk.Button(self._root, text = "OPEN SERVER", 
                                        font = ("Consolas 20 bold"), command = self.open_server)
        
        self._root.btn_open_server.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)


    def run(self):
        self._root.mainloop()

    def open_server(self):
        IP = (socket.gethostbyname('localhost'), 54321)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(IP)
        self.server.listen(1)

        self.client, addr = self.server.accept()
        print("Connected by ", addr)
        while True:
            msg = self.client.recv(1024)
            print(msg)
            if (msg == "QUIT"):
                break

    pass

app = Server()
app.run()