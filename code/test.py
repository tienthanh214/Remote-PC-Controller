import socket 
from threading import Thread, Event
import sys
import tkinter

running = True

def run():
    tk.close = tkinter.Button(tk, text = "CLOSE SERVER", 
                                        font = ("Consolas 20 bold"), command = close_server)
    tk.close.grid()
    i = 0
    while running:
        i += 1
        print(i)
        
def close_server():
    running = False
    sys.exit()

def open_server():
    t = Thread(target = run, daemon = True)
    t.start()

tk = tkinter.Tk()
tk.open = tkinter.Button(tk, text = "OPEN SERVER", 
                                        font = ("Consolas 20 bold"), command = open_server)

tk.open.grid()

tk.mainloop()