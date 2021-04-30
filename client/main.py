import src.views.screenshot as ui
import tkinter
import time
from PIL import Image, ImageTk


def main():
    # file = ImageTk.PhotoImage(Image.open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/ndtt.jpg"))
    pic = ui.Screenshot(ui.root)

    # these two line exist within the while loop of tk.mainloop()
    # So, the question is: how do you execute something over and over again without actually
    # creating an infinite loop? Tkinter has an answer for that problem: a widget's after() method:
    

    file0 = open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/menu.png", "rb")
    file1 = open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/screenshot.png", "rb")
    time.sleep(1)
    pic.update_image(file0.read())
    file0.close()


    yn = input("switch:")
    if yn == "y":
        pic.update_image(file1.read())
    file1.close()


    #pic.save_image()

    pic.mainloop()
    # app = menu.Application(menu.root)
    # app.mainloop()


if __name__ == "__main__":
    main()
