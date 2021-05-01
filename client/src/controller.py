import src.views.menu as menu
import src.views.screenshot as scrsh
import src.views.running as runng
import src.views.keystroke as kystk
import src.views.registry as regis
import src.views.utilities as util
import src.model as mysk
import tkinter as tk


class Application():
    def __init__(self, sock=None):
        super().__init__()
        self._socket = mysk.MySocket()
        # Bind event to the Menu window's buttons
        self._menu = menu.Menu(tk.Tk())
        self._menu.btn_connect.bind("<Button>", self.connect)
        self._menu.btn_process.bind("<Button>", self.running_prc)
        self._menu.btn_app.bind("<Button>", self.running_app)
        self._menu.btn_keystroke.bind("<Button>", self.keystroke)
        self._menu.btn_screenshot.bind("<Button>", self.screenshot)
        self._menu.btn_registry.bind("<Button>", self.registry)
        self._menu.btn_shutdown.bind("<Button>", self.shutdown)

    def run(self):
        self._menu.mainloop()

    def connect(self, event):
        self._socket.connect(ip='localhost', port=54321)

    # 1 no
    def running_prc(self, event):
        self._running_prc = runng.Running(tk.Tk())
        # bindings...
        self._running_prc.btn_kill.bind("<Button>", self.running_prc_kill)
        self._running_prc.btn_view.bind("<Button>", self.running_prc_view)
        self._running_prc.btn_clear.bind("<Button>", self.running_prc_clear)
        self._running_prc.btn_start.bind("<Button>", self.running_prc_start)
        # run window
        self._running_prc.mainloop()

    def running_prc_kill(self, event):
        self._running_prc.manip_runn(action="kill")

    def running_prc_start(self, event):
        self._running_prc.manip_runn()

    def running_prc_clear(self, event):
        self._running_prc.clear()

    def running_prc_view(self, event):
        self._socket.send("process")
        data = self._socket.receive()
        self._running_prc.view(data)

    # 2 no
    def running_app(self, event):
        self._running_app = runng.Running(tk.Tk(), "application")
        # bindings...
        self._running_app.btn_kill.bind("<Button>", self.running_app_kill)
        self._running_app.btn_view.bind("<Button>", self.running_app_view)
        self._running_app.btn_clear.bind("<Button>", self.running_app_clear)
        self._running_app.btn_start.bind("<Button>", self.running_app_start)
        # run window
        self._running_app.mainloop()

    def running_app_kill(self, event):
        self._running_app.manip_runn(action="kill")

    def running_app_start(self, event):
        self._running_app.manip_runn()

    def running_app_clear(self, event):
        self._running_app.clear()

    def running_app_view(self, event):
        self._socket.send("application")
        data = self._socket.receive()
        self._running_app.view(data)

    # 3 yes
    def keystroke(self, event):
        self._keystroke = kystk.Keystroke(tk.Tk())
        # bindings...
        self._keystroke.btn_hook.bind("<Button>", self.keystroke_hook)
        self._keystroke.btn_unhook.bind("<Button>", self.keystroke_unhook)
        self._keystroke.btn_print.bind("<Button>", self.keystroke_print)
        # self._keystroke.btn_clear.bind("<Button>", self.keystroke_clear)
        # run window
        self._keystroke.mainloop()

    def keystroke_hook(self, event):
        self._socket.send("keystroke hook")
        data = self._socket.receive()

    def keystroke_unhook(self, event):
        self._socket.send("keystroke unhook")
        data = self._socket.receive()

    def keystroke_print(self, event):
        self._socket.send("keystroke")
        data = self._socket.receive()
        self._keystroke.print_keystroke(data)

    # 4 yes
    def screenshot(self, event):
        self._screenshot = scrsh.Screenshot(tk.Tk())
        # bindings...
        self._screenshot.btn_snap.bind("<Button>", self.screenshot_snap)
        self._screenshot.btn_save.bind("<Button>", self.screenshot_save)
        self._screenshot.mainloop()

    def screenshot_snap(self, event):
        # send
        self._socket.send("screenshot")
        data = self._socket.receive()
        self._screenshot.update_image(data)

    def screenshot_save(self, event):
        self._screenshot.save_image()

    # 5 no
    def registry(self, event):
        self._registry = regis.Registry(tk.Tk())
        # bindings...
        self._registry.btn_browse.bind("Button", self.registry_browse)
        self._registry.btn_sendcont.bind("Button", self.registry_sendcont)
        self._registry.btn_send.bind("Button", self.registry_send)
        self._registry.btn_clear.bind("Button", self.registry_clear)
        self._registry.mainloop()

    # 6 yes
    def shutdown(self, event):
        self._socket.send("shutdown")
        self._socket.shutdown()
