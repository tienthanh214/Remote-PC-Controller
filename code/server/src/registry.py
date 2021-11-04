import winreg
import os

class Registry:
    def __init__(self, sock = None):
        self.client = sock
        pass

    def run(self):
        while True:
            cmd = self.client.recv(512).decode('utf8')
            if cmd == "registry,file":
                self.update_file_reg()
            elif cmd == "exit":
                try:
                    os.remove("fileReg.reg") # remove dump
                except:
                    pass
                return
            else:
                if (len(cmd.split(',')) != 6): continue
                cmd, path, name, value, datatype = cmd.rsplit(',', 4) 
                # accept / or \ in path
                path = path.replace('/', '\\')
                if len(path.split('\\', 1)) == 2:
                    HKEY, link = path.split('\\', 1)
                else:
                    HKEY, link = path, ''
                # end of get link
                HKEY = self.baseRegistryKey(HKEY)
                datatype = self.baseDataType(datatype)

                if not HKEY: # key not found
                    self.client.send(bytes("FAIL: HKEY not found", "utf8"))
                    continue

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
        data = self.client.receive()
        fi = open("fileReg.reg", "wb")
        fi.write(data)
        fi.close()
        try:
            os.popen("regedit.exe /s fileReg.reg")
        except Exception:
            self.client.send(bytes("FAIL", "utf8"))
            os.remove("fileReg.reg")
        self.client.send(bytes("SUCCESS", "utf8"))


    def get_registry(self, reg, link, name):
        try:
            key =  winreg.OpenKey(reg, link, 0, winreg.KEY_QUERY_VALUE)
            result = winreg.QueryValueEx(key, name) 
            
            if not result[0]:
                data = "Error"
            else:
                if (result[1] == winreg.REG_MULTI_SZ):
                    data = ''
                    for x in result[0]: data += x + '\n'
                elif (result[1] == winreg.REG_BINARY):
                    data = ' '.join('%02x' % x for x in result[0])
                else:
                    data = str(result[0])
            self.client.sendall(bytes(data, "utf8"))
            winreg.CloseKey(key) 
        except Exception:
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
        try:
            if datatype in [winreg.REG_DWORD, winreg.REG_QWORD]:
                value = int(value)
            elif datatype == winreg.REG_MULTI_SZ:
                value = value.split('\n')
            elif datatype == winreg.REG_BINARY:
                value = value.replace(' ', '')
                value = bytearray.fromhex(value)
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