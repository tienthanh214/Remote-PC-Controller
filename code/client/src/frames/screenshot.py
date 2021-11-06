from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from threading import Thread
from src.mysocket import MySocket
import tkinter as tk
import io
import src.textstyles as textstyle
import src.themecolors as THEMECOLOR


class Screenshot(tk.Frame):
    STREAM_BTN_LABEL = 'Watch'
    STOP_BTN_LABEL = 'Pause'

    def __init__(self, parent):
        tk.Frame.__init__(
            self, parent, bg=THEMECOLOR.body_bg)
        self._image_bytes = None
        self.grid()
        self._socket = MySocket.getInstance()
        self._doSave = False
        self._continue_stream = False
        self._img_size = None
        self.create_widgets()

    def clean_activity(self):
        self._continue_stream = False

    def create_icons(self):
        self.icons = {}
        self.icons['stream'] = self.create_sprite(
            'assets/screenshot/ic_stream.png')
        self.icons['pause'] = self.create_sprite(
            'assets/screenshot/ic_pause.png')
        self.icons['take'] = self.create_sprite(
            'assets/screenshot/ic_take.png')

    def create_sprite(self, path):
        image = Image.open(path)
        image.mode = 'RGBA'
        return ImageTk.PhotoImage(image)

    def create_widgets(self):

        self.create_icons()

        self.img = Image.open("assets/screenshot/screenGUI.png")
        self.img1 = self.img.resize((1024, 650), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.img1)
        self.bgImage = tk.Label(self, image=self.bg, highlightthickness=0, borderwidth=0).grid(
            column=0, row=0, sticky=tk.S+tk.N+tk.W+tk.E)
        # Display the image
        self.canvas = tk.Canvas(
            self, bg="#000000", highlightthickness=0, width=835, height=395)
        self.item_on_canvas = self.canvas.create_image(
            417, 198, anchor=tk.CENTER, image=None)
        # Adjust base on individual
        self.canvas.place(x=93, y=85)
        # Take another screenshot and update the picture
        # When pressed, Screenshot will sent a request to the server via Controller
        self.btn_snap = tk.Button(
            self, text=Screenshot.STREAM_BTN_LABEL, image=self.icons['stream'], command=self.stream_screen_async, fg="black", activebackground="#800000",
            activeforeground="black", borderwidth=3, cursor="hand2", compound=tk.LEFT)
        self.btn_snap.place(anchor='center', x=390, y=620)
        self.btn_snap.config(height=50, width=100)
        # Write the picture to a file as .png, .jpg and .bmp
        self.btn_save = tk.Button(
            self, text="Screenshot", image=self.icons['take'], command=self.snap_image, fg="black", activebackground="#800000",
            activeforeground="black", borderwidth=3, cursor="hand2", compound=tk.LEFT)
        self.btn_save.place(anchor='center', x=620, y=620)
        self.btn_save.config(height=50, width=100)

    def _resize_image(self, IMG):
        if self._img_size == None:
            h = w = 0
            basewidth = 860
            wpercent = basewidth / float(IMG.size[0])
            hsize = int((float(IMG.size[1]) * float(wpercent)))
            if (hsize > 400):
                h = 400
                hpercent = h / float(hsize)
                w = int((float(basewidth) * float(hpercent))) + 80
            else:
                h = hsize
                w = basewidth
            self._img_size= (int(w), int(h))
        return IMG.resize(self._img_size, Image.ANTIALIAS)

    def update_image(self, img_data):
        # img_data: bytes
        # Take image data in bytes from and update the image in the canvas
        self._image_bytes = img_data
        image = Image.open(io.BytesIO(img_data))
        # Save image data to object
        try:
            _img = ImageTk.PhotoImage(self._resize_image(image))
            self.canvas.itemconfig(self.item_on_canvas, image=_img)
            self.canvas.image = _img
        except:
            pass
        
    def set_doSave(self):
        self._doSave = True

    def snap_image(self):
        if self._image_bytes == None:
            return
        self._data = self._image_bytes
        if self._data == None:
            messagebox("Screenshot", "Image data corrupted", "error")
            exit
        files = [('PNG', '*.png'),
                 ('JPEG', '*.jpg;*.jpeg'),
                 ('Bitmap', '*.bmp'), ]
        # Open the file system dialog
        file = filedialog.asksaveasfile(
            mode="wb", filetypes=files, defaultextension=files, title="Save image to this location")
        if file != None:
            file.write(self._data)
            file.close()

    def stream_screen_async(self):
        if self.btn_snap.cget('text') == Screenshot.STREAM_BTN_LABEL:
            if not self._continue_stream:
                self._continue_stream = True
                Thread(target=self.stream_screen, args=(), daemon=True).start()
            self.btn_snap.configure(
                text=Screenshot.STOP_BTN_LABEL, image=self.icons['pause'])
        else:
            self._continue_stream = False
            self.btn_snap.configure(
                text=Screenshot.STREAM_BTN_LABEL, image=self.icons['stream'])

    def stream_screen(self):
        self._socket.send_immediate("screenshot,live")
        while True:
            data = self._socket.receive()
            if len(data) == 4:
                return
            self._socket.send_immediate("ok")
            self.update_image(data)
            # Stop stream if we want
            if not self._continue_stream:
                self._socket.send_immediate("screenshot,stop")
            # Interrupt an grab current image data for the window
            if self._doSave:
                Thread(target=self.snap_image, args=(), daemon=True).start()
                self._doSave = False
