from src.mysocket import MySocket
from tkinter import ttk, filedialog
import tkinter as tk
import codecs
import src.utils as utl
import src.themecolors as THEMECOLOR
import time


class Registry(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(
            self, parent, bg=THEMECOLOR.body_bg, padx=150, pady=30)
        self._regpath = ""
        self._regcont = tk.StringVar(self)
        self._regcont.set("")
        self._result = ""
        self.create_widgets()
        self._socket = MySocket.getInstance()

    def clean_activity(self):
        pass

    def create_widgets(self):
        # ============================ Change from file ============================
        # Display the registry file path
        self.txt_browse = tk.Text(self, width=64, height=2, bg="#FFFFFF")
        self.txt_browse.grid(row=0, column=0, sticky=tk.N+tk.S,
                             padx=10, pady=10, columnspan=3)
        # Open the browse window to get the registry file
        self.btn_browse = tk.Button(
            self, text="Browse", command=self.browse_path, width=22)
        self.btn_browse.grid(
            row=0, column=3, sticky=tk.N+tk.S, padx=10, pady=10)
        # Display the registry file's content
        self.txt_regcont = tk.Text(self, width=64, height=8, bg="#FFFFFF")
        self.txt_regcont.grid(row=1, column=0, sticky=tk.N+tk.S,
                              padx=10, pady=10, columnspan=3)
        # Send the regis content to the server
        self.btn_sendcont = tk.Button(
            self, text="Send content", command=self.registry_sendcont, width=22)
        self.btn_sendcont.grid(
            row=1, column=3, sticky=tk.N+tk.S, padx=10, pady=10)
        # ============================ Break line ============================
        # A line to seperate 2 sending method
        self.lbl_brk = tk.Label(
            self, height=1, text=("-" * 40 + " Update value " + "-" * 40), justify="center")
        self.lbl_brk.grid(row=2, column=0, sticky=tk.N,
                          padx=10, pady=0, columnspan=4)
        # ============================ Change from setting ============================
        # File path
        self.lbl_path = tk.Label(
            self, height=1, text="Path:", width=20, justify="left")
        self.lbl_path.grid(row=4, column=0, sticky=tk.E,
                           padx=10, pady=0, columnspan=1)
        self.txt_path = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_path.grid(row=4, column=1, sticky=tk.W,
                           padx=10, pady=10, columnspan=3)
        # Name of the value
        self.lbl_name = tk.Label(
            self, height=1, text="Name value", justify="center")
        self.lbl_name.grid(row=5, column=0, sticky=tk.N,
                           padx=10, pady=0, columnspan=1)
        self.txt_name = tk.Text(self, width=24, height=1, bg="#FFFFFF")
        self.txt_name.grid(row=6, column=0, sticky=tk.N,
                           padx=10, pady=10, columnspan=1)
        # Set the value
        self.lbl_value = tk.Label(
            self, height=1, text="Value", justify="center")
        self.lbl_value.grid(row=5, column=1, sticky=tk.N,
                            padx=10, pady=0, columnspan=2)
        self.txt_value = tk.Text(self, width=24, height=1, bg="#FFFFFF")
        self.txt_value.grid(row=6, column=1, sticky=tk.N,
                            padx=10, pady=10, columnspan=2)
        # Choose data type
        self.lbl_dttype = tk.Label(
            self, height=1, text="Data type", justify="center")
        self.lbl_dttype.grid(row=5, column=3, sticky=tk.N,
                             padx=10, pady=0, columnspan=1)
        self._dttypes = {'String', 'Binary',
                         'DWORD', 'QWORD', 'Multi-String', 'Expandable string'}
        self._df_dttype = tk.StringVar(self)
        self._df_dttype.set('String')  # set the default option
        self.opmn_dttype = tk.OptionMenu(self, self._df_dttype, *self._dttypes)
        self.opmn_dttype.config(width=20)
        self.opmn_dttype.grid(row=6, column=3, sticky=tk.N,
                              padx=10, pady=5, columnspan=1)
        # Text field to display the result of commands
        self.txt_result = tk.Text(
            self, width=88, height=10, bg="#FFFFFF", fg='#000000', state="disable")
        self.txt_result.grid(row=7, column=0, sticky=tk.N,
                             padx=10, pady=10, columnspan=4)
        # Send these command to the server
        self.btn_send = tk.Button(
            self, text="Enter", command=self.registry_send, width=10, height=2)
        self.btn_send.grid(row=8, column=1, sticky=tk.N+tk.W,
                           padx=10, pady=10, columnspan=1)
        # Clear the result text field
        self.btn_clear = tk.Button(
            self, text="Clear", command=self.clear_result, width=10, height=2)
        self.btn_clear.grid(row=8, column=2, sticky=tk.N+tk.E,
                            padx=10, pady=10, columnspan=1)
        # Choose functionality
        self.lbl_func = tk.Label(
            self, height=1, text="Functions:", width=20, justify="left")
        self.lbl_func.grid(row=3, column=0, sticky=tk.E,
                           padx=10, pady=10, columnspan=1)
        self._func = {'Get value', 'Set value',
                      'Delete value', 'Create key', 'Delete key'}
        self._df_func = tk.StringVar(self)
        self._df_func.trace("w", lambda a, b, c: self.update_ui(a=a, b=b, c=c))
        self._df_func.set('Get value')
        self.opmn_func = tk.OptionMenu(self, self._df_func, *self._func)
        self.opmn_func.grid(row=3, column=1, sticky=tk.W,
                            padx=10, pady=5, columnspan=3)

    def browse_path(self):
        files = [('Registry Files', '*.reg'),
                 ('Text Documents', '*.txt'), ('All files', '*')]
        self._regpath = filedialog.askopenfilename(
            filetypes=files, defaultextension=files, title="Open file")
        self.txt_browse.delete("1.0", tk.END)
        self.txt_browse.insert("end", self._regpath)
        self.update_cont()

    def update_cont(self):
        try:
            file = codecs.open(filename=self._regpath,
                               mode="r", encoding="utf-16")
            self._regcont = file.read()
            self.txt_regcont.delete("1.0", tk.END)
            self.txt_regcont.insert("end", self._regcont)
        except IOError:
            utl.messagebox("Registry", "Cannot load file", "error")

    def insert_result(self, result="<Error>"):
        self._response = result.strip("\n")
        self._response += "\n"
        self.txt_result.configure(state="normal")
        self.txt_result.insert(tk.END, self._response)
        self.txt_result.configure(state="disable")

    def clear_result(self):
        self.txt_result.configure(state="normal")
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.configure(state="disable")

    def update_ui(self, a, b, c):
        if self._df_func.get() == "Set value":
            self.lbl_name.grid()
            self.txt_name.grid()
            self.lbl_value.grid()
            self.txt_value.grid()
            self.lbl_dttype.grid()
            self.opmn_dttype.grid()
        else:
            self.lbl_value.grid_remove()
            self.txt_value.grid_remove()
            self.lbl_dttype.grid_remove()
            self.opmn_dttype.grid_remove()

            if self._df_func.get() == "Create key" or self._df_func.get() == "Delete key":
                self.lbl_name.grid_remove()
                self.txt_name.grid_remove()
            else:
                self.lbl_name.grid()
                self.txt_name.grid()

    def registry_sendcont(self):
        filecont = self.txt_regcont.get("1.0", tk.END)
        self._socket._isconnected = self._socket.send_immediate(
            "registry,file")
        if not self._socket._isconnected:
            return
        self._socket.send(filecont)

        response = self._socket._sock.recv(7).decode("utf8")
        utl.messagebox("Send regsitry file", response,
                       "info" if response == "SUCCESS" else "error")

    def registry_send(self):
        func = self._df_func.get().strip("\n")
        path = self.txt_path.get("1.0", tk.END).strip("\n")
        if len(path) == 0: return
        name = self.txt_name.get("1.0", tk.END).strip("\n")
        if len(name) == 0: return
        value = self.txt_value.get("1.0", tk.END).strip("\n")
        if len(value) == 0: return
        dttp = self._df_dttype.get().strip("\n")

        if func in ['Get value', 'Set value', 'Create key']:
            func = func.split(" ", 1)[0].lower()
        else:
            func = func.replace(" ", "").lower()
        self._socket._isconnected = self._socket.send_immediate(
            ','.join(["registry", func, path, name, value, dttp]))
        if not self._socket._isconnected:
            return
        response = self._socket.receive().decode('utf8')
        self.insert_result(response)
