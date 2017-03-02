import json
import subprocess
import base64
import datetime, time
import re
import threading
import Queue
import b64
import os
import signal

class CmdHandler:
    def __init__(self, *args, **kwds):
        self.cmd_proc = subprocess.Popen("cmd.exe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         stdin=subprocess.PIPE)
        self.src = None
        self.stdout_loop = None
        self.stderr_loop = None

    pass

    def restart_cmd(self, ws, tid, wid, cmd, cid, param):
        self.stdout_loop.stopped = True
        self.stderr_loop.stopped = True
        #os.kill(self.cmd_proc.pid,9)
        os.system("taskkill /F /T /PID %s"%self.cmd_proc.pid)
        self.cmd_proc = subprocess.Popen("cmd.exe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        self.start_loop()
        return ('','')

    def start_loop(self):
        self.stdout_loop = threading.Thread(target=self._stdout_loop)
        self.stderr_loop = threading.Thread(target=self._stderr_loop)
        self.stdout_loop.start()
        self.stderr_loop.start()

    pass

    def handle(self, ws, tid, wid, cmd, cid, param):
        print 'stdinput:'
        print param
        self.cmd_proc.stdin.write(param + '\r\n')
        # max wait 180 sec for a command
        self.src = (ws, tid, wid, cmd, cid)

        '''msg = ''
        #get all stdout stderr in queue
        while not self._result_queue.empty():
            temp = self._result_queue.get()
            msg = msg + temp
        print "cmd reslut msg:"+ msg.decode('gbk')
        return ('cmd_resp',msg.decode('gbk'))'''
        return ('cmd_resp','')
    pass

    def _stdout_loop(self):
        while 1:
            o = self.cmd_proc.stdout.readline()
            o = o.replace('<DIR>', 'DIR')
            print "output_loop new line read:" + o.decode('gbk')

            if self.src is not None:
                (ws, tid, wid, cmd, cid) = self.src
                ws.send(b64.json_to_b64(
                    {'cmd': 'cmd_resp', 'tid': tid, 'wid': wid, 'cid': cid, 'param': o.decode('gbk')}))
            pass

    pass

    def _stderr_loop(self):
        while 1:
            o = self.cmd_proc.stderr.readline()
            o = o.replace('<DIR>', 'DIR')

            print "err_loop new line read:" + o.decode('gbk')

            if self.src is not None:
                (ws, tid, wid, cmd, cid) = self.src
                ws.send(b64.json_to_b64(
                    {'cmd': 'cmd_resp', 'tid': tid, 'wid': wid, 'cid': cid, 'param': o.decode('gbk')}))
            pass

        pass

    pass


pass
