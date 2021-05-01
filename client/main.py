import src.views.screenshot as scrsh
import src.views.running as runn
import src.views.keystroke as kystk
import src.views.utilities as util
import tkinter as tk
import time
from PIL import Image, ImageTk


def main():
    p = scrsh.Screenshot(tk.Tk())
    p.update_image(open("E:\My_document\MON_MANG_MAY_TINH\Socket-Programming\client\screenshot.png", "rb").read())
    p.mainloop()


if __name__ == "__main__":
    main()
