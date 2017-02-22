import random
import string
import os
import pty
import fcntl
import io
import signal
import threading
import b64
import tornado
import tornado.options
import tornado.process
import tornado.web
import tornado.websocket
from tornado import ioloop
import pwd
import select

# from gevent.monkey import patch_all

# patch_all()

ioloop = tornado.ioloop.IOLoop.instance()


class PtyHandler:
    def __init__(self):
        self.uid = ''.join(
            random.choice(
                string.ascii_lowercase + string.ascii_uppercase +
                string.digits)
            for _ in range(4))
        self.pid, self.fd = pty.fork()

        self.closed = False
        self.ws = None
        self.tid = None
        self.wid = None
        self.cid = None

        print 'pty.fork result:'
        print 'pid:%s,fd:%s' % (self.pid, self.fd)
        if self.pid == 0:
            self.shell()
        else:
            fcntl.fcntl(self.fd, fcntl.F_SETFL, os.O_NONBLOCK)
            self.writer = io.open(
                self.fd,
                'wt',
                encoding='utf-8',
                closefd=False
            )
            self.reader = io.open(
                self.fd,
                'rb',
                buffering=0,
                closefd=False
            )
            #self.communicate()
            stdout_loop = threading.Thread(target=self.read_loop)
            stdout_loop.start()
        pass

    pass

    def shell(self):

        print 'go into shell()'
        # try:
        #    os.chdir(self.path or self.callee.dir)
        # except Exception:
        #    print "Can't chdir to %s" % (self.path or self.callee.dir)

        try:
            print "tty = os.ttyname.replace"
            tty = os.ttyname(0).replace('/dev/', '')
        except Exception:
            print "Can't get ttyname"

        # Unsecure connection with su

        if os.path.exists('/usr/bin/su'):
            args = ['/usr/bin/su']
        else:
            args = ['/bin/su']

        pw = pwd.getpwuid(os.getuid())
        shell = pw.pw_shell
        shell_args = [shell, '-il']
        os.execvp(shell_args[0], shell_args)

    pass

    def read_loop(self):

        print 'read'
        while not self.closed:
            try:
                select.select([self.fd],[],[])
                r = self.reader.read()

                # send via websocket
                print ' pty read >%s' % r
                if self.ws:
                    self.ws.send(b64.json_to_b64(
                        {'cmd': 'pty_resp', 'tid': self.tid, 'wid': self.wid, 'cid': self.cid, 'param': r}))
                pass
            except Exception as e:
                print 'pty read error'
                print e
        pass

    pass


    def handle(self, ws, tid, wid, cmd, cid, param):
        self.ws = ws
        self.tid = tid
        self.wid = wid
        self.cid = cid
        if not hasattr(self, 'writer'):
            self.on_close()
            self.close()

        if cmd == 'pty_resize':
            cols, rows = map(int, [param['columns'], param['rows']])
            print 'resize %s,%s' % (cols,rows)
            s = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(self.fd, termios.TIOCSWINSZ, s)
            print 'SIZE (%d, %d)' % (cols, rows)

        elif cmd == 'pty_input':
            print 'w %r' % param
            # log.debug('WRIT<%r' % message)
            self.writer.write(param)
            self.writer.flush()

        return 'pty_resp', None

    pass

    def close(self):
        if self.closed:
            return
        self.closed = True
        if self.fd is not None:
            print 'Closing fd %d' % self.fd

        if getattr(self, 'pid', 0) == 0:
            print 'pid is 0'
            return

        try:
            os.close(self.fd)
        except Exception:
            print 'closing fd fail'

        try:
            os.kill(self.pid, signal.SIGHUP)
            os.kill(self.pid, signal.SIGCONT)
            os.waitpid(self.pid, 0)
        except Exception:
            print 'waitpid fail'


pass

if __name__ == '__main__':
    pty = PtyHandler()
    ioloop.start()
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', unicode('p'))
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', unicode('p'))
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', u'p')
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', u'p')
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', u'p')
    print 'all end'
