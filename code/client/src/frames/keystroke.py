from tkinter import ttk
from src.mysocket import MySocket
import tkinter as tk
import src.themecolors as THEMECOLOR


class Keystroke(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self.create_widgets()
        self._socket = MySocket.getInstance()

    def create_widgets(self):
        # Start collecting keystroke fro the server
        self.btn_hook = tk.Button(
            self, text="Hook", command=self.keystroke_hook, width=10, height=2)
        self.btn_hook.grid(row=0, column=0, sticky=tk.N, padx=10, pady=10)

        # Stop collecting keystroke from the server
        self.btn_unhook = tk.Button(
            self, text="Unhook", command=self.keystroke_unhook, width=10, height=2)
        self.btn_unhook.grid(row=0, column=1, sticky=tk.N, padx=10, pady=10)

        # Print the collected keystrokes
        self.btn_print = tk.Button(
            self, text="In phím", command=self.keystroke_print, width=10, height=2)
        self.btn_print.grid(row=0, column=2, sticky=tk.N, padx=10, pady=10)

        # Clear the screen
        self.btn_clear = tk.Button(
            self, text="Xóa", command=self.keystroke_clear, width=10, height=2)
        self.btn_clear.grid(row=0, column=3, sticky=tk.N, padx=10, pady=10)

        # Display the text
        self.text_field = tk.Text(
            self, width=64, height=20, bg="#FFFFFF", state="disable")
        self.text_field.grid(row=1, column=0, sticky=tk.N,
                             padx=10, pady=10, columnspan=4)

    def print_keystroke(self, keystroke="<Not hooked>"):
        keystroke = keystroke + "\n"
        self.text_field.configure(state="normal")
        self.text_field.insert("end", keystroke)
        self.text_field.configure(state="disable")

    def keystroke_hook(self):
        self._socket.send(','.join(["keystroke", "hook"]))

    def keystroke_unhook(self):
        self._socket.send(','.join(["keystroke", "unhook"]))

    def keystroke_print(self):
        self._socket.send("keystroke,print")
        log_len = int(self._socket._sock.recv(32).decode('utf8'))
        data = self._socket.receive(length=log_len).decode("utf8")
        self.print_keystroke(data)

    def keystroke_clear(self):
        self.text_field.configure(state="normal")
        self.text_field.delete("1.0", tk.END)
        self.text_field.configure(state="disable")
