# -*- coding: utf-8 -*

import tornado.escape
from tornado import ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.gen
import time
import json
import tornado.httpclient
from tornado.concurrent import Future
import zlib
import base64
import os
import tornado.httpserver
from tornado import httpclient
from tornado import gen
from tornado import ioloop
import logging
import logging.handlers

# connected t server <serv_name,ip_port>
connected_t_server = {}
# connected t server <serv_name,internal_ip_port>
connected_t_server_internal = {}
# connect counter <server_name, connected_terminal_count>
connected_counter ={}
# terminal connected to which t server <tid,serv_name>
terminal_t_serv_map = {}
# terminal os name
terminal_os = {}
# terminal version
terminal_version = {}

web_server = ''

settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'template_path': os.path.join(os.path.dirname(__file__), "templates")
}

def get_logger():
    if not os.path.exists('log/'):
        os.makedirs('log')
    _logger = logging.getLogger('ws_job')
    log_format = '%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)
    logfile = 'log/name_server.log'
    rotate_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024, backupCount=5)
    rotate_handler.setFormatter(formatter)
    _logger.addHandler(rotate_handler)
    _logger.setLevel(logging.DEBUG)
    return _logger


pass

logger = get_logger()



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/t_server_reg", TServerRegController),
                    (r"/terminal_reg", TerminalRegController),
                    (r"/web_server_reg", WebServerController),
                    (r"/get_conn_t", GetConnectedTController),
                    (r"/get_t_server", GetTServerController),
                    (r"/kickaway", KickAwayController)]
        tornado.web.Application.__init__(self, handlers, **settings)

    pass


pass


class TServerRegController(tornado.web.RequestHandler):
    """
    @api {post} /t_server_reg/ t_server_reg
    @apiGroup NameServer
    @apiName Terminal Server Register
    @apiDescription Terminal_server 需要在启动时会使用这个api注册，NameServer会随机分配注册过得Terminal_Server给来注册的终端
    @apiParam {String} server_name Each terminal server should had an unique server name, register this server name with ip/port in this api
    @apiParam {String} ip_port Each ip and port of the registered server 
    @apiParam {String} inter_ip_port Each internal ip and port of the registered server 

    @apiSuccess {Boolean} result true or false 

    @apiExample {curl} ExampleUsage:
        curl -v http://119.29.181.180:8088/t_server_reg -H "Content-Type: application/json" -X Post -d '{"server_name":"t_server_1","ip_port":"119.29.181.180:8089"}'
    """

    # terminal server register
    def post(self, *args, **kwargs):
        body = json.loads(self.request.body)
        logger.info('terminal reg %s'% body)
        server_name = body['server_name']
        ip_port = body['ip_port']
        inter_ip_port = body['inter_ip_port']
        logger.info('t_server reg')
        logger.info(server_name)
        logger.info(ip_port)
        logger.info(inter_ip_port)

        connected_t_server[server_name] = ip_port
        connected_t_server_internal[server_name] = inter_ip_port

        #从termianl_t_serv_map里面删除以前这台t_server的映射关系，避免每一个新连接都会来个remove请求
        tid_to_remove = []
        for tid, t_serv in terminal_t_serv_map.iteritems():
            if t_serv == server_name:
                tid_to_remove.append(tid)
        pass

        for tid in tid_to_remove:
            del terminal_t_serv_map[tid]
        pass

        logger.info('avaliable connected_t_server %s' % json.dumps(connected_t_server))
        self.write(json.dumps({'result': True}))

    pass


pass


class KickAwayController(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        tid = json.loads(self.request.body)['tid']
        if tid in terminal_t_serv_map.keys():
            del terminal_t_serv_map[tid]
        if tid in terminal_os.keys():
            del terminal_os[tid]


class TerminalRegController(tornado.web.RequestHandler):
    """
    @api {post} /terminal_reg/ terminal_reg
    @apiGroup NameServer
    @apiName Terminal Client Register
    @apiDescription 终端连接时需要先请求这个接口注册，返回终端websocket连接的terminal server 

    @apiParam {String} tid terminal id of the terminal client

    @apiSuccess {Boolean} result true or false 
    @apiSuccess {String} msg message
    @apiSuccess {String} ip_port The IP:port of the terminal server. The client should connect to the return t_server

    @apiExample {curl} ExampleUsage:
        curl -v http://119.29.181.180:8088/terminal_reg/ -H "Content-Type: application/json" -X Post -d '{"tid":"518067N123", "os":"posix/winnt", "version": "1.5.0"}'
    """

    # terminal register
    @gen.coroutine
    def post(self, *args, **kwargs):
        body = json.loads(self.request.body)
        tid = body['tid']
        os_name = body['os']
        version = None
        if 'version' in body.keys():
            version = body['version']

        if not tid:
            self.write(json.dumps({'result': False, 'msg': 'unknown tid'}))
            return

        # randomly pick a registered t server
        logger.info('Terminal reg avaliable connected_t_server %s' % json.dumps(connected_t_server))
        # 如果本来这台终端已经连接上了某台t_server，还要通知这台t_server踢掉这台终端，再重新连
        if tid in terminal_t_serv_map.keys():
            ori_t_server = terminal_t_serv_map[tid]
            inter_ip_port = connected_t_server_internal[ori_t_server]
            try:
                http_c = httpclient.AsyncHTTPClient()
                headers = {'Content-Type': 'application/json; charset=UTF-8'}
                yield http_c.fetch('http://' + inter_ip_port + '/remove_terminal', body=json.dumps({'tid': tid}),
                             method='POST', headers=headers, request_timeout=2)
            except Exception as ex:
                logger.error('requests %s remove_terminal exception: %s'% (inter_ip_port, ex))
                pass

        pass

        #选择连接terminal少的t_server
        if len(connected_counter.keys())==0:
            #没有可用t_server
            self.write(
                json.dumps({'result': False, 'msg': 'can not get a terminalserver'}))
            return
        pass
        target_t_serv = min(connected_counter, key=connected_counter.get)
        terminal_t_serv_map[tid] = target_t_serv
        terminal_os[tid] = os_name
        if version:
            terminal_version[tid] = version

        self.write(
            json.dumps({'result': True, 'msg': 'get a terminals erver', 'ip_port': connected_t_server[target_t_serv]}))

    pass


pass


class WebServerController(tornado.web.RequestHandler):
    """
    @api {post} /web_server_reg/ web_server_reg
    @apiGroup NameServer
    @apiName Web Server Register
    @apiDescription web server需要再启动时调用此api
    @apiParam {String} ip_port IP:Port of the web server 

    @apiSuccess {Boolean} result true or false 
    @apiSuccess {String} msg message
    @apiSuccess {String} ip_port The IP:port of the terminal server. The client should connect to the return t_server

    @apiExample {curl} ExampleUsage:
        curl -v http://119.29.181.180:8088/terminal_reg/ -H "Content-Type: application/json" -X Post -d '{"tid":"518067N123"}'
    """

    # register web server
    def post(self, *args, **kwargs):
        web_server = json.loads(self.request.body)['ip_port']
        self.write(json.dumps({'result': True, 'msg': 'reg web server'}))

    pass


pass


class GetTServerController(tornado.web.RequestHandler):
    """
    @api {get} /get_t_server/ get_t_server
    @apiGroup NameServer
    @apiName Get Terminal Server by terminal id
    @apiDescription Web Server下发命令时调用此接口获取Terminal Client连接到哪一台Terminal Server

    @apiParam {String} tid terminal id 

    @apiSuccess {Boolean} result true or false 
    @apiSuccess {String} msg message
    @apiSuccess {String} ip_port The IP:port of the terminal server.

    @apiExample {curl} ExampleUsage:
        curl -v http://119.29.181.180:8088/get_t_server?tid=518067N123'
    """

    def get(self, *args, **kwargs):
        tid = self.get_argument('tid')
        if (tid not in terminal_t_serv_map.keys()):
            self.write(json.dumps({'result': False, 'msg': 'this terminal is not connected'}))
            return

        t_server = terminal_t_serv_map[tid]
        ip_port = connected_t_server[t_server]
        self.write(json.dumps({'result': True, 'ip_port': ip_port}))

    pass


pass


class GetConnectedTController(tornado.web.RequestHandler):
    """
    @api {get} /get_conn_t/ get_conn_t
    @apiGroup NameServer
    @apiName get connected terminal
    @apiDescription 获取所有 连接到上了的终端

    @apiSuccess {Boolean} result true or false 
    @apiSuccess {List} list list of tid

    @apiExample {curl} ExampleUsage:
        curl -v http://119.29.181.180:8088/get_conn_t?tid=518067N123'
    """

    def get(self, *args, **kwargs):
        self.write(json.dumps({'result': True, 'list': terminal_os}))

    pass


pass

@gen.coroutine
def check_t_server():
    for t_serv, ip in connected_t_server_internal.iteritems():
        try:
            http_c = httpclient.AsyncHTTPClient()

            r = yield http_c.fetch('http://'+ip+ "/check", request_timeout=1)
            logger.info('call check to %s'% t_serv)
            if r.code == 200:
                result = json.loads(r.body)
                if result['result']:
                    count = result['param']['connected_count']
                    connected_counter[t_serv] = count
            else:
                #not alive
                del connected_t_server_internal[t_serv]
                del connected_t_server[t_serv]
                del connected_counter[t_serv]
            pass
        except Exception as ex:
            logger.error(ex)
    pass
pass


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8088)
    #    http_server=tornado.httpserver.HTTPServer(app)
    #    http_server.bind(8081,'0.0.0.0')
    #    http_server.start(num_processes=0)
    logger.info('Name Server Start listening')
    ioloop.PeriodicCallback(check_t_server,30000).start()
    tornado.ioloop.IOLoop.instance().start()
