import tkinter as tk
import src.textstyles as style
import src.themecolors as THEMECOLOR


class Menu(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self.create_widgets()

    def create_widgets(self):
        # Show running processes
        self.btn_process = tk.Button(self, text="Process running",
                                     width=30)
        self.btn_process.grid(row=1, column=0, sticky=tk.W+tk.S +
                              tk.E+tk.N, padx=10, pady=10, columnspan=2, rowspan=1)

        # Show running apps
        self.btn_app = tk.Button(self, text="App running", width=30)
        self.btn_app.grid(row=1, column=2, sticky=tk.W+tk.S +
                          tk.E+tk.N, padx=10, pady=10, columnspan=2, rowspan=1)

        # Shutdown computer
        self.btn_shutdown = tk.Button(self, text="Shut down")
        self.btn_shutdown.grid(
            row=2, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)

        # Take screenshot
        self.btn_screenshot = tk.Button(self, text="Take screenshot")
        self.btn_screenshot.grid(
            row=2, column=2, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)

        # Get keystroke
        self.btn_keystroke = tk.Button(self, text="Get keystroke")
        self.btn_keystroke.grid(
            row=3, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)

        # Change registry
        self.btn_registry = tk.Button(self, text="Change registry")
        self.btn_registry.grid(
            row=3, column=2, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)

        # Exit program
        self.btn_quit = tk.Button(self, text="QUIT PROGRAM", fg="red")
        self.btn_quit.grid(row=4, column=1, sticky=tk.W +
                           tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)