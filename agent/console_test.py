import subprocess
import threading
import time
import os

class CmdHandler:
    def __init__(self, *args, **kwds):
        self.cmd_proc = subprocess.Popen('powershell', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         stdin=subprocess.PIPE)
        self.src = None

    pass

    def start_loop(self):
        stdout_loop = threading.Thread(target=self._stdout_loop)
        stderr_loop = threading.Thread(target=self._stderr_loop)
        stdout_loop.start()
        stderr_loop.start()

    pass

    def handle(self, param):
        print 'stdinput:'
        print param
        self.cmd_proc.stdin.write(param + '\r\n')
    pass

    def _stdout_loop(self):
        while 1:
            o = self.cmd_proc.stdout.readline()
            o = o.replace('<DIR>', 'DIR')

            print "output_loop new line read:" + o.decode('gbk')
    pass

    def _stderr_loop(self):
        while 1:
            o = self.cmd_proc.stderr.readline()
            o = o.replace('<DIR>', 'DIR')

            print "err_loop new line read:" + o.decode('gbk')

        pass

    pass


pass

if __name__ == "__main__":
    cmd_handler = CmdHandler()
    cmd_handler.start_loop()
    cmd_handler.handle('dir')
    cmd_handler.handle('cd ..')
    cmd_handler.handle('dir')
    time.sleep(5)
    
    cmd_handler.handle('python -u')
    cmd_handler.handle('import os')
    cmd_handler.handle('dir = os.listdir(".")')
    cmd_handler.handle('print dir')
    cmd_handler.handle('f = open("test_111.txt","w")')
    cmd_handler.handle('f.write("testtesttest")')
    cmd_handler.handle('exit')
    raw_input("end")
    
