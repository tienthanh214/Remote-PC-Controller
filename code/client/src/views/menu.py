import tkinter as tk
import sys
import io
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk


class Menu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Client")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Display the entered IP address and connection state
        self.resultLabel = tk.Label(self, text="IP address", width=15)
        self.resultLabel.grid(row=0, column=0, sticky="E",
                              padx=10, pady=10, columnspan=1)

        # Get user input of IP address
        self.myEntry = tk.Entry(self, width=40)
        self.myEntry.focus()
        self.myEntry.bind("<Return>", self.returnIP)
        self.myEntry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

        # Press to connect or disconnect
        self.btn_connect = tk.Button(self, text="CONNECT", fg="green",
                                     command=self.returnIP)
        self.btn_connect.grid(row=0, column=3, sticky=tk.W +
                              tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=1)

        # Show running processes
        self.btn_process = tk.Button(self, text="Process running",
                                     command=None, width=30)
        self.btn_process.grid(row=1, column=0, sticky=tk.W+tk.S +
                              tk.E+tk.N, padx=10, pady=10, columnspan=2, rowspan=1)

        # Show running apps
        self.btn_app = tk.Button(self, text="App running",
                                 command=None, width=30)
        self.btn_app.grid(row=1, column=2, sticky=tk.W+tk.S +
                          tk.E+tk.N, padx=10, pady=10, columnspan=2, rowspan=1)

        # Shutdown computer
        self.btn_shutdown = tk.Button(self, text="Shut down",
                                      command=None)
        self.btn_shutdown.grid(
            row=2, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)

        # Take screenshot
        self.btn_screenshot = tk.Button(self, text="Take screenshot",
                                        command=None)
        self.btn_screenshot.grid(
            row=2, column=2, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)

        # Get keystroke
        self.btn_keystroke = tk.Button(self, text="Get keystroke",
                                       command=None)
        self.btn_keystroke.grid(
            row=3, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)

        # Change registry
        self.btn_registry = tk.Button(self, text="Change registry",
                                      command=None)
        self.btn_registry.grid(
            row=3, column=2, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)

        # Exit program
        self.btn_quit = tk.Button(self, text="EXIT", fg="red",
                                  command=self.master.destroy)
        self.btn_quit.grid(row=4, column=1, sticky=tk.W +
                           tk.S+tk.E+tk.N, padx=10, pady=10, columnspan=2)

    def returnIP(self, args=None):
        print(args)
        result = self.myEntry.get()
        self.resultLabel.config(text=result)
        self.myEntry.delete(0, tk.END)
