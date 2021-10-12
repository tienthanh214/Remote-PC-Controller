import tkinter as tk
from tkinter import ttk


class Keystroke(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Keystroke")
        self.master.resizable(False, False)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Start collecting keystroke fro the server
        self.btn_hook = tk.Button(
            self, text="Hook", width=10, height=2)
        self.btn_hook.grid(row=0, column=0, sticky=tk.N, padx=10, pady=10)

        # Stop collecting keystroke from the server
        self.btn_unhook = tk.Button(
            self, text="Unhook", width=10, height=2)
        self.btn_unhook.grid(row=0, column=1, sticky=tk.N, padx=10, pady=10)

        # Print the collected keystrokes
        self.btn_print = tk.Button(
            self, text="In phím", width=10, height=2)
        self.btn_print.grid(row=0, column=2, sticky=tk.N, padx=10, pady=10)

        # Clear the screen
        self.btn_clear = tk.Button(
            self, text="Xóa", width=10, height=2)
        self.btn_clear.grid(row=0, column=3, sticky=tk.N, padx=10, pady=10)

        # Display the text
        self.text_field = tk.Text(self, width=64, height=20, bg="#FFFFFF", state="disable")

        self.text_field.grid(row=1, column=0, sticky=tk.N,
                             padx=10, pady=10, columnspan=4)

    def print_keystroke(self, keystroke="<Not hooked>"):
        keystroke = keystroke + "\n"
        self.text_field.configure(state="normal")
        self.text_field.insert("end", keystroke)
        self.text_field.configure(state="disable")