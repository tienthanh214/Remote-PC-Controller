import os

class Application:
    def __init__(self, sock):
        self.client = sock
        pass

    def run(self):
        while True:
            cmd = self.client.recv(32).decode('utf8')
            if cmd == "application,view":
                self.application_view()
            elif cmd == "exit":
                return
            else:
                if len(cmd.split(',')) == 3:
                    cmd, pid = cmd.rsplit(',', 1)
                if cmd == "application,kill":
                    self.application_kill(pid)
                elif cmd == "application,start":
                    self.application_start(pid)
                pass
            pass
        pass

    def application_view(self):
        output = os.popen('powershell "gps | where {$_.MainWindowTitle } | select name, id, {$_.Threads.Count}').read()
        
        self.client.sendall(bytes(str(len(output)), "utf8"))
        self.client.sendall(bytes(output, "utf8"))
        pass

    def application_kill(self, pid):
        if not pid.isdigit():
            self.client.send(bytes("FAIL", "utf8"))
            return

        pid = int(pid)
        try:
            os.kill(pid, 9) #9 = signal.SIGTERM
        except OSError:
            self.client.send(bytes("FAIL", "utf8"))
            return
        self.client.send(bytes("SUCCESS", "utf8"))


    def application_start(self, pname):
        if len(pname) == 0: return
        pname += ".exe"
        try:
            os.popen(pname)
        except OSError:
            self.client.send(bytes("FAIL", "utf8"))
            return
        self.client.send(bytes("SUCCESS", "utf8"))
        

