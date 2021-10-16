from tkinter import ttk
from src.mysocket import MySocket
import tkinter as tk
import src.themecolors as THEMECOLOR


class Keystroke(tk.Frame):
    HOOK_BTN_LABEL = 'Hook'
    UNHOOK_BTN_LABEL = 'Unhook'
    LOCK_BTN_LABEL = 'Khóa'
    UNLOCK_BTN_LABEL = 'Mở khóa'

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self.create_widgets()
        self._socket = MySocket.getInstance()

    def create_widgets(self):
        # Start collecting keystroke fro the server
        self.btn_hook = tk.Button(
            self, text=Keystroke.HOOK_BTN_LABEL, command=self.keystroke_hook, width=10, height=2)
        self.btn_hook.grid(row=0, column=5, sticky=tk.N,
                           padx=10, pady=5, rowspan=2)

        # Print the collected keystrokes
        self.btn_print = tk.Button(
            self, text="In phím", command=self.keystroke_print, width=10, height=2)
        self.btn_print.grid(row=2, column=5, sticky=tk.N,
                            padx=10, pady=5, rowspan=2)

        # Clear the screen
        self.btn_clear = tk.Button(
            self, text="Xóa", command=self.keystroke_clear, width=10, height=2)
        self.btn_clear.grid(row=4, column=5, sticky=tk.N,
                            padx=10, pady=5, rowspan=2)

        # Lock the keyboard
        self.btn_lock = tk.Button(
            self, text=Keystroke.LOCK_BTN_LABEL, command=self.keystroke_lock, width=10, height=2)
        self.btn_lock.grid(row=6, column=5, sticky=tk.N,
                           padx=10, pady=5, rowspan=2)

        # Display the text
        self.text_field = tk.Text(
            self, width=64, height=20, bg="#FFFFFF", state="disable")
        self.text_field.grid(row=0, column=0, sticky=tk.N,
                             padx=10, pady=5, columnspan=5, rowspan=8)

    def keystroke_lock(self):
        if self.btn_lock.cget('text') == Keystroke.LOCK_BTN_LABEL:
            self._socket.send_immediate('keystroke,lock')
            self.btn_lock.configure(text=Keystroke.UNLOCK_BTN_LABEL)
        else:
            self._socket.send_immediate('keystroke,unlock')
            self.btn_lock.configure(text=Keystroke.LOCK_BTN_LABEL)

    def print_keystroke(self, keystroke="<Not hooked>"):
        keystroke = keystroke + "\n"
        self.text_field.configure(state="normal")
        self.text_field.insert("end", keystroke)
        self.text_field.configure(state="disable")

    def keystroke_hook(self):
        if self.btn_hook.cget('text') == Keystroke.HOOK_BTN_LABEL:
            self._socket.send_immediate('keystroke,hook')
            self.btn_hook.configure(text=Keystroke.UNHOOK_BTN_LABEL)
        else:
            self._socket.send_immediate('keystroke,unhook')
            self.btn_hook.configure(text=Keystroke.HOOK_BTN_LABEL)

    def keystroke_print(self):
        self._socket.send_immediate("keystroke,print")
        data = self._socket.receive().decode("utf8")
        self.print_keystroke(data)

    def keystroke_clear(self):
        self.text_field.configure(state="normal")
        self.text_field.delete("1.0", tk.END)
        self.text_field.configure(state="disable")
