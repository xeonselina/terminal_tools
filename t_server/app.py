# -*- coding: utf-8 -*

import tornado.escape
from tornado import ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.gen
import threading
import datetime
import json
import tornado.httpclient
from tornado.concurrent import Future
import zlib
import base64
import os
import requests
import tornado.httpserver
import random
import string
import b64
import copy
from tornado import httpclient, gen
import objgraph
import time
import logging
import logging.handlers

# connected terminal {'518067N123':connection}
connected_terminal = {}

web_server = ''
requests.adapters.DEFAULT_RETRIES = 50

settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'template_path': os.path.join(os.path.dirname(__file__), "templates")
}

config = {}
execfile('app.conf', config)

terminal_hb = {}

def get_logger():
    if not os.path.exists('log/'):
        os.makedirs('log')
    _logger = logging.getLogger('ws_job')
    log_format = '%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)
    logfile = 'log/t_server.log'
    rotate_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024, backupCount=5)
    rotate_handler.setFormatter(formatter)
    _logger.addHandler(rotate_handler)
    _logger.setLevel(logging.DEBUG)
    return _logger


pass

logger = get_logger()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/terminal", TerminalController),
                    (r"/server", ServerController),
                    (r"/remove_terminal", RemoveTerminalController),
                    (r"/check", CheckController),
                    (r"/check_memory",MemoryController)]
        tornado.web.Application.__init__(self, handlers, **settings)

    pass


pass

class MemoryController(tornado.web.RequestHandler):
    def get(self):
        root = objgraph.get_leaking_objects()
        logger.info("len(root)")
        logger.info(len(root))
        logger.info('show_growth')
        logger.info(objgraph.show_growth(20))

        self.write("ok")
pass


class CheckController(tornado.web.RequestHandler):
    '''
    返回连接了多少个终端
    '''
    def get(self):
        self.write(json.dumps({'result': True, 'param': {'connected_count': len(connected_terminal)}}))
    pass
pass

def _scan_offline_loop():
    thread = threading.Thread(
            target=_scan_terminal_offline_, args=(60,))
    # thread.setDaemon(True)
    thread.start()
pass

@gen.coroutine
def _scan_terminal_offline_(interval):
    while 1:
        try:
            time.sleep(interval)
            logger.info('start check hb')
            dict_hb = copy.copy(terminal_hb)

            for tid, hb_time in dict_hb.iteritems():

                current_time = datetime.datetime.now()
                if (current_time - hb_time).seconds >= 300:
                    logger.info('%s hb out of time'%tid)
                    http_c = httpclient.AsyncHTTPClient()
                    headers = {'Content-Type': 'application/json; charset=UTF-8'}
                    http_c.fetch('http://' + config['name_server'] + '/kickaway', body=json.dumps({'tid': tid}),
                                 headers=headers, request_timeout=5, method="POST")


                    if tid in terminal_hb:
                        del terminal_hb[tid]
                    if tid in connected_terminal:
                        try:
                            connected_terminal[tid].close()
                        except Exception as ex:
                            print '_scan_offline_loop() connection close exception: %s'% ex
                            pass
                        del connected_terminal[tid]
                pass
            pass
        except Exception as ex:
            logger.error('scan offline Exception:%s' %ex)
pass

'''
终端连接到服务器，使用websocket
'''


class ServerController(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    pass

    def __init__(self, application, request, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(self, application, request, **kwargs)
        self.tid = -1

    pass

    def open(self):
        #	Nothing to do untill we got the first heartbeat
        logger.info("new client connected")



    pass



    @gen.coroutine
    def on_message(self, message):
        #logger.info('received terminal message: %s' % base64.b64decode(message))
        msg_obj = b64.b64_to_json(message)

        cmd = msg_obj['cmd']

        if cmd == 'reg':
            connected_terminal[msg_obj['tid']] = self
            #注册也当一次心跳
            terminal_hb[msg_obj['tid']] = datetime.datetime.now()
            self.tid = msg_obj['tid']
        pass

        # todo:心跳处理
        if cmd == 'hb':
            #logger.info('hb from tid: %s' % msg_obj['tid'])
            terminal_hb[msg_obj['tid']] = datetime.datetime.now()

        pass

        # 连接到web server
        web_server = config['web_server']
        try:
            #too much log
            #logger.info('on_message message: %s' % message)
            http_c = httpclient.AsyncHTTPClient()
            http_c.fetch("http://" + web_server + "/resp", body=message, method="POST", request_timeout=5)
            self.write_message(b64.json_to_b64({'result': True}))
        except:
            self.write_message(b64.json_to_b64({'result': False, 'msg': 'cant connect to web_server'}))

    pass

    def on_close(self):
        if self.tid in connected_terminal:

            try:
                connected_terminal[self.tid].close()
            except Exception as ex:
                print 'on_close connection close exception: %s'% ex
                pass

            del connected_terminal[self.tid]
            logger.info("close %s" % self.tid)

    pass


pass

'''
web server服务器连接到终端，使用http
'''


class TerminalController(tornado.web.RequestHandler):
    # terminal register
    def post(self, *args, **kwargs):
        body = b64.b64_to_json(self.request.body)
        logger.info('received terminal cmd: %s' % body)
        tid = body['tid']
        wid = body['wid']
        cid = body['cid']
        cmd = body['cmd']

        if tid in connected_terminal:
            terminal = connected_terminal[tid]
            terminal.write_message(self.request.body)
        pass

        self.write(json.dumps({'result': True}))

    pass


pass


class RemoveTerminalController(tornado.web.RequestHandler):
    # remove terminal
    def post(self, *args, **kwargs):
        body = json.loads(self.request.body)
        logger.info('received remove_terminal : %s' % body)
        tid = body['tid']

        if tid in connected_terminal:
            try:
                connected_terminal[tid].close()
            except Exception as ex:
                print 'removeTerminalController connection close exception: %s'% ex
                pass

            del connected_terminal[tid]
        pass

        self.write(json.dumps({'result': True}))

    pass


pass

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    current_ip_port = config['server_instance']
    current_ip_port_inter = config['server_instance_inter']
    current_server_name = config['server_instance_name']
    port = string.split(current_ip_port, ':')[1]
    app.listen(port)
    #    http_server=tornado.httpserver.HTTPServer(app)
    #    http_server.bind(8081,'0.0.0.0')
    #    http_server.start(num_processes=0)
    r = requests.post('http://' + config['name_server'] + '/t_server_reg',
                      json={'server_name': current_server_name, 'ip_port': current_ip_port,
                            'inter_ip_port': current_ip_port_inter}, timeout=5)


    _scan_offline_loop()

    logger.info('Terminal Server Start listening')
    tornado.ioloop.IOLoop.instance().start()
