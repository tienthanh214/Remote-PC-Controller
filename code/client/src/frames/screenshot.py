from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from threading import Thread
from src.mysocket import MySocket
import tkinter as tk
import io
import src.textstyles as textstyle
import src.themecolors as THEMECOLOR


class Screenshot(tk.Frame):
    STREAM_BTN_LABEL = 'Theo dõi'
    STOP_BTN_LABEL = 'Dừng xem'

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self._image_bytes = None
        self.grid()
        self._socket = MySocket.getInstance()
        self._doSave = False
        self._continue_stream = False
        self.create_widgets()

    def clean_activity(self):
        self._continue_stream = False

    def create_widgets(self):
        # Display the image
        self.canvas = tk.Canvas(
            self, bg="#000000", highlightthickness=0, width=560, height=560)
        self.item_on_canvas = self.canvas.create_image(
            280, 280, anchor=tk.CENTER, image=None)
        self.canvas.grid(row=0, column=0, sticky=tk.W +
                         tk.N, padx=10, pady=10, rowspan=2)
        # Take another screenshot and update the picture
        # When pressed, Screenshot will sent a request to the server via Controller
        self.btn_snap = tk.Button(
            self, text=Screenshot.STREAM_BTN_LABEL, command=self.stream_screen_async, width=20, height=10)
        self.btn_snap.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
        # Write the picture to a file as .png, .jpg and .bmp
        self.btn_save = tk.Button(
            self, text="Chụp", command=self.snap_image, width=20, height=10)
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
        # Save image data to object
        self._img = ImageTk.PhotoImage(self._resize_image(image))
        try:
            self.canvas.itemconfig(self.item_on_canvas, image=self._img)
        except:
            pass

    def set_doSave(self):
        self._doSave = True

    def snap_image(self):
        copy = self._image_bytes
        ImageOpener(tk.Toplevel(self), 'Preview', copy)

    def stream_screen_async(self):
        if self.btn_snap.cget('text') == Screenshot.STREAM_BTN_LABEL:
            if not self._continue_stream:
                self._continue_stream = True
                Thread(target=self.stream_screen, args=(), daemon=True).start()
            self.btn_snap.configure(text=Screenshot.STOP_BTN_LABEL)
        else:
            self._continue_stream = False
            self.btn_snap.configure(text=Screenshot.STREAM_BTN_LABEL)

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


class ImageOpener(tk.Frame):
    def __init__(self, parent, title, data):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("View Book")
        self.parent.resizable(False, False)
        self._title = title
        self._data = data
        self._img = None
        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        # Show the image on canvas
        self.canvas = tk.Canvas(
            self, bg="#000000", highlightthickness=0, width=560, height=560)
        self.item_on_canvas = self.canvas.create_image(
            280, 280, anchor=tk.CENTER, image=None)
        self.canvas.grid(row=0, column=0, sticky=tk.W +
                         tk.N, padx=10, pady=10, rowspan=2)
        stream = io.BytesIO(self._data)
        image = Image.open(stream)
        self._img = ImageTk.PhotoImage(self._resize_image(image))
        self.canvas.itemconfig(self.item_on_canvas, image=self._img)
        # Save the image to the file system
        self.btn_clear = tk.Button(
            self.parent, text="Download", width=10, height=1, command=self.save_image)
        self.btn_clear.grid(row=2, column=3, sticky=tk.S +
                            tk.E, padx=10, pady=10, columnspan=1)

    def save_image(self):
        if self._data == None:
            messagebox("Screenshot", "Image data corrupted", "error")
            exit
        files = [('PNG', '*.png'),
                 ('JPEG', '*.jpg;*.jpeg'),
                 ('Bitmap', '*.bmp'), ]
        # Open the file system dialog
        file = filedialog.asksaveasfile(
            mode="wb", filetypes=files, defaultextension=files, title="Save image")
        if file != None:
            file.write(self._data)
            file.close()

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
