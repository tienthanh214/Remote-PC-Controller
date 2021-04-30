import src.view as ui
import tkinter
import time
from PIL import Image, ImageTk


def main():
    file = ImageTk.PhotoImage(Image.open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/ndtt.jpg"))
    pic = ui.Screenshot(ui.root)

    # these two line exist within the while loop of tk.mainloop()
    # So, the question is: how do you execute something over and over again without actually
    # creating an infinite loop? Tkinter has an answer for that problem: a widget's after() method:
    pic.update_idletasks()
    pic.update()

    time.sleep(1)
    pic.update_image(file)

    file1 = ImageTk.PhotoImage(Image.open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/menu.png"))
    time.sleep(1)
    pic.update_image(file1)

    file = open("E:/My_document/MON_MANG_MAY_TINH/Socket-Programming/client/_server_assets/menu.png", "rb").read()
    pic.save_image(file)

    pic.mainloop()
    # app = menu.Application(menu.root)
    # app.mainloop()


if __name__ == "__main__":
    main()
