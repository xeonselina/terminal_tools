import os
import urllib
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
import requests
import tornado.httpserver


class dir_list_handler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        r=[ '<ul class="jqueryFileTree" style="display: none;">']
        try:
            print 'test1111111111111'
            r=['<ul class="jqueryFileTree" style="display: none;">']
            d=urllib.unquote(self.get_argument('dir','c:\\temp'))
            for f in os.listdir(d):
                ff=os.path.join(d,f)
                if os.path.isdir(ff):
                    r.append('<li class="directory collapsed"><a rel="%s/">%s</a></li>' % (ff,f))
                else:
                    e=os.path.splitext(f)[1][1:] # get .ext and remove dot
                    r.append('<li class="file ext_%s"><a rel="%s">%s</a></li>' % (e,ff,f))
            r.append('</ul>')
            print 'test2222222'
        except Exception,e:
            r.append('Could not load directory: %s' % str(e))
        r.append('</ul>')
        return self.write(''.join(r))