import json
import subprocess
import base64
import datetime,time
import re
import threading
import Queue


class CmdHandler:
    def __init__(self,*args, **kwds):
        self.cmd_proc = subprocess.Popen("cmd.exe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
        self._result_queue = Queue.Queue() 
        self.evt = threading.Event()
    pass
    
    def start_loop(self):
        stdout_loop = threading.Thread(target=self._stdout_loop)
        stderr_loop = threading.Thread(target=self._stderr_loop)
        stdout_loop.start()
        stderr_loop.start()
    pass
    
    def handle(self, ws, tid, wid, cmd, cid, param):
        self.cmd_proc.stdin.write(param+'\r\n')
        #output a echo $$endl$$ ,when stdout reads $$endl$$ indicate that this command is finished
        self.cmd_proc.stdin.write('echo $$endl$$\r\n')
        #max wait 180 sec for a command 
        self.evt.wait(180)

        msg=''
        #get all stdout stderr in queue
        while not self._result_queue.empty():
            temp = self._result_queue.get()
            msg = msg + temp
        print "cmd reslut msg:"+ msg.decode('gbk')
        return ('cmd_resp',msg.decode('gbk'))
    pass
    
    def _stdout_loop(self):
        while 1:
            o = self.cmd_proc.stdout.readline()
            o = o.replace('<DIR>','DIR')
            print "output_loop new line read:"+o.decode('gbk') 
            if 'echo $$endl$$' in o:
                print "outputloop endl occured"
                self.evt.set()
                self.evt.clear()
            elif o == '$$endl$$\r\n':
                #skip
                pass
            else:
                self._result_queue.put(o)
            pass
    pass

    
    def _stderr_loop(self):
        while 1:
            o = self.cmd_proc.stderr.readline()
            self._result_queue.put(o)
        pass
    pass
pass
    