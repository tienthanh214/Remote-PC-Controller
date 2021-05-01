import src.views.screenshot as scrsh
import src.views.process as prcs
import src.views.utilities as util
import tkinter as tk
import time
from PIL import Image, ImageTk


def main():
    p = prcs.Process(tk.Tk(), 'app')
    p.mainloop()


if __name__ == "__main__":
    main()
