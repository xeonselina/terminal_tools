from tornado import httpclient, gen
from cachetools import TTLCache, cached
import time,json
from tornado.httputil import url_concat

config = {}
execfile('app.conf', config)

t_server_cache = TTLCache(maxsize=128, ttl=32)
connected_t_cache = TTLCache(maxsize=1, ttl=8)


@cached(t_server_cache)
@gen.coroutine
def get_t_server(tid):
    http_c = httpclient.AsyncHTTPClient()
    param = {'tid':tid}
    url = config['name_server'] + "/get_t_server"
    url = url_concat(url,param)
    r = yield http_c.fetch(url, request_timeout=1)

    #print 'get_t_server return r'+ json.dumps(r)

    if r.code == 200:
        obj = json.loads(r.body)
        if obj['result']:
            raise gen.Return(obj['ip_port'])
    else:
        raise gen.Return(None)


pass


#@web.asynchronous
@cached(connected_t_cache)
@gen.coroutine
def get_connected_client():
    conn_t_list = []
    http_c = httpclient.AsyncHTTPClient()

    r = yield http_c.fetch(config['name_server'] + "/get_conn_t", request_timeout=1)
    print 'get_connected_client return f struct:' + r.body
    if r.code == 200:
        result = json.loads(r.body)
        if result['result']:
            conn_t_list = result['list']
    raise gen.Return(conn_t_list)

pass
