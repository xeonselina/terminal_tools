# -*- coding: UTF-8 -*-
import tornado
import t_server
import time
from tornado import gen
import retrying
from retrying import retry

connected_web_client = {}
connected_client = {}


class PTYWSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    pass

    def __init__(self, application, request, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(self, application, request, **kwargs)
        self.session_id = None
        self.tid = None

        self.__callback_map = {
            'c': self.client_reg_handle,
            'w': self.web_client_reg_handle,
            'i': self.input_handle,
            'p': self.resp_handle,
            's': self.resize_handle,
            'e': self.client_close_handle
        }

    pass

    def open(self):
        #	Nothing to do untill we got the first heartbeat
        print "new client connected"

    pass

    def on_message(self, message):

        print time.time()
        print 'pty_module on_message: ' + message

        cmd = message[0]
        handle = self.__callback_map[cmd]
        ret = handle(message[1:])
        if not ret:
            if self.session_id in connected_client.keys():
                connected_client[self.session_id].close()
            if self.session_id in connected_web_client.keys():
                connected_web_client[self.session_id].close()
        pass

    pass

    # 客户端注册
    def client_reg_handle(self, message):
        try:
            self.session_id = message
            print time.time()
            print 'client_reg_handle sid:' + self.session_id
            connected_client[self.session_id] = self
            return True
        except Exception as ex:
            print ex
            raise ex

    pass

    # 页面注册
    def web_client_reg_handle(self, message):
        try:
            self.session_id, self.tid = tuple(message.split('&&'))
            print time.time()
            print 'web_client_reg_handle sid:' + self.session_id
            connected_web_client[self.session_id] = self
            #ack to connected agent client
            print time.time()
            print 'send w+sid to client'
            connected_client[self.session_id].write_message('w'+self.session_id)
            return True
        except Exception as ex:
            print ex
            raise ex

    pass

    # 页面输入
    # @retry(stop_max_attempt_number=20, wait_random_min=500, wait_random_max=1000)
    def input_handle(self, message):
        try:
            connected_client[self.session_id].write_message('i' + message)
            return True
        except Exception as ex:
            print ex
            raise ex

    pass

    # 客户端返回
    #@retry(stop_max_attempt_number=10, wait_random_min=500, wait_random_max=1000)
    def resp_handle(self, message):
        try:
            print time.time()
            if not self.session_id:
                print 'self.session_id is None, received msg is : ' + message
                return True

            print 'resp_handle received session_id %s. msg %s' % (self.session_id, message)
            connected_web_client[self.session_id].write_message('p' + message)
            return True
        except Exception as ex:
            print ex
            raise ex

    pass

    # 通知客户端resize
    # @retry(stop_max_attempt_number=20, wait_random_min=500, wait_random_max=1000)
    @gen.coroutine
    def resize_handle(self, message):
        print 'send resize'
        try:
            print time.time()
            print 'resize_handle received session_id %s. msg %s' % (self.session_id, message)
            yield gen.sleep(3)
            connected_client[self.session_id].write_message('s' + message)
            raise gen.Return(True)
        except Exception as ex:
            print ex
            raise ex

    pass

    def client_close_handle(self, message):
        print 'client disconnect'
        self.on_close()
        return True

    pass

    def on_close(self):
        if self.session_id in connected_web_client.keys():
            connected_web_client[self.session_id].close()
            del connected_web_client[self.session_id]

            if self.session_id in connected_client.keys():
                connected_client[self.session_id].close()
                del connected_client[self.session_id]
                t_server.close_pty(self.tid, self.session_id)

            print "close %s" % self.session_id
            print "new webclient connected, all connected_web_client.keys() are:"
            print connected_web_client.keys()

    pass


pass
