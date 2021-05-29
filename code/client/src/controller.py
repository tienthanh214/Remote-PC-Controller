import src.views.menu as mnu
import src.views.screenshot as ssh
import src.views.manager as mng
import src.views.keystroke as ksk
import src.views.registry as rgs
import src.views.utilities as utl
import src.mysocket as msk
import tkinter as tk
import time


class Controller():
    def __init__(self, sock=None):
        super().__init__()
        self._root = tk.Tk()
        self._socket = msk.MySocket()
        # Bind event to the Menu window's buttons
        self._menu = mnu.Menu(self._root)
        self._menu.btn_connect["command"] = self.connect
        self._menu.btn_process["command"] = self.manager_prc
        self._menu.btn_app["command"] = self.manager_app
        self._menu.btn_keystroke["command"] = self.keystroke
        self._menu.btn_screenshot["command"] = self.screenshot
        self._menu.btn_registry["command"] = self.registry
        self._menu.btn_shutdown["command"] = self.shutdown
        self._menu.btn_quit["command"] = self.exit_prog
        self._menu.bind("<Destroy>", lambda e: self.exit_prog(isKilled=True))
        self._inputbox = [None] * 2
        self._function = None

    def run(self):
        self._menu.mainloop()

    def exit_prog(self, isKilled=False):
        try:
            self._socket.send("quit", showerror=False)
        except OSError:
            pass
        finally:
            self._socket.close()
            if not isKilled:
                self._root.destroy()

    def connect(self):
        ip = self._menu.etr_ip.get().strip("\n")
        if self._socket._isconnected:
            ans = tk.messagebox.askquestion(
                "New IP address", "Do you want to disconnect to the current server\n and reconnect to this IP ({})?".format(ip), icon="warning")
            if ans == "yes":
                try:
                    self._socket.send("quit")
                finally:
                    self._socket.close()
                    time.sleep(1)
            else:
                utl.messagebox("Client", "New connection cancelled", "error")
                return

        self._socket.connect(ip=ip)
        if self._socket._isconnected:
            utl.messagebox("Client", "Connected to the server", "info")
        else:
            utl.messagebox("Client", "Fail to connect to server", "error")

    # Function 1
    def manager_prc(self):
        self._socket._isconnected = self._socket.send("process")
        if not self._function == None or not self._socket._isconnected:
            return
        self._function = mng.Manager(tk.Toplevel(self._root))
        # bindings...
        self._function.btn_kill["command"] = self.manager_prc_kill
        self._function.btn_view["command"] = self.manager_prc_view
        self._function.btn_start["command"] = self.manager_prc_start
        self._function.bind(
            "<Destroy>", self.exit_func)
        # run window
        self._function.mainloop()

    def manager_prc_kill(self):
        if not self._inputbox[0] == None:
            return
        self._inputbox[0] = utl.inputbox(
            tk.Toplevel(self._function), tl="process", cmd="kill")
        # binding...
        self._inputbox[0].btn_get["command"] = lambda: self.manip_runnin(
            boxid=0, cmd="process", act="kill")
        self._inputbox[0].bind(
            "<Destroy>", lambda e: self.reset_inputbox(boxid=0))
        self._inputbox[0].mainloop()

    def manager_prc_start(self):
        if not self._inputbox[1] == None:
            return
        self._inputbox[1] = utl.inputbox(
            tk.Toplevel(self._function), tl="process", cmd="start")
        # binding...
        self._inputbox[1].btn_get["command"] = lambda: self.manip_runnin(
            boxid=1, cmd="process", act="start")
        self._inputbox[1].bind(
            "<Destroy>", lambda e: self.reset_inputbox(boxid=1))
        self._inputbox[1].mainloop()

    def manager_prc_view(self):
        self._socket._isconnected = self._socket.send("process,view")
        if not self._socket._isconnected:
            return
        list_len = int(self._socket._sock.recv(32).decode('utf8'))
        data = self._socket.receive(length=list_len).decode("utf8")
        self._function.view(data)

    # Function 2
    def manager_app(self):
        self._socket._isconnected = self._socket.send("application")
        if not self._function == None or not self._socket._isconnected:
            return
        self._function = mng.Manager(
            tk.Toplevel(self._root), "application")
        # bindings...
        self._function.btn_kill["command"] = self.manager_app_kill
        self._function.btn_view["command"] = self.manager_app_view
        self._function.btn_start["command"] = self.manager_app_start
        self._function.bind(
            "<Destroy>", self.exit_func)
        # run window
        self._function.mainloop()

    def manager_app_kill(self):
        if not self._inputbox[0] == None:
            return
        self._inputbox[0] = utl.inputbox(tk.Toplevel(
            self._function), tl="application", cmd="kill")
        # binding...
        self._inputbox[0].btn_get["command"] = lambda: self.manip_runnin(
            boxid=0, cmd="application", act="kill")
        self._inputbox[0].bind(
            "<Destroy>", lambda e: self.reset_inputbox(boxid=0))
        self._inputbox[0].mainloop()

    def manager_app_start(self):
        if not self._inputbox[1] == None:
            return
        self._inputbox[1] = utl.inputbox(tk.Toplevel(
            self._function), tl="application", cmd="start")
        # binding...
        self._inputbox[1].btn_get["command"] = lambda: self.manip_runnin(
            boxid=1, cmd="application", act="start")
        self._inputbox[1].bind(
            "<Destroy>", lambda e: self.reset_inputbox(boxid=1))
        self._inputbox[1].mainloop()

    def manager_app_view(self):
        self._socket._isconnected = self._socket.send("application,view")
        if not self._socket._isconnected:
            return
        list_len = int(self._socket._sock.recv(32).decode("utf8"))
        data = self._socket.receive(length=list_len).decode("utf8")
        self._function.view(data)

    def manip_runnin(self, boxid, cmd, act):
        target = self._inputbox[boxid].getvalue()
        self._socket._isconnected = self._socket.send(
            ','.join([cmd, act, target]))
        self._inputbox[boxid].clear()
        if not self._socket._isconnected:
            return
        response = self._socket._sock.recv(32).decode("utf8")
        utl.messagebox(title=cmd, msg=response,
                       type="info" if response == "SUCCESS" else "error")

    # Function 3
    def keystroke(self):
        self._socket._isconnected = self._socket.send("keystroke")
        if not self._function == None or not self._socket._isconnected:
            return
        self._function = ksk.Keystroke(tk.Toplevel(self._root))
        # bindings...
        self._function.btn_hook["command"] = self.keystroke_hook
        self._function.btn_unhook["command"] = self.keystroke_unhook
        self._function.btn_print["command"] = self.keystroke_print
        self._function.btn_clear["command"] = self.keystroke_clear
        self._function.bind(
            "<Destroy>", self.exit_func)
        # run window
        self._function.mainloop()

    def keystroke_hook(self):
        self._socket.send(','.join(["keystroke", "hook"]))

    def keystroke_unhook(self):
        self._socket.send(','.join(["keystroke", "unhook"]))

    def keystroke_print(self):
        self._socket.send("keystroke,print")
        log_len = int(self._socket._sock.recv(32).decode('utf8'))
        data = self._socket.receive(length=log_len).decode("utf8")
        self._function.print_keystroke(data)

    def keystroke_clear(self):
        self._function.text_field.configure(state="normal")
        self._function.text_field.delete("1.0", tk.END)
        self._function.text_field.configure(state="disable")

    # Function 4
    def screenshot(self):
        self._socket._isconnected = self._socket.send("screenshot")
        if not self._function == None or not self._socket._isconnected:
            return
        self._function = ssh.Screenshot(tk.Toplevel(self._root))
        # bindings...
        self._function.btn_snap["command"] = self.screenshot_snap
        self._function.btn_save["command"] = self.screenshot_save
        self._function.bind(
            "<Destroy>", self.exit_func)
        self._function.mainloop()

    def screenshot_snap(self):
        # send
        self._socket.send("screenshot,snap")
        picture_len = int(self._socket._sock.recv(32).decode('utf8'))
        data = self._socket.receive(length=picture_len)
        self._function.update_image(data)

    def screenshot_save(self):
        self._function.save_image()

    # Function 5
    def registry(self):
        self._socket._isconnected = self._socket.send("registry")
        if not self._function == None or not self._socket._isconnected:
            return
        self._function = rgs.Registry(tk.Toplevel(self._root))
        # bindings...
        self._function.btn_browse["command"] = self.registry_browse
        self._function.btn_sendcont["command"] = self.registry_sendcont
        self._function.btn_send["command"] = self.registry_send
        self._function.bind(
            "<Destroy>", self.exit_func)
        self._function.mainloop()

    def registry_browse(self):
        self._function.browse_path()

    def registry_sendcont(self):
        filecont = self._function.txt_regcont.get("1.0", tk.END)
        self._socket._isconnected = self._socket.send(
            ','.join(["registry", "file"]))
        if not self._socket._isconnected:
            return
        self._socket._sock.sendall(bytes(str(len(filecont)), "utf8"))
        time.sleep(0.1)
        self._socket.send(filecont)

        response = self._socket._sock.recv(1024).decode("utf8")
        utl.messagebox("Send regsitry file", response,
                       "info" if response == "SUCCESS" else "error")

    def registry_send(self):
        func = self._function._df_func.get().strip("\n")
        path = self._function.txt_path.get("1.0", tk.END).strip("\n")
        name = self._function.txt_name.get("1.0", tk.END).strip("\n")
        value = self._function.txt_value.get("1.0", tk.END).strip("\n")
        dttp = self._function._df_dttype.get().strip("\n")

        request = None
        if func in ['Get value', 'Set value', 'Create key']:
            func = func.split(" ", 1)[0].lower()
        else:
            func = func.replace(" ", "").lower()
        self._socket._isconnected = self._socket.send(
            ','.join(["registry", func, path, name, value, dttp]))
        if not self._socket._isconnected:
            return
        response = self._socket._sock.recv(1024).decode("utf8")
        self._function.insert_result(response)

    # Function 6
    def shutdown(self):
        self._socket._isconnected = self._socket.send("shutdown")
        self._socket.shutdown()

    # Window utilities methods
    def exit_func(self, event):
        self._socket.send("exit", showerror=False)
        self._function = None

    def reset_inputbox(self, boxid):
        self._inputbox[boxid].killbox()
        self._inputbox[boxid] = None
