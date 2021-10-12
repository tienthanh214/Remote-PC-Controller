import tkinter as tk
import src.utils as util
from tkinter import ttk
import src.themecolors as THEMECOLOR


class Manager(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=THEMECOLOR.body_bg)
        self.create_widgets()

    def create_widgets(self):
        # Prompt the inputbox
        # User will input the application or process id they want to kill
        self.btn_kill = tk.Button(
            self, text="Kill", width=10, height=2)
        self.btn_kill.grid(row=0, column=0, sticky=tk.N, padx=10, pady=10)

        # Refresh and show running process or application from the server
        self.btn_view = tk.Button(
            self, text="Xem", width=10, height=2)
        self.btn_view.grid(row=0, column=1, sticky=tk.N, padx=10, pady=10)

        # Clear the running process or application table
        self.btn_clear = tk.Button(
            self, text="Xóa", command=self.clear, width=10, height=2)
        self.btn_clear.grid(row=0, column=2, sticky=tk.N, padx=10, pady=10)

        # Similar to btn_kill, but this will take the name of the application and start it instead
        self.btn_start = tk.Button(
            self, text="Start", width=10, height=2)
        self.btn_start.grid(row=0, column=3, sticky=tk.N, padx=10, pady=10)

        # Display info of running process or application from the server
        cols = ("Name", "ID", "Count thread")
        self.table = ttk.Treeview(self, columns=cols, show="headings")
        self.table.grid(row=1, column=0, sticky=tk.N,
                        padx=10, pady=10, columnspan=4)
        for col in cols:
            self.table.heading(col, text=col)
        for i in range(10):
            self.table.insert("", "end", values=("_", "_", "_"))

    def view(self, data):
        # for testing data will be in 2d list
        self.clear()
        if (data):
            data = data.split('\n')[3:-3]  # bo dong title, bo 2 dong \n\n cuoi
            data.sort(key=lambda x: x[0].upper())  # sort de tim theo ten thoi

        for current_process in data:
            (name_process, id_process, count_thread) = current_process.rsplit(maxsplit=2)
            self.table.insert("", "end", values=(
                name_process, id_process, count_thread))

    def clear(self):
        # clear data in the tabel before updating
        for rowid in self.table.get_children():
            self.table.delete(rowid)
