# -*- coding: UTF-8 -*-

import b64
import threading
import websocket
import gevent
import logging
import logging.handlers
import time
import traceback
import os
import requests
import ctypes
import random
import random
import threading

_running_inst = []


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

logger = get_logger()
conn = []


class test:

    def run(self, tid):

        t_server = self.reg_to_name_server(tid)
        print t_server
        if t_server:
            ws = websocket.WebSocketApp("ws://" + t_server + "/server",
                                            on_message=self.on_message,
                                            on_error=self.on_error,
                                            on_close=self.on_close,
                                            )
            self.ws = ws
            self.tid = tid
            ws.on_open = self.on_open
            ws.run_forever()
            return ws
        return None
    pass

    def close(self):
        self.ws.close()
    pass

    def on_message(self,ws, message):
        logger.info(message)
    pass


    def on_error(self,ws, error):
        # print error
        logger.error(traceback.format_exc())
    pass


    def on_close(self,ws):
        # print "### closed ###"
        logger.info('##### Conection closed ######')
        print 'conn closed tid:' + str(self.tid)
        global __conn
        __conn = 0
        #self.run(self.tid)


    pass


    def on_ping(self,ws):
        ws.send(b64.json_to_b64({'tid': '123'}))


    def on_open(self,ws):
        logger.info("##### Connection open #####")
        print "open"
        ws.send(b64.json_to_b64({'cmd': 'reg', 'tid': self.tid, 'wid': 'w0', 'cid': 'c0', 'param': {"os": os.name}}))
        print 'ws connected tid:' + str(self.tid)


        def hb(self,websocket):
            while 1:
                print 'sending hb'
                try:
                    websocket.send(b64.json_to_b64({'cmd': 'hb', 'tid': self.tid, 'wid': 'w0', 'cid': 'c0', 'param': ''}))
                    gevent.sleep(30)
                except:
                    break

        pass
        #t = threading.Thread(target=hb, args=(self, ws))
        #t.start()

        #_g_group.add(gevent.spawn(hb, self, ws))


    pass



    def reg_to_name_server(self,tid):
        name_server = 'http://192.168.232.128:8088'
        # get t_server ip_port from name_server
        ip_port = None
        try:
            os_name = os.name
            logger.info('request to name_server with name_server: %s, tid: %s, os_name: %s ' % (name_server, tid, os_name))

            if os_name == 'posix':
                libc = ctypes.cdll.LoadLibrary('libc.so.6')
                res_init = libc.__res_init
                res_init()

            response = requests.post(name_server + '/terminal_reg', json={'tid': tid, 'os': os_name}, timeout=6)

            if response.status_code == 200:
                logger.info('request to name_server resp:' + response.content)
                result = response.json()
                if result['result']:
                    ip_port = result['ip_port']
            else:
                logger.error('request to name_server error, response code: ' + response.status_code)
        except Exception as ex:
            logger.error('request to name_server error')
            logger.error(ex)
        pass
        return ip_port


pass

def kick_loop():
    while 1:
        gevent.sleep(1)
        list = random.sample(_running_inst,20)
        print 'going to kick %s'%list
        for inst in list:
            tid = inst.tid
            if tid:
                print 'reconnect tid: '+str(tid)
                inst.close()
pass





if __name__ == "__main__":
    websocket.enableTrace(True)

    for i in range(1,1000):
        inst = test()
        #g = gevent.spawn_later(rn.random()*60, inst.run, i)
        t = threading.Thread(target=inst.run, args=(i,))
        t.start()
        _running_inst.append(inst)
        time.sleep(0.1)
    pass
    #_g_group.add(gevent.spawn_later(60, kick_loop))

pass

