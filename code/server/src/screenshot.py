import io
from PIL import ImageGrab
import time


class Screenshot:
    def __init__(self, sock):
        self.client = sock
        self.is_live = False
        self.t = time.time()

    def run(self):
        while True:
            cmd = self.client.recv(15).decode('utf8')
            if cmd == "screenshot,snap":
                self.capture()
            elif cmd == "screenshot,live":
                self.livestream()
            elif cmd == "screenshot,stop":
                if self.is_live:
                    self.client.sendall(bytes('done', 'utf8'))
                self.is_live = False
            elif cmd[:4] == "exit":
                if self.is_live:
                    self.client.sendall(bytes('done', 'utf8'))
                self.is_live = False
                return
            if self.is_live:
                self.capture()

    def capture(self):
        image = ImageGrab.grab()
        byteIO = io.BytesIO()
        image.save(byteIO, format='BMP')
        byteArr = byteIO.getvalue()
        # send image Size then read image
        self.client.sendall(byteArr)

    def livestream(self):
        self.is_live = True
        pass
