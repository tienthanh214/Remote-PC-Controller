import tkinter as tk
import io
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import src.themecolors as THEMECOLOR
from src.mysocket import MySocket


class Screenshot(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self._image_bytes = None
        self.grid()
        self._socket = MySocket.getInstance()
        self.create_widgets()

    def create_widgets(self):
        # Display the image
        self.canvas = tk.Canvas(self, bg="#FFFFFF", width=560, height=560)
        self.item_on_canvas = self.canvas.create_image(
            280, 280, anchor=tk.CENTER, image=None)
        self.canvas.grid(row=0, column=0, sticky=tk.W +
                         tk.N, padx=10, pady=10, rowspan=2)

        # Take another screenshot and update the picture
        # When pressed, Screenshot will sent a request to the server via Controller
        self.btn_snap = tk.Button(
            self, text="Chụp", command=self.snap_screenshot, width=20, height=10)
        self.btn_snap.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)

        # Write the picture to a file as .png, .jpg and .bmp
        self.btn_save = tk.Button(
            self, text="Lưu", command=self.save_image, width=20, height=10)
        self.btn_save.grid(row=1, column=1, sticky=tk.E, padx=10, pady=10)

    def _resize_image(self, IMG):
        h = w = 0
        basewidth = 560
        wpercent = basewidth / float(IMG.size[0])
        hsize = int((float(IMG.size[1]) * float(wpercent)))
        if (hsize > 560):
            h = 560
            hpercent = h / float(hsize)
            w = int((float(basewidth) * float(hpercent)))
        else:
            h = hsize
            w = basewidth

        return IMG.resize((int(w), int(h)), Image.ANTIALIAS)

    def update_image(self, img_data):
        # img_data: bytes
        # Take image data in bytes from and update the image in the canvas
        self._image_bytes = img_data
        stream = io.BytesIO(img_data)
        image = Image.open(stream)

        self._img = ImageTk.PhotoImage(self._resize_image(image))
        self.canvas.itemconfig(self.item_on_canvas, image=self._img)
        self.update_idletasks()
        self.update()

    def save_image(self):
        # img_data: bytes
        # Save an image in bytes form
        if self._image_bytes == None:
            messagebox("Screenshot", "Image data corrupted", "error")
            exit
        files = [('PNG', '*.png'),
                 ('JPEG', '*.jpg;*.jpeg'),
                 ('Bitmap', '*.bmp')]
        file = filedialog.asksaveasfile(
            mode="wb", filetypes=files, defaultextension=files, title="Save image")
        if file != None:
            file.write(self._image_bytes)
            file.close()

    def snap_screenshot(self):
        # send
        self._socket.send("screenshot,snap")
        picture_len = int(self._socket._sock.recv(32).decode('utf8'))
        data = self._socket.receive(length=picture_len)
        self.update_image(data)
