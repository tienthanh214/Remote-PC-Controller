import src.view as menu


def main():
    app = menu.Application(menu.root)
    app.master.mainloop()

    menu.popup_notif('hello world')


if __name__ == "__main__":
    main()
