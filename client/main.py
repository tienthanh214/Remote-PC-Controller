import src.views.menu as menu
import src.views.screenshot as scrsh
import src.views.running as runng
import src.views.keystroke as kystk
import src.views.registry as regis
import src.views.utilities as util
import tkinter as tk
import time
from PIL import Image, ImageTk


def main():
    p = menu.Menu(tk.Tk())
    p.mainloop()

    p = scrsh.Screenshot(tk.Tk())
    p.mainloop()

    p = runng.Running(tk.Tk())
    p.mainloop()
    
    p = runng.Running(tk.Tk(), command="App")
    p.mainloop()

    p = kystk.Keystroke(tk.Tk())
    p.mainloop()

    p = regis.Registry(tk.Tk())
    p.mainloop()


if __name__ == "__main__":
    main()
