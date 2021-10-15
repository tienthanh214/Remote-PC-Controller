import tkinter as tk
import src.textstyles as style
import src.themecolors as THEMECOLOR


class Menu(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self.create_widgets()

    def create_widgets(self):
        # --------------------- Group 1 ---------------------
        # Take screenshot
        self.btn_screenshot = tk.Button(
            self, text="Screen", width=40, height=4)
        self.btn_screenshot.grid(
            row=0, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=3)
        # File system
        self.btn_filesys = tk.Button(
            self, text="File system", width=40, height=4)
        self.btn_filesys.grid(
            row=1, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=3)
        # Change registry
        self.btn_registry = tk.Button(
            self, text="Registry", width=40, height=4)
        self.btn_registry.grid(
            row=2, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=3)
        # --------------------- Group 2 ---------------------
        # Show running applications
        self.btn_app = tk.Button(self, text="Appications", width=40, height=4)
        self.btn_app.grid(row=0, column=3, sticky=tk.W+tk.S +
                          tk.E+tk.N, padx=10, pady=10, columnspan=3)
        # Show running processes
        self.btn_process = tk.Button(
            self, text="Processes", width=40, height=4)
        self.btn_process.grid(row=1, column=3, sticky=tk.W +
                              tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=3)
        # Get keystroke
        self.btn_keystroke = tk.Button(
            self, text="Keyboard", width=40, height=4)
        self.btn_keystroke.grid(
            row=2, column=3, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=3)
        # --------------------- Group 3 ---------------------
        # Shutdown computer
        self.btn_shutdown = tk.Button(self, text="Shut down", height=2)
        self.btn_shutdown.grid(
            row=3, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)
        # Logout computer
        self.btn_logout = tk.Button(self, text="Log out", height=2)
        self.btn_logout.grid(row=3, column=2, sticky=tk.W +
                             tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)
        # Exit program
        self.btn_quit = tk.Button(
            self, text="Quit program", height=2, fg="red")
        self.btn_quit.grid(row=3, column=4, sticky=tk.W +
                           tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)
