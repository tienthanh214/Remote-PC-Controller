import winreg
import os

class Registry:
    def __init__(self, sock = None):
        self.client = sock
        pass

    def run(self):
        while True:
            cmd = self.client.recv(512).decode('utf8')
            print(cmd)
            if cmd == "registry,file":
                self.update_file_reg()
            elif cmd == "exit":
                return
            else:
                if (len(cmd.split(',')) != 6): continue
                cmd, path, name, value, datatype = cmd.rsplit(',', 4) 
                HKEY, link = path.split('\\', 2)
                print(HKEY, link)
                HKEY = self.baseRegistryKey(HKEY)
                datatype = self.baseDataType(datatype)
                reg = winreg.ConnectRegistry(None, HKEY)

                if (cmd == 'registry,get'):
                    self.get_registry(reg, link, name)
                elif cmd == 'registry,set': 
                    self.set_registry(reg, link, name, datatype, value)
                elif cmd == 'registry,deletevalue':
                    self.delete_value_registry(reg, link, name)          
                elif cmd == 'registry,create':
                    self.create_registry(reg, link)
                elif cmd == 'registry,deletekey':
                    self.delete_key_registry(reg, link)

    
    def update_file_reg(self):
        file_len = int(self.client.recv(64).decode("utf8"))
        data = bytearray()
        while len(data) < file_len:
            packet = self.client.recv(1024)
            if not packet: break
            data.extend(packet)

        data = data.decode("utf8")
        print(data)
        fi = open("fileReg.reg", "w")
        fi.write(data)
        fi.close()
        try:
            os.popen("regedit.exe /s src\\fileReg.reg")
        except Exception:
            self.client.send(bytes("FAIL", "utf8"))
            os.remove("fileReg.reg")
        self.client.send(bytes("SUCCESS", "utf8"))
        os.remove("fileReg.reg")


    def get_registry(self, reg, link, name):
        try:
            key =  winreg.OpenKey(reg, link, 0, winreg.KEY_QUERY_VALUE)
            result = winreg.QueryValueEx(key, name) 
            # print(result)
            if not result[0]:
                data = "Error"
            else:
                print(result[0])
                if (result[1] == winreg.REG_MULTI_SZ):
                    data = ''
                    for x in result: data += x + ' '
                else:
                    data = str(result[0])
            self.client.sendall(bytes(data, "utf8"))
            winreg.CloseKey(key) 
        except OSError:
            self.client.sendall(bytes("Error", "utf8"))
            return
        


    def create_registry(self, reg, link):
        try:
            winreg.CreateKey(reg, link)
        except Exception:
            self.client.sendall(bytes("Error", "utf8"))
            return
        self.client.sendall(bytes("Create key successfully", "utf8"))


    def set_registry(self, reg, link, name, datatype, value):
        try: # bug kieu du lieu chua ep
            key =  winreg.OpenKey(reg, link, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, name, 0, datatype, value)
            winreg.CloseKey(key)
        except Exception:
            self.client.sendall(bytes("Error", "utf8"))
            return 
        self.client.sendall(bytes("Set key successfully", "utf8"))
        
    def delete_value_registry(self, reg, link, name):
        try:
            key =  winreg.OpenKey(reg, link, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, name)
        except Exception:
            self.client.sendall(bytes("Error", "utf8"))
            return
        self.client.sendall(bytes("Delete value successfully", "utf8"))

    def delete_key_registry(self, reg, link):
        try:
            winreg.DeleteKeyEx(reg, link)
        except Exception:
            self.client.sendall(bytes("Error", "utf8"))
            return
        self.client.sendall(bytes("Delete key successfully", "utf8"))
        


    def baseRegistryKey(self, name):
        if (len(name) == 0):
            return None
        if name == "HKEY_CLASSES_ROOT":
            return winreg.HKEY_CLASSES_ROOT
        elif name == "HKEY_CURRENT_USER":
            return winreg.HKEY_CURRENT_USER
        elif name == "HKEY_LOCAL_MACHINE":
            return winreg.HKEY_LOCAL_MACHINE
        elif name == "HKEY_USERS":
            return winreg.HKEY_USERS
        elif name == "HKEY_CURRENT_CONFIG":
            return winreg.HKEY_CURRENT_CONFIG
        else:
            return None

    def baseDataType(self, name):
        if len(name) == 0:
            return None
        if name == "String":
            return winreg.REG_SZ
        elif name == "Binary":
            return winreg.REG_BINARY
        elif name == "DWORD":
            return winreg.REG_DWORD
        elif name == "QWORD":
            return winreg.REG_QWORD
        elif name == "Multi-String":
            return winreg.REG_MULTI_SZ
        elif name == "Expandable string":
            return winreg.REG_EXPAND_SZ
        else:
            return None