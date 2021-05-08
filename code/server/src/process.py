import os

class Process:
    def __init__(self, sock):
        self.client = sock
        pass

    def run(self):
        while True:
            cmd = self.client.recv(32).decode('utf8')
            if cmd == "process,view":
                self.process_view()
            elif cmd == "exit":
                return
            else:
                if len(cmd.split(',')) == 3:
                    cmd, pid = cmd.rsplit(',', 1)
                if cmd == "process,kill":
                    self.process_kill(pid)
                elif cmd == "process,start":
                    self.process_start(pid)
                pass
            pass
        pass

    def process_view(self):
        output = os.popen('powershell "gps |  select name, id, {$_.Threads.Count}').read()
        # self.process_list = output.split('\n\n')[1:]
        self.client.sendall(bytes(str(len(output)), "utf8"))
        self.client.sendall(bytes(output, "utf8"))
        pass

    def process_kill(self, pid):
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

    def process_start(self, pname):
        if len(pname) == 0: return
        pname += ".exe"
        try:
            result = os.popen(pname)
        except Exception:
            self.client.send(bytes("FAIL", "utf8"))
            return
        self.client.send(bytes("SUCCESS", "utf8"))
        

