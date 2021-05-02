import tkinter as tk
import sys
import io
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


class Registry(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Registry")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self._regpath = ""
        self._regcont = tk.StringVar(self)
        self._regcont.set("")
        self._result = ""
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # ============================ Change from file ============================
        # Display the registry file path
        self.txt_path = tk.Text(self, width=64, height=2, bg="#E5E5E5")
        self.txt_path.grid(row=0, column=0, sticky=tk.N,
                           padx=10, pady=10, columnspan=3)
        # Open the browse window to get the registry file
        self.btn_browse = tk.Button(
            self, text="Browse...", command=self.browse_path, width=22, height=2)
        self.btn_browse.grid(row=0, column=3, sticky=tk.N, padx=10, pady=10)
        # Display the registry file's content
        self.txt_regcont = tk.Text(self, width=64, height=10, bg="#E5E5E5")
        self.txt_regcont.grid(row=1, column=0, sticky=tk.N,
                              padx=10, pady=10, columnspan=3)
        # Send the regis content to the server
        self.btn_sendcont = tk.Button(
            self, text="Gửi\nnội dung", command=None, width=22, height=10)
        self.btn_sendcont.grid(row=1, column=3, sticky=tk.N, padx=10, pady=10)

        # ============================ Break line ============================
        # A line to seperate 2 sending method
        self.lbl_brk = tk.Label(
            self, height=1, text=("-" * 40 + " Sửa giá trị trực tiếp " + "-" * 40), justify="center")
        self.lbl_brk.grid(row=2, column=0, sticky=tk.N,
                          padx=10, pady=0, columnspan=4)

        # ============================ Change from setting ============================
        # Choose functionality
        self.lbl_func = tk.Label(
            self, height=1, text="Chức năng:", width=20, justify="left")
        self.lbl_func.grid(row=3, column=0, sticky=tk.E,
                           padx=10, pady=10, columnspan=1)
        self._func = {'Get value', 'Set value',
                      'Delete value', 'Create key', 'Delete key'}
        self._df_func = tk.StringVar(self)
        self._df_func.set('Chọn chức năng')  # set the default option
        self.opmn_func = tk.OptionMenu(self, self._df_func, *self._func)
        self.opmn_func.grid(row=3, column=1, sticky=tk.W,
                            padx=10, pady=5, columnspan=3)

        # File path
        self.lbl_path = tk.Label(
            self, height=1, text="Đường dẫn:", width=20, justify="left")
        self.lbl_path.grid(row=4, column=0, sticky=tk.E,
                           padx=10, pady=0, columnspan=1)
        self.txt_path = tk.Text(self, width=48, height=1, bg="#E5E5E5")
        self.txt_path.grid(row=4, column=1, sticky=tk.W,
                           padx=10, pady=10, columnspan=3)

        # Name of the value
        self.lbl_name = tk.Label(
            self, height=1, text="Name value", justify="center")
        self.lbl_name.grid(row=5, column=0, sticky=tk.N,
                           padx=10, pady=0, columnspan=1)
        self.txt_name = tk.Text(self, width=24, height=1, bg="#E5E5E5")
        self.txt_name.grid(row=6, column=0, sticky=tk.N,
                           padx=10, pady=10, columnspan=1)

        # Set the value
        self.lbl_value = tk.Label(
            self, height=1, text="Value", justify="center")
        self.lbl_value.grid(row=5, column=1, sticky=tk.N,
                            padx=10, pady=0, columnspan=2)
        self.txt_value = tk.Text(self, width=24, height=1, bg="#E5E5E5")
        self.txt_value.grid(row=6, column=1, sticky=tk.N,
                            padx=10, pady=10, columnspan=2)

        # Choose data type :)))))))))))
        self.lbl_dttype = tk.Label(
            self, height=1, text="Data type", justify="center")
        self.lbl_dttype.grid(row=5, column=3, sticky=tk.N,
                             padx=10, pady=0, columnspan=1)
        self._dttypes = {'String', 'Binary',
                         'DWORD', 'QWORD', 'Multi-String', 'Expandable string'}
        self._df_dttype = tk.StringVar(self)
        self._df_dttype.set('Kiểu dữ liệu')  # set the default option
        self.opmn_func = tk.OptionMenu(self, self._df_dttype, *self._dttypes)
        self.opmn_func.config(width=20)
        self.opmn_func.grid(row=6, column=3, sticky=tk.N,
                            padx=10, pady=5, columnspan=1)

        # Text field to display the result of commands
        self.txt_result = tk.Text(
            self, width=88, height=10, bg="#E5E5E5", state="disable")
        self.txt_result.grid(row=7, column=0, sticky=tk.N,
                             padx=10, pady=10, columnspan=4)

        # Send these command to the server
        self.btn_send = tk.Button(
            self, text="Gửi", command=None, width=10, height=2)
        self.btn_send.grid(row=8, column=0, sticky=tk.N,
                           padx=10, pady=10, columnspan=2)

        # Clear the result text field
        self.btn_clear = tk.Button(
            self, text="Xóa", command=self.clear_result, width=10, height=2)
        self.btn_clear.grid(row=8, column=2, sticky=tk.N,
                            padx=10, pady=10, columnspan=2)

    def browse_path(self):
        files = [('Registry Files', '*.reg'),
                 ('Text Documents', '*.txt'), ('All files', '*')]
        self._regpath = filedialog.askopenfilename(
            filetypes=files, defaultextension=files, title="Open file")
        self.update_cont()

    def update_cont(self):
        try:
            file = open(self._regpath, "r", encoding="utf-16")
            self._regcont = file.read()
            self.txt_regcont.insert("end", self._regcont)
        except IOError:
            print("> file does not appear to exist.")

    def update_result(self, result="Lỗi"):
        self._result = result

    def insert_result(self):
        self._response = self._keybuff.strip("\n")
        self._response += "\n"
        self.txt_result.configure(state="normal")
        self.txt_result.insert("end", self._response)
        self.txt_result.configure(state="disable")

    def clear_result(self):
        self.txt_result.configure(state="normal")
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.configure(state="disable")