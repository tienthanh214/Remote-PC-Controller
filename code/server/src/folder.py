import os
import shutil
import pickle
import struct as stc
import win32api

class Folder:
    def __init__(self, sock) -> None:
        self.client = sock
        # send list of all available Windows's drives
        drives_list = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        self.client.sendall(pickle.dumps(drives_list))
        pass

    def run(self):
        while True:
            try:
                cmd = self.client.receive().decode('utf8')
            except:
                return
            cmd = cmd.split(',')
            if cmd[0] == "exit":
                return
            if cmd[0] != "folder":
                return
            if cmd[1] == "view":
                self.view_folder(cmd[2])
            elif cmd[1] == "copy":
                self.copy_file(cmd[2], cmd[3])
            elif cmd[1] == "del":
                self.delete_file(cmd[2])
            elif cmd[1] == "move":
                self.move_file(cmd[2], cmd[3])

    def view_folder(self, path):
        # list of tuple (path, is this a direction)
        try:
            if not os.path.isdir(path):
                list_dir = []
            else:
                list_dir = [(x, os.path.isdir(os.path.join(path, x)))
                            for x in os.listdir(path)]
            list_dir.sort(key = lambda x : not x[1])
            self.client.sendall(pickle.dumps(list_dir))
        except:
            self.client.sendall(bytes('bad', 'utf8'))

    def copy_file(self, source, target):
        if source == '?':       # copy from client to server
            self.receive_file(target)
        elif target == '?':     # copy from server to client
            self.send_file(source)
        else:                   # copy inside server
            try:
                shutil.copy2(source, target)
                self.client.send(bytes('ok', 'utf8'))
            except:
                # print("File Not Found Error")
                self.client.send(bytes('bad', 'utf8'))
        pass
    
    def move_file(self, source, target):
        """ move a file from source to target
            target can be a folder or a file
        """
        try:
            shutil.move(source, target)
            self.client.send(bytes('ok', 'utf8'))
        except:
            # print("Can't move this file")
            self.client.send(bytes('bad', 'utf8'))
        pass
    
    def delete_file(self, path):
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            self.client.send(bytes('ok', 'utf8'))
        except:
            self.client.send(bytes('bad', 'utf8'))
        pass

    def receive_file(self, filename):
        print(filename)
        raw_msglen = self.client.recv(4)
        if not raw_msglen:
            return None
        # get file sie first
        msglen = stc.unpack('>I', raw_msglen)[0]
        print(msglen)
        try:
            f = open(filename, "wb")
        except:
            # print("Invalid path")
            return
        curlen = 0
        # read binary data to file
        while curlen < msglen:
            packet = self.client.recv(min(4096 * 2, msglen - curlen))
            if not packet:
                break
            f.write(packet)
            curlen += len(packet)
            # use curlen/msglen to show progress bar
        f.close()

    def send_file(self, filename):
        print(filename)
        try:
            f = open(filename, "rb")
        except:
            # print("file not found")
            return
        filesize = os.path.getsize(filename)
        # send file size first
        self.client.send(stc.pack('>I', filesize))
        print(filesize)
        prog = 0
        while True:
            bytes_read = f.read(4096 * 2)
            if not bytes_read:
                break
            self.client.sendall(bytes_read)
            prog += len(bytes_read)
            # use prog/filesize to show progress bar
        f.close()
