import tkinter as tk

root = tk.Tk()
root.title("Client")
root.geometry("560x320+200+100")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
# Configure row and column setting so that widget will take up all space
# tk.Grid.rowconfigure(root, 0, weight=1)
# tk.Grid.columnconfigure(root, 0, weight=1)

# # Create & Configure frame
# frame = tk.Frame(root)
# frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

# for row_index in range(5):
#     tk.Grid.rowconfigure(frame, row_index, weight=1)
#     for col_index in range(10):
#         tk.Grid.columnconfigure(frame, col_index, weight=1)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = root
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Display the entered IP address and connection state
        self.resultLabel = tk.Label(self, text="IP address", width=15)
        self.resultLabel.grid(row=0, column=0, sticky="E",
                              padx=10, pady=5, columnspan=1)

        # Get user input of IP address
        self.myEntry = tk.Entry(self, width=40)
        self.myEntry.focus()
        self.myEntry.bind("<Return>", self.returnIP)
        self.myEntry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

        # Press to connect or disconnect
        self.btn_connect = tk.Button(self, text="CONNECT", fg="green",
                                     command=self.returnIP)
        self.btn_connect.grid(row=0, column=3, sticky=tk.W +
                              tk.S+tk.E+tk.N, padx=10, pady=5, columnspan=1)

        # Show running processes
        self.btn_process = tk.Button(self, text="Process running",
                                     command=None, width=30)
        self.btn_process.grid(row=1, column=0, sticky=tk.W+tk.S +
                              tk.E+tk.N, padx=10, pady=5, columnspan=2, rowspan=1)

        # Show running apps
        self.btn_app = tk.Button(self, text="App running",
                                 command=None, width=30)
        self.btn_app.grid(row=1, column=2, sticky=tk.W+tk.S +
                          tk.E+tk.N, padx=10, pady=5, columnspan=2, rowspan=1)

        # Shutdown computer
        self.btn_shutdown = tk.Button(self, text="Shut down",
                                      command=None)
        self.btn_shutdown.grid(
            row=2, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=5, columnspan=2)

        # Take screenshot
        self.btn_screenshot = tk.Button(self, text="Take screenshot",
                                        command=None)
        self.btn_screenshot.grid(
            row=2, column=2, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=5, columnspan=2)

        # Get keystroke
        self.btn_keystroke = tk.Button(self, text="Get keystroke",
                                       command=None)
        self.btn_keystroke.grid(
            row=3, column=0, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=5, columnspan=2)

        # Change registry
        self.btn_registry = tk.Button(self, text="Change registry",
                                      command=None)
        self.btn_registry.grid(
            row=3, column=2, sticky=tk.W+tk.S+tk.E+tk.N, padx=10, pady=5, columnspan=2)

        # Exit program
        self.btn_quit = tk.Button(self, text="EXIT", fg="red",
                                  command=self.master.destroy)
        self.btn_quit.grid(row=4, column=1, sticky=tk.W +
                           tk.S+tk.E+tk.N, padx=10, pady=5, columnspan=2)

    def returnIP(self, args=None):
        print(args)
        result = self.myEntry.get()
        self.resultLabel.config(text=result)
        self.myEntry.delete(0, tk.END)
