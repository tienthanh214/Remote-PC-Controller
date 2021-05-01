import src.views.screenshot as scrsh
import src.views.running as runng
import src.views.keystroke as kystk
import src.views.registry as regis
import src.views.utilities as util
import tkinter as tk
import time
from PIL import Image, ImageTk


def main():
    p = regis.Registry(tk.Tk())
    p.mainloop()


if __name__ == "__main__":
    main()
