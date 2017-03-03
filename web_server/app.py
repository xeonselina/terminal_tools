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
import magic
from tornado import gen
from urllib import quote
import sys
import pty_module
from pty_module import PTYWSHandler

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
                    (r"/cmd", CMDHandler),
                    (r"/restart_cmd", Restart_CMDHandler),
                    (r"/sqlite", SqliteHandler),
                    (r"/web_upload", FineUploadHandler),
                    (r"/file_download", DownloadHandler),
                    (r"/file_view", FileViewHandler),
                    (r"/file_delete", FileDeleteHandler),
                    (r"/dir_tree", DirTreeHandler),
                    (r"/uploads/(.*)", tornado.web.StaticFileHandler, {"path": "uploads/"}),
                    (r"/ws", WSHandler),
                    (r"/pty_ws", PTYWSHandler),
                    (r"/cli_upload", ClientUploadHandler),
                    (r"/rename", RenameHandler),
                    (r"/unzip", UnzipHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    (r"/auth", AuthHandler),
                    (r"/process", GetProcessListHandler),
                    (r"/kill_proc", KillProcess),]
        tornado.web.Application.__init__(self, handlers, **settings)


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    pass

    def __init__(self, application, request, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(self, application, request, **kwargs)
        self.wid = -1
        self.tid = -1

    pass

    def open(self):
        #	Nothing to do untill we got the first heartbeat
        print "new client connected"

    pass

    @gen.coroutine
    def on_message(self, message):
        print 'received web client message: %s' % base64.b64decode(message)
        msg_obj = b64.b64_to_json(message)

        cmd = msg_obj['cmd']

        if cmd == 'reg':
            connected_web_client[msg_obj['wid']] = self
            print "new webclient connected, all connected_web_client.keys() are:"
            print connected_web_client.keys()
            self.wid = msg_obj['wid']
            self.tid = msg_obj.get('tid', '')

        elif cmd == 'pty_input':
            # 收到页面xterm的输入，要把输入发送到client端
            param = msg_obj['param']
            connected_clients = yield name_server.get_connected_client()
            if self.tid in connected_clients.keys():
                cid = 'cid' + str(uuid.uuid1())
                yield t_server.send_pty(self.tid, param, cid, self.wid)

        elif cmd == 'pty_resize':
            # 收到页面xterm的resize，要把输入发送到client端
            param = msg_obj['param']
            connected_clients = yield name_server.get_connected_client()
            if self.tid in connected_clients.keys():
                cid = 'cid' + str(uuid.uuid1())
                yield t_server.send_pty_resize(self.tid, param, cid, self.wid)
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
        is_view = self.get_argument('view', '')

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
                subprocess.call(['7za', 'x', 'uploads/%s/%s' % (sub_path, cname), '-y', '-o%s' % unzip_path])
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
                        # (mtype, _) = mimetypes.guess_type(long)
                        mtype = magic.from_file(long)
                        # 文本文件才打开
                        if 'text' in mtype:
                            with open(long) as f:
                                cl = f.readlines()
                                cl = [c + '<br/>' for c in cl]
                                content = ""
                                content = content.join(cl)

                                try:
                                    content = content.decode("gbk")
                                except:
                                    pass

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
        path = requests.utils.unquote(path)
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
        paths = [requests.utils.unquote(p) for p in paths]
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


class RenameHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        param = json.loads(self.request.body)
        tid = param['tid']
        newValue = param['newValue']
        fullName = param['fullPath']
        oldValue = param['oldValue']
        connected_client = yield name_server.get_connected_client().keys()
        if tid in connected_client:
            future = Future()
            cid = 'cid' + str(uuid.uuid1())
            _future_list[cid] = future
            excuteCmd = json.dumps({'fullName': fullName, 'newValue': newValue, 'oldValue': oldValue},
                                   ensure_ascii=False)
            t_server.request_rename(tid, excuteCmd, cid)
            pass
            print time.asctime(time.localtime(time.time()))
            # todo: may raise a TimeoutError
            try:
                result = yield tornado.gen.with_timeout(time.time() + 180, future)
            except Exception as e:
                result = {'param': e, "result": False}
            del _future_list[cid]
            print 'response to rename:%s' % result
            r = result['param']
            if not r['result']:
                self.write({'result': False, 'msg': r['msg']})
            else:
                self.write(json.dumps({'result': True, 'msg': '重命名成功!'}))
        pass


pass





class GetProcessListHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        param = json.loads(self.request.body)
        tid = param['tid']
        connected_client = yield name_server.get_connected_client()
        if tid in connected_client.keys():
            future = Future()
            cid = 'cid' + str(uuid.uuid1())
            _future_list[cid] = future
            t_server.request_getprocesslist(tid, '', cid)
            try:
                result = yield tornado.gen.with_timeout(time.time() + 180, future)
            except Exception as e:
                result = {'param': e, "result": False}
            del _future_list[cid]
            print 'response to getprocesslist:%s' % result
            r = result['param']
            if not r['result']:
                self.write({'result': False, 'msg': r['msg']})
            else:
                self.write(json.dumps({'result': True, 'msg': '获取成功!', 'list': r['list']}))
        pass

class KillProcess(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        param = json.loads(self.request.body)
        tid = param['tid']
        pid = param['pid']
        connected_client = yield name_server.get_connected_client()
        if tid in connected_client.keys():
            future = Future()
            cid = 'cid' + str(uuid.uuid1())
            _future_list[cid] = future
            t_server.kill_proce(tid, pid, cid)
            try:
                result = yield tornado.gen.with_timeout(time.time() + 180, future)
            except Exception as e:
                result = {'param': e, "result": False}
            del _future_list[cid]
            print 'response to getprocesslist:%s' % result
            r = result['param']
            if not r['result']:
                self.write({'result': False, 'msg': r['msg']})
            else:
                self.write(json.dumps({'result': True, 'msg': '操作成功!'}))
        pass


class FileDeleteHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        param = json.loads(self.request.body)
        tid = param['tid']
        file_path = param['paths']
        connected_client = yield name_server.get_connected_client()
        if tid in connected_client.keys():
            future = Future()
            cid = 'cid' + str(uuid.uuid1())
            _future_list[cid] = future
            params = json.dumps({'filePath': file_path}, ensure_ascii=False)
            t_server.request_delete_file(tid, params, cid)
            pass
            print time.asctime(time.localtime(time.time()))
            # todo: may raise a TimeoutError
            try:
                result = yield tornado.gen.with_timeout(time.time() + 180, future)
            except Exception as e:
                result = {'param': e, "result": False}
            del _future_list[cid]
            print 'response to delete:%s' % result
            r = result['param']
            if not r['result']:
                self.write({'result': False, 'msg': r['msg']})
            else:
                self.write(json.dumps({'result': True, 'msg': '删除成功!'}))
        pass
pass


class UnzipHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        param = json.loads(self.request.body)
        tid = param['tid']
        file_path = param['path']
        connected_client = yield name_server.get_connected_client()
        if tid in connected_client.keys():
            future = Future()
            cid = 'cid' + str(uuid.uuid1())
            _future_list[cid] = future
            t_server.request_unzip_file(tid, file_path, cid)
            pass
            print time.asctime(time.localtime(time.time()))
            # todo: may raise a TimeoutError
            try:
                result = yield tornado.gen.with_timeout(time.time() + 180, future)
            except Exception as e:
                result = {'param': e, "result": False}
            del _future_list[cid]
            print 'response to unzip:%s' % result
            r = result['param']
            if not r['result']:
                self.write({'result': False, 'msg': r['msg']})
            else:
                self.write(json.dumps({'result': True, 'msg': '解压成功!'}))
        pass
pass




class FineUploadHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        fileuuid = self.get_argument('qquuid')
        filename = self.get_argument('qqfilename')
        tid = self.get_argument('tid')
        upload_file = self.request.files['qqfile'][0]
        path = self.get_argument('path')
        print 'received file, filename is %s' % filename
        path_dir = 'uploads/' + fileuuid
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        path_file = path_dir + '/' + filename
        with open(path_file, 'w') as fh:
            fh.write(upload_file['body'])

        cid = 'cid' + str(uuid.uuid1())
        future = Future()
        _future_list[cid] = future
        print 'config is :'
        print config

        url = ('http://%s/uploads/%s/%s' % (config['web_server'], fileuuid, filename)).encode('utf-8')
        print 'download url is: ' + url
        dest_path = (os.path.join(path, filename)).encode('utf-8')
        t_server.request_download(tid, dest_path, url, cid)

        result = yield tornado.gen.with_timeout(time.time() + 3600, future)
        del _future_list[cid]

        print 'downloadHandler get response from terminal'
        # handle response
        r = result['param']
        if not r['result']:
            self.write({'success': False, 'msg': '下发失败，请稍后再试'})
        else:
            self.write(json.dumps({'success': True}))

    pass


class WebUploadHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):

        path = self.get_argument('path')
        path = requests.utils.unquote(path)
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

        cid = 'cid' + str(uuid.uuid4())
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
        path = requests.utils.unquote(path)
        if pattern is not None:
            pattern = requests.utils.unquote(pattern)
        print [(urllib.unquote(urllib.unquote(path)))]
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
            self.write({'result': False, 'msg': r['msg'], 'data': {'dir_list': [], 'file_list': []}})
        elif not r['list']:
            self.write({'result': True, 'msg': '没有子目录了', 'data': {'dir_list': [], 'file_list': []}})
        elif len(r['list']) == 0:
            self.write({'result': True, 'msg': '没有子目录了', 'data': {'dir_list': [], 'file_list': []}})
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
    @tornado.gen.coroutine
    def get(self):
        tid = self.get_argument('tid', '')
        conn_t = yield name_server.get_connected_client()
        self.render('index.html', connect_total=len(conn_t.keys()),
                    user=self.get_current_user(), tid=tid)

    pass

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        tid = self.get_argument('tid', '')
        if tid in (yield name_server.get_connected_client()).keys():
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
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        error = True
        tid = self.get_argument('tid', '')
        oper = self.get_argument('oper', '')
        db_path = self.get_argument('db_path', '')
        if db_path:
            db_path = db_path.replace("\\", "\\\\")
        connected_client = yield name_server.get_connected_client()
        if tid in connected_client.keys():
            error = False
            res = {'result': None, 'lastbeat': None}
            # linux的打开pty.html里面用xterm.js作为终端
            if oper == 'cmd' and connected_client[tid] == 'posix':
                session_id = 's' + str(uuid.uuid4())

                cid = "c"+str(uuid.uuid1())
                open_pty_future = Future()
                yield t_server.open_pty(tid, session_id,config['web_server'],cid)
                _future_list[cid] = open_pty_future
                result = yield tornado.gen.with_timeout(time.time() + 180, open_pty_future)

                self.render('terminal/%s' % 'pty.html', tid=tid, error=error, res=res, ws_host=config['web_server'],
                            session_id=session_id)
            else:
                self.render('terminal/%s' % views_dict[oper], tid=tid, error=error, res=res,db_path = db_path,
                            ws_host=config['web_server'])
        else:
            self.render('terminal/%s' % views_dict[oper], tid=tid, error=error)


pass


class CMDHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        param = self.get_argument('param')
        tid = self.get_argument('tid')
        wid = self.get_argument('wid')
        res = {'result': None, 'lastbeat': None}
        connected_client = yield name_server.get_connected_client()
        if tid in connected_client.keys():
            res['lastbeat'] = None

            cid = 'cid' + str(uuid.uuid1())
            yield t_server.send_cmd(tid, param, cid, wid)

            # print base64.b64decode(result).decode('gb2312')
            self.write({'result': True})

        else:
            pass


pass

class Restart_CMDHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        param = self.get_argument('param')
        tid = self.get_argument('tid')
        wid = self.get_argument('wid')
        res = {'result': None, 'lastbeat': None}
        connected_client = yield name_server.get_connected_client()
        if tid in connected_client.keys():
            res['lastbeat'] = None

            cid = 'cid' + str(uuid.uuid1())
            t_server.restart_cmd(tid, param, cid, wid)

            # print base64.b64decode(result).decode('gb2312')
            self.write({'result':True})

        else:
            pass

class SqliteHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        param = self.get_argument('param')
        db_path = self.get_argument('db_path','')
        tid = self.get_argument('tid')
        res = {'result': None, 'lastbeat': None}
        connected_client = yield name_server.get_connected_client()
        if tid in connected_client.keys():
            future = Future()
            res['lastbeat'] = None

            cid = 'cid' + str(uuid.uuid1())
            _future_list[cid] = future
            if db_path:
                db_path = db_path.replace("\\","\\\\")
            t_server.send_sqlite(tid, param, cid, db_path)
            pass
            try:
                result = yield tornado.gen.with_timeout(time.time() + 180, future)
            except Exception as e:
                result = {'param': e, "result": False}
            del _future_list[cid]
            print 'response to sqlite_cmd:%s' % result
            r = result['param']
            res['result'] = r

            self.write(r)

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
        #print 'response is : ' + base64.b64decode(self.request.body)
        tid = body['tid']
        wid = body['wid']
        cid = body['cid']
        cmd = body['cmd']
        param = body['param']

        global _future_list
        if cid in _future_list.keys():
            _future_list[cid].set_result(body)
        pass

        if wid in connected_web_client.keys():
            connected_web_client[wid].write_message(b64.json_to_b64(body))
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
