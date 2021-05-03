import os

class Process:
    def __init__(self, sock):
        self.client = sock
        pass

    def run(self):
        while True:
            cmd = self.client.recv(512).decode('utf8')
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
        output = os.popen('wmic process get name, processid, threadcount').read()
        self.process_list = output.split('\n\n')[1:]
        self.client.sendall(bytes(output, "utf8"))
        pass

    def process_kill(self, pid):
        pid = int(pid)
        try:
            os.kill(pid, 9) #9 = signal.SIGTERM
        except OSError:
            print('send loi qua ben client nha nhe')

    def process_start(self, pname):
        pname += ".exe"
        os.popen(pname)


