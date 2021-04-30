import src.views.screenshot as ui
import tkinter as tk
import time
from PIL import Image, ImageTk


def main():
    # file = ImageTk.PhotoImage(Image.open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/ndtt.jpg"))
    pic = ui.Screenshot(tk.Tk())

    # these two line exist within the while loop of tk.mainloop()
    # So, the question is: how do you execute something over and over again without actually
    # creating an infinite loop? Tkinter has an answer for that problem: a widget's after() method:
    

    file0 = open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/menu.png", "rb")
    file1 = open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/screenshot.png", "rb")
    time.sleep(1)
    pic.update_image(file0.read())


    yn = input("switch:")
    if yn == "y":
        pic.update_image(file1.read())


    #pic.save_image()
    pic.mainloop()

    file0.close()
    file1.close()

    
    pic1 = ui.Screenshot(tk.Tk())

    file0 = open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/menu.png", "rb")
    file1 = open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/screenshot.png", "rb")
    

    time.sleep(1)
    pic1.update_image(file0.read())


    yn = input("switch:")
    if yn == "y":
        pic1.update_image(file1.read())


    #pic.save_image()

    pic1.mainloop()
    # app = menu.Application(menu.root)
    # app.mainloop()


if __name__ == "__main__":
    main()
