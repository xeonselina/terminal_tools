# coding=utf-8
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
import os
import requests
import tornado.httpserver
from Connector.DirListHandler import dir_list_handler
import uuid
import name_server
import base64
import t_server
import b64
import urllib
import logging
import subprocess
import mimetypes

MAX_REQUEST = 50

config = {}
execfile('app.conf', config)

connected_web_client = {}

settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    "login_url": "/login"
}


def parse_json_resp(json_message):
    action_type = json_message.get('type')
    result = json_message.get('result')
    resp_id = json_message.get('respID')
    return action_type, result, resp_id


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")


class BaseWsHandler(tornado.websocket.WebSocketHandler):
    def _handle_request_exception(self, e):
        logging.error('error')


# Request Routing
class Application(tornado.web.Application):
    def __init__(self):
        # /term is used for handling terminal req/resp, while /manager is used for request from browser
        handlers = [(r"/resp", TerminalRespController),
                    (r"/", HomeController),
                    (r"/list_log", LogHandler),
                    (r"/list_dir", dir_list_handler),
                    (r"/show_log", Show_logHandler),
                    (r"/oper", Oper_Handler),
                    (r"/web_upload", WebUploadHandler),
                    (r"/file_download", DownloadHandler),
                    (r"/file_view", FileViewHandler),
                    (r"/dir_tree", DirTreeHandler),
                    (r"/uploads/(.*)", tornado.web.StaticFileHandler, {"path": "uploads/"}),
                    (r"/ws", WSHandler),
                    (r"/cli_upload", ClientUploadHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    (r"/auth", AuthHandler)]
        tornado.web.Application.__init__(self, handlers, **settings)


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    pass

    def __init__(self, application, request, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(self, application, request, **kwargs)
        self.wid = -1

    pass

    def open(self):
        #	Nothing to do untill we got the first heartbeat
        print "new client connected"

    pass

    def on_message(self, message):
        print 'received web client message: %s' % base64.b64decode(message)
        msg_obj = b64.b64_to_json(message)

        cmd = msg_obj['cmd']

        if cmd == 'reg':
            connected_web_client[msg_obj['wid']] = self
            print "new webclient connected, all connected_web_client.keys() are:"
            print connected_web_client.keys()

            self.wid = msg_obj['wid']
        pass

    pass

    def on_close(self):
        if self.wid in connected_web_client.keys():
            del connected_web_client[self.wid]
            print "close %s" % self.wid
            print "new webclient connected, all connected_web_client.keys() are:"
            print connected_web_client.keys()

    pass


pass


class ClientUploadHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        tid = self.get_argument('tid')
        cid = self.get_argument('cid')
        wid = self.get_argument('wid')
        # 是否打開文件查看
        is_view = self.get_argument('view')

        fileinfo = self.request.files['zipfile'][0]

        fname = fileinfo['filename']
        print 'received file, filename is %s' % fname
        fn_part = os.path.splitext(fname)
        extn = None
        if len(fn_part) > 1:
            extn = fn_part[1]

        sub_path = str(uuid.uuid4())
        cname = "{0}{1}".format(fn_part[0], extn)

        path_dir = 'uploads/' + sub_path
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        with open(path_dir + '/' + cname, 'w') as fh:
            fh.write(fileinfo['body'])

        print 'config is :'
        print config
        url = 'http://%s/uploads/%s/%s' % (config['web_server'], sub_path, cname)
        print 'download url is: ' + url

        print 'Is wid in connected_web_client:'
        print wid in connected_web_client.keys()

        print "all connected_web_client"
        print connected_web_client.keys()

        if wid in connected_web_client.keys():
            ws = connected_web_client[wid]
            if is_view:
                # unzip
                unzip_path = 'uploads/%s/%s' % (sub_path, 'unzip')
                subprocess.call(['7z', 'x', 'uploads/%s/%s' % (sub_path, cname), '-y', '-o%s' % unzip_path])
                # should be only one file in sub_path/unzip/
                items = os.listdir(unzip_path)
                items = [(os.path.join(unzip_path, t), t) for t in items]
                for long, short in items:
                    print 'try to open file:'
                    print long
                    if os.path.isdir(long):
                        self.write(json.dumps({'result': False, 'msg': '不能打开目录'}))
                        return
                    else:
                        (mtype, _) = mimetypes.guess_type(long)
                        # 文本文件才打开
                        if 'text' in mtype:
                            with open(long) as f:
                                cl = f.readlines()
                                cl = [c + '<br/>' for c in cl]
                                content = ""
                                content = content.join(cl)

                                ws.write_message(
                                    b64.json_to_b64(
                                        {'cmd': 'view', 'param': {'result': True, 'title': short, 'content': content}}))
                                self.write(json.dumps({'result': True}))
                                return
                            pass
                        else:
                            ws.write_message(b64.json_to_b64({'cmd': 'view', 'param': {'result': False}}))
                            self.write(json.dumps({'result': True}))
                            return
                        pass
                    pass
                pass
                ws.write_message(b64.json_to_b64({'cmd': 'download', 'param': url}))
                self.write(json.dumps({'result': True}))
            else:
                # 通知页面可以下载文件了
                ws.write_message(b64.json_to_b64({'cmd': 'download', 'param': url}))
                self.write(json.dumps({'result': True}))
            pass

        self.write(json.dumps({'result': False}))

    pass


pass


class LoginHandler(BaseHandler):
    def get(self):
        # self.render('index.html', connect_total=len(name_server.get_connected_client()))
        host = self.request.headers["host"]
        self.redirect("http://sytest.cimc.com/sso/user/login?ref=http%3a%2f%2f{0}%2fauth".format(urllib.quote(host)))


class LogoutHandler(BaseHandler):
    #    http://sytest.cimc.com/sso/user/logout?ref=http%3A%2F%2Fticket.cimc.com%2Fuser%2Flogout
    def get(self):
        if (self.get_current_user()):
            self.clear_cookie("username")
            host = self.request.headers["host"]
            self.redirect("http://sytest.cimc.com/sso/user/logout?ref=http%3a%2f%2f{0}".format(urllib.quote(host)))


class AuthHandler(BaseHandler):
    def get(self):
        # self.render('index.html', connect_total=len(name_server.get_connected_client()))
        token = self.get_argument('token', '')
        res = urllib.urlopen("http://sytest.cimc.com/sso/user/getUinfo?token=%s" % token)
        data = json.loads(res.read())
        if data.get("code") == 0:
            self.set_secure_cookie("username", data["data"].get("name"))
            self.redirect("/")

        # self.render('index.html', connect_total=len(name_server.get_connected_client()))
        self.redirect("/")


# http://sytest.cimc.com/sso/user/logout?ref=http%3A%2F%2Fticket.cimc.com%2Fuser%2Flogout

class FileViewHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        print 'want to download file from client,request body is:'
        print self.request.body

        body = json.loads(self.request.body)

        path = body['path']
        path = requests.utils.unquote(path).decode('utf-8')
        tid = body['tid']
        wid = body['wid']

        cid = 'cid' + str(uuid.uuid1())
        future = Future()
        _future_list[cid] = future
        # upload file through which url

        # url 是查看的url
        url = 'http://%s/cli_upload?view=1&tid=%s&cid=%s&wid=%s' % (config['web_server'], tid, cid, wid)

        print 'upload url is: ' + url

        paths = [path]
        t_server.request_upload(tid, paths, url, cid, wid)

        result = yield tornado.gen.with_timeout(time.time() + 180, future)
        del _future_list[cid]

        print 'downloadHandler get response from terminal'
        # handle response
        r = result['param']
        print "DownloadHandler r is:"
        print r
        if not r['result']:
            self.write({'result': False, 'msg': '下发失败，请稍后再试'})
        else:
            # get file

            self.write(json.dumps({'result': True}))

    pass


class DownloadHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        print 'want to download file from client,request body is:'
        print self.request.body

        body = json.loads(self.request.body)

        paths = body['paths']
        paths = [requests.utils.unquote(p).decode('utf-8') for p in paths]
        tid = body['tid']
        wid = body['wid']

        cid = 'cid' + str(uuid.uuid1())
        future = Future()
        _future_list[cid] = future
        # upload file through which url

        url = 'http://%s/cli_upload?tid=%s&cid=%s&wid=%s' % (config['web_server'], tid, cid, wid)
        print 'upload url is: ' + url

        t_server.request_upload(tid, paths, url, cid, wid)

        result = yield tornado.gen.with_timeout(time.time() + 180, future)
        del _future_list[cid]

        print 'downloadHandler get response from terminal'
        # handle response
        r = result['param']
        print "DownloadHandler r is:"
        print r
        if not r['result']:
            self.write({'result': False, 'msg': '下发失败，请稍后再试'})
        else:
            self.write(json.dumps({'result': True}))

    pass


class WebUploadHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        path = self.get_argument('path')
        path = requests.utils.unquote(path).decode('utf-8')
        tid = self.get_argument('tid')
        cli_down = self.get_argument('cli_down', 1)

        fileinfo = self.request.files['upload_file'][0]

        fname = fileinfo['filename']
        print 'received file, filename is %s' % fname
        fn_part = os.path.splitext(fname)
        extn = None
        if len(fn_part) > 1:
            extn = fn_part[1]

        sub_path = str(uuid.uuid4())
        cname = "{0}{1}".format(fn_part[0], extn)

        path_dir = 'uploads/' + sub_path
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        with open(path_dir + '/' + cname, 'w') as fh:
            fh.write(fileinfo['body'])

        cid = 'cid' + str(uuid.uuid1())
        future = Future()
        _future_list[cid] = future
        print 'config is :'
        print config
        url = 'http://%s/uploads/%s/%s' % (config['web_server'], sub_path, cname)
        print 'download url is: ' + url

        t_server.request_download(tid, path + "\\" + cname, url, cid)

        result = yield tornado.gen.with_timeout(time.time() + 180, future)
        del _future_list[cid]

        print 'downloadHandler get response from terminal'
        # handle response
        r = result['param']
        if not r['result']:
            self.write({'result': False, 'msg': '下发失败，请稍后再试'})
        else:
            self.write(json.dumps({'result': True}))

    pass


pass


class DirTreeHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        path = self.get_argument('id')
        pattern = self.get_argument('pattern', None)
        path = requests.utils.unquote(path).decode('utf-8')
        if pattern is not None:
            pattern = requests.utils.unquote(pattern).decode('utf-8')

        tid = self.get_argument('tid')

        cid = 'cid' + str(uuid.uuid1())
        t_server.get_file_list(tid, path, pattern, cid)

        future = Future()
        _future_list[cid] = future
        result = yield tornado.gen.with_timeout(time.time() + 180, future)
        del _future_list[cid]

        # handle response
        r = result['param']
        if not r['result']:
            self.write({'result': False, 'msg': '获取失败，请稍后再试'})
        elif not r['list']:
            self.write({'result': False, 'msg': '没有子目录了'})
        elif len(r['list']) == 0:
            self.write({'result': False, 'msg': '没有子目录了'})
        else:
            data = []
            print 'r is :'
            print r
            dir_list = [t for t in r['list'] if t['type'] == 'dir']
            file_list = [t for t in r['list'] if t['type'] == 'file']

            self.write({'result': True, 'msg': 'success', 'data': {'dir_list': dir_list, 'file_list': file_list}})

    pass


pass


class HomeController(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        tid = self.get_argument('tid', '')
        self.render('index.html', connect_total=len(name_server.get_connected_client()), user=self.get_current_user(), tid = tid)

    pass

    def post(self, *args, **kwargs):
        tid = self.get_argument('tid', '')
        if tid in name_server.get_connected_client():
            msg = 'ok'
            self.render('oper_select.html', tid=tid, lastbeat=None)
        else:
            msg = 'no'
            self.write(msg)


class LogHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        tid = self.get_argument('Terminal_ID', '')
        self.render('terminal/look_log.html', tid=tid)


class Show_logHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        tid = self.get_argument('tid', '')
        filename = self.get_argument('filename', '')
        self.render('terminal/show_log.html', tid=tid, filename=filename)


views_dict = {
    'cmd': 'exec_cmd.html',
    'mysql': 'exec_mysql.html',
    'list_dir': 'list_dir.html',
    'sqlite': 'exec_sqlite.html'
}

_future_list = {}


class Oper_Handler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        error = True
        tid = self.get_argument('tid', '')
        oper = self.get_argument('oper', '')
        connected_client = name_server.get_connected_client()
        if tid in connected_client:
            error = False
            res = {'result': None, 'lastbeat': None}
            self.render('terminal/%s' % views_dict[oper], tid=tid, error=error, res=res, ws_host=config['web_server'])
        else:
            self.render('terminal/%s' % views_dict[oper], tid=tid, error=error)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        param = self.get_argument('param', '')
        tid = self.get_argument('tid', '')
        oper = self.get_argument('cmd', '')
        res = {'result': None, 'lastbeat': None}
        connected_client = name_server.get_connected_client()
        if tid in connected_client:
            future = Future()
            res['lastbeat'] = None

            cid = 'cid' + str(uuid.uuid1())
            _future_list[cid] = future
            json_cmd = None
            if oper == 'cmd':
                t_server.send_cmd(tid, param, cid)
            elif oper == 'sqlite':
                t_server.send_sqlite(tid, param, cid)
            pass
            print time.asctime(time.localtime(time.time()))
            # todo: may raise a TimeoutError
            try:
                result = yield tornado.gen.with_timeout(time.time() + 180, future)
            except Exception as e:
                result = {'param': e, "result": False}
            del _future_list[cid]
            print 'response to oper:%s' % result
            r = result['param']
            res['result'] = r

            if oper == 'cmd':
                # print base64.b64decode(result).decode('gb2312')
                self.write(r)

            elif oper == 'mysql':
                self.render("terminal/mysql_result.html", result=result)

            elif oper == 'sqlite':
                self.write(r)

            elif oper == 'list_dir':
                result = json.dumps(result)
                self.write(result)

            elif oper == 'get_log':
                result = base64.b64decode(result)
                self.write(result)

        else:
            pass


pass

'''
接收T server的推送
'''


class TerminalRespController(BaseHandler):
    # @tornado.web.authenticated
    def post(self, *args, **kwargs):
        print 'get response from terminal_server'
        body = b64.b64_to_json(self.request.body)
        print 'response is : ' + base64.b64decode(self.request.body)
        tid = body['tid']
        wid = body['wid']
        cid = body['cid']
        cmd = body['cmd']
        param = body['param']

        global _future_list
        if cid in _future_list.keys():
            _future_list[cid].set_result(body)
        pass

    pass


pass

if __name__ == "__main__":

    if not os.path.exists('downloads/'):
        os.makedirs('downloads')
    if not os.path.exists('uploads/'):
        os.makedirs('uploads')
    tornado.options.parse_command_line()
    app = Application()
    app.listen(9000)
    #    http_server=tornado.httpserver.HTTPServer(app)
    #    http_server.bind(8081,'0.0.0.0')
    #    http_server.start(num_processes=0)
    print 'Server Start listening'
    tornado.ioloop.IOLoop.instance().start()
