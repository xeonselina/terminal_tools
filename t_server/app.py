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
import requests
import string
import b64
import copy

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


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/terminal", TerminalController),
                    (r"/server", ServerController),
                    (r"/remove_terminal", RemoveTerminalController)]
        tornado.web.Application.__init__(self, handlers, **settings)

    pass


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
        print "new client connected"

        event = threading.Event()
        thread = threading.Thread(
            target=self._scan_terminal_offline_, args=(60, event))
        #thread.setDaemon(True)
        thread.start()

    pass

    def _scan_terminal_offline_(self, interval, event):
        while not event.wait(timeout=interval):
            dict_hb = copy.copy(terminal_hb)
            for item in dict_hb:
                hb_time = dict_hb[item]
                current_time = datetime.datetime.now()
                if((current_time-hb_time).seconds>=300):
                    requests.post('http://' + config['name_server'] + '/kickaway',
                                      json={'tid': item})
                    del terminal_hb[item]


    def on_message(self, message):
        print 'received terminal message: %s' % base64.b64decode(message)
        msg_obj = b64.b64_to_json(message)

        cmd = msg_obj['cmd']

        if cmd == 'reg':
            connected_terminal[msg_obj['tid']] = self
            self.tid = msg_obj['tid']
        pass

        # todo:心跳处理
        if cmd == 'hb':
            print 'hb from tid: ' + msg_obj['tid']
            terminal_hb[msg_obj['tid']] = datetime.datetime.now()
        pass

        # 连接到web server
        web_server = config['web_server']
        try:
            requests.post("http://" + web_server + "/resp", message)
            self.write_message(b64.json_to_b64({'result': True}))
        except requests.exceptions.ConnectionError:
            self.write_message(b64.json_to_b64({'result': False, 'msg': 'cant connect to web_server'}))

    pass

    def on_close(self):
        if self.tid in connected_terminal.keys():
            del connected_terminal[self.tid]
            print "close %s" % self.tid

    pass


pass

'''
web server服务器连接到终端，使用http
'''


class TerminalController(tornado.web.RequestHandler):
    # terminal register
    def post(self, *args, **kwargs):
        body = b64.b64_to_json(self.request.body)
        print 'received terminal cmd: %s' % body
        tid = body['tid']
        wid = body['wid']
        cid = body['cid']
        cmd = body['cmd']

        if (tid in connected_terminal):
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
        print 'received remove_terminal : %s' % body
        tid = body['tid']

        if (tid in connected_terminal):
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
                            'inter_ip_port': current_ip_port_inter})

    print 'Terminal Server Start listening'
    tornado.ioloop.IOLoop.instance().start()
