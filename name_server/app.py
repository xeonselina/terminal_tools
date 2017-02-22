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
import grequests
import tornado.httpserver
import random

#connected t server <serv_name,ip_port>
connected_t_server={}

#connected t server <serv_name,internal_ip_port>
connected_t_server_internal={}
#terminal connected to which t server <tid,serv_name>
terminal_t_serv_map={}
#terminal os name
terminal_os={}

web_server=''

settings={
    'debug':True,
    'static_path':os.path.join(os.path.dirname(__file__), "static"),
    'template_path':os.path.join(os.path.dirname(__file__), "templates")
}

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [(r"/t_server_reg", TServerRegController),
                    (r"/terminal_reg", TerminalRegController),
                    (r"/web_server_reg", WebServerController),
                    (r"/get_conn_t", GetConnectedTController),
                    (r"/get_t_server",GetTServerController),
                    (r"/kickaway",KickAwayController)]
        tornado.web.Application.__init__(self, handlers,**settings)
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
    #terminal server register
    def post(self ,*args, **kwargs):
        body = json.loads(self.request.body)
        print body
        server_name = body['server_name']
        ip_port =  body['ip_port']
        inter_ip_port =  body['inter_ip_port']
        print 't_server reg'
        print server_name
        print ip_port
        print inter_ip_port

        connected_t_server[server_name] = ip_port
        connected_t_server_internal[server_name] = inter_ip_port
        print 'avaliable connected_t_server %s'% json.dumps(connected_t_server)
        self.write(json.dumps({'result':True}))
    pass
pass

class KickAwayController(tornado.web.RequestHandler):
    def post(self, *args,**kwargs):
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
        curl -v http://119.29.181.180:8088/terminal_reg/ -H "Content-Type: application/json" -X Post -d '{"tid":"518067N123"}'
    """
    #terminal register
    def post(self, *args,**kwargs):
        body = json.loads(self.request.body)
        tid = body['tid']
        os_name = body['os']
        if not tid:
            self.write(json.dumps({'result':False,'msg':'unknown tid'}))
            return
        
        #randomly pick a registered t server
        print 'Terminal reg avaliable connected_t_server %s'% json.dumps(connected_t_server)
        #如果本来这台终端已经连接上了某台t_server，还要通知这台t_server踢掉这台终端，再重新连
        if tid in terminal_t_serv_map.keys():
            ori_t_server = terminal_t_serv_map[tid]
            inter_ip_port = connected_t_server_internal[ori_t_server]
            try:
                req = grequests.post('http://'+inter_ip_port+'/remove_terminal',json={'tid':tid})
                job = grequests.send(req,grequests.Pool(1))
            except:
                pass
                
            #time.sleep(3)
        pass
            
        target_t_serv = random.choice(connected_t_server.keys())
        terminal_t_serv_map[tid] = target_t_serv
        terminal_os[tid] = os_name

        self.write(json.dumps({'result':True,'msg':'get a terminals erver', 'ip_port':connected_t_server[target_t_serv]}))
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
    #register web server
    def post(self,*args,**kwargs):
        web_server= json.loads(self.request.body)['ip_port']
        self.write(json.dumps({'result':True,'msg':'reg web server'}))
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
    def get(self,*args,**kwargs):
        tid = self.get_argument('tid')
        if(tid not in terminal_t_serv_map.keys()):
            self.write(json.dumps({'result':False,'msg':'this terminal is not connected'}))
            return

        t_server = terminal_t_serv_map[tid]
        ip_port = connected_t_server[t_server]
        self.write(json.dumps({'result':True,'ip_port':ip_port}))
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
    def get(self,*args,**kwargs):
        self.write(json.dumps({'result':True,'list':terminal_os}))
    pass
pass

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8088)
#    http_server=tornado.httpserver.HTTPServer(app)
#    http_server.bind(8081,'0.0.0.0')
#    http_server.start(num_processes=0)
    print 'Name Server Start listening'
    tornado.ioloop.IOLoop.instance().start()
