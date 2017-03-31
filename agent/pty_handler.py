# -*- coding: UTF-8 -*-
import random
import string
import struct
import termios
import os
import pty
import fcntl
import io
import signal
import threading
import b64
import pwd
import select
import websocket
import time
import base64
import logging
import logging.handlers

# from gevent.monkey import patch_all

# patch_all()
def get_logger():
    _logger = logging.getLogger('ws_job')
    log_format = '%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)
    logfile = 'log/ws.log'
    rotate_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024, backupCount=5)
    rotate_handler.setFormatter(formatter)
    _logger.addHandler(rotate_handler)
    _logger.setLevel(logging.DEBUG)
    return _logger


pass

LOG_DIR = os.path.join(os.path.dirname(__file__), 'log').replace('\\', '/')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
logger = get_logger()


class PtyHandler:
    def __init__(self):
        self.uid = ''.join(
            random.choice(
                string.ascii_lowercase + string.ascii_uppercase +
                string.digits)
            for _ in range(4))
        logging.info("ptyHandler.init")

        self.ws = None
        self.tid = None
        self.cid = None
        self._pty_dict = {}

    pass

    # fork a new pty for every session_id
    def _lazy_init_by_session_id(self, session_id, host, ori_ws, cid, tid):

        pid, fd = None, None

        if session_id not in self._pty_dict.keys() or self._pty_dict[session_id].closed:
            pid, fd = pty.fork()

        logging.info('pty.fork result:')
        logging.info('pid:%s,fd:%s' % (pid, fd))
        if pid == 0:
            #child process
            self.shell()
        else:
            #origin process
            fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
            writer = io.open(
                fd,
                'wt',
                encoding='utf-8',
                closefd=False
            )
            reader = io.open(
                fd,
                'rb',
                buffering=0,
                closefd=False
            )
            # self.communicate()

            logging.info('new pty ws connect to session_id: '+ session_id)
            ws = websocket.WebSocketApp("ws://" +host + "/pty_ws",
                                            on_message=self.on_message,
                                            on_error=self.on_error,
                                            on_close=self.on_close,
                                            )
            ws.session_id = session_id
            stdout_loop = threading.Thread(target=self.read_loop, args=(session_id,))
            self._pty_dict[session_id] = pty_struct(session_id, fd, pid, writer, reader, stdout_loop, ws, ori_ws, cid, tid)

            ws.on_open = self.on_open
            ws_loop = threading.Thread(target=ws.run_forever)
            ws_loop.start()
        pass

    pass

    def on_error(self, ws, error):
        logging.info('on_error, sid: '+ ws.session_id)
        logging.info(error)
        self.on_close(ws)
    pass

    def on_open(self, ws):
        logging.info(time.time())
        logging.info('on_open, sid: '+ ws.session_id)
        ws.send('c'+ws.session_id)
        pty = self._pty_dict[ws.session_id]
        pty.ori_ws.send(b64.json_to_b64(
            {'cmd': 'open_pty_resp', 'tid': pty.tid, 'wid': "w1", 'cid': pty.cid, 'param':True}))
    pass

    def on_message(self, ws, msg):
        logging.info('on_message '+msg)
        cmd = msg[0]

        pty = self._pty_dict[ws.session_id]
        fd, writer = pty.fd, pty.writer
        #input from web
        if cmd == 'i':
            logging.info('w %r' % msg)
            # log.debug('WRIT<%r' % message)
            writer.write(unicode(msg[1:]))
            writer.flush()

        #resize from web
        elif cmd == 's':
            cols, rows = map(int, tuple(msg[1:].split(',')))
            logging.info('resize %s,%s' % (cols, rows))
            s = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(fd, termios.TIOCSWINSZ, s)
            logging.info('SIZE (%d, %d)' % (cols, rows))

        elif cmd == 'w': #web client connected
            #等webclient都连上了 才开始真正工作
            pty.read_loop.start()
        pass

    pass

    def shell(self):

        logging.info('go into shell()')
        # try:
        #    os.chdir(self.path or self.callee.dir)
        # except Exception:
        #    logging.info("Can't chdir to %s" % (self.path or self.callee.dir)

        try:
            logging.info("tty = os.ttyname.replace")
            tty = os.ttyname(0).replace('/dev/', '')
        except Exception:
            logging.info("Can't get ttyname")

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

    def read_loop(self, session_id):

        #time.sleep(3)
        logging.info('read loop start')
        pty = self._pty_dict[session_id]
        fd, closed, reader, ws = (pty.fd, pty.closed, pty.reader, pty.ws)

        while not closed:
            try:
                select.select([fd], [], [])
                r = reader.read()

                # send via websocket
                logging.info(' pty read >%s' % r)
                if ws:
                    ws.send('p'+base64.b64encode(r))
                else:
                    logging.info("no ws")
                pass
            except Exception as e:
                logging.info('pty read error')
                logging.info(e)
                logging.info('pty read error end_________________________')
                pty = self._pty_dict[session_id]
                pty.closed = True
                self.on_close(pty.ws)

            if session_id not in self._pty_dict.keys():
                break

            pty = self._pty_dict[session_id]
            closed = pty.closed
        pass

    pass



    def handle(self, ws, tid, wid, cmd, cid, param):

        self.tid = tid
        self.cid = cid

        #打开pty
        if cmd == 'open_pty':
            session_id = param['session_id']
            host = param['host']
            logging.info('handle open_pty,sid: %s , host: %s '%(session_id, host))

            #建立连接
            if session_id not in self._pty_dict.keys():
                logging.info('%s not inited, start init read_loop: ' % session_id)
                self._lazy_init_by_session_id(session_id, host, ws, cid, tid)

            pty = self._pty_dict[session_id]
            fd, writer = pty.fd, pty.writer
        elif cmd == 'close_pty':
            session_id = param
            logging.info('handle close_pty for sid :'+ session_id)
            pty = self._pty_dict[session_id]

            if pty:
                self.on_close(pty.ws)

        return 'pty_resp', None

    pass

    def on_close(self, ws):
        logging.info('agent pty ws close, sid: '+ ws.session_id)

        session_id = ws.session_id
        if session_id not in self._pty_dict.keys():
            return

        pty = self._pty_dict[session_id]
        closed, fd, pid, read_loop, ws= pty.closed, pty.fd, pty.pid, pty.read_loop, pty.ws

        try:
            #send close to web server
            ws.send('e')
        except:
            pass

        if closed:
            return
        pty.closed = True
        #close the ws
        pty.ws.close()

        if fd is not None:
            logging.info('Closing fd %d' % fd)

        if pid == 0:
            logging.info('pid is 0')
            return

        try:
            os.close(fd)
        except Exception:
            logging.info('closing fd fail')

        try:
            os.kill(pid, signal.SIGHUP)
            os.kill(pid, signal.SIGCONT)
            os.waitpid(pid, 0)
        except Exception:
            logging.info('waitpid fail')


pass


class pty_struct:
    closed = None
    session_id = None
    fd = None
    pid = None
    writer = None
    reader = None
    read_loop = None
    ws = None
    cid = None
    ori_ws = None
    tid = None

    def __init__(self, session_id, fd, pid, writer, reader, read_loop, ws, ori_ws, cid, tid):
        self.read_loop = read_loop
        self.reader = reader
        self.writer = writer
        self.pid = pid
        self.fd = fd
        self.session_id = session_id
        self.closed = False
        self.ws = ws
        self.ori_ws = ori_ws
        self.cid = cid
        self.tid = tid

    pass


pass



if __name__ == '__main__':
    pty = PtyHandler()
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', unicode('p'))
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', unicode('p'))
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', u'p')
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', u'p')
    pty.handle(None, '518067N999', 'w123', 'pty_input', 'c0', u'p')
    logging.info('all end')
