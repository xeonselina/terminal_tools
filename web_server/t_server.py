import json
import requests
import name_server
import base64
import b64
from tornado import gen

config = {}
execfile('app.conf', config)


@gen.coroutine
def get_file_list(tid, path, pattern, cid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'dir', 'wid': 'w1',
                                                                    'param': {'path': path, 'pattern': pattern}}),
                  timeout=1)


pass


@gen.coroutine
def send_cmd(tid, cmd, cid, wid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'cmd', 'wid': wid,
                                                                    'param': cmd}), timeout=1)


pass


@gen.coroutine
def restart_cmd(tid, cmd, cid, wid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'restart_cmd', 'wid': wid,
                                                                    'param': cmd}))




@gen.coroutine
def request_getprocesslist(tid, cmd, cid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'process', 'wid': 'w1',
                                   'param': cmd}), timeout=1)

@gen.coroutine
def kill_proce(tid, cmd, cid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'kill_proc', 'wid': 'w1',
                                                                    'param': cmd}),timeout=1)

@gen.coroutine
def send_sqlite(tid, cmd, cid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'sqlite', 'wid': 'w1',
                                   'param': {'query': cmd}}), timeout=1)


pass


@gen.coroutine
def request_download(tid, path, url, cid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'download', 'wid': 'w1',
                                   'param': {'path': path, 'url': url}}), timeout=1)


pass


@gen.coroutine
def request_upload(tid, paths, url, cid, wid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'upload', 'wid': wid,
                                   'param': {'paths': paths, 'url': url}}), timeout=1)


pass


@gen.coroutine
def request_rename(tid, cmd, cid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'rename', 'wid': 'w1',
                                   'param': cmd}), timeout=1)


pass


@gen.coroutine
def request_delete_file(tid, cmd, cid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'delete', 'wid': 'w1',
                                   'param': cmd}), timeout=1)


@gen.coroutine
def close_pty(tid, session_id):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': 'c0', 'cmd': 'close_pty', 'wid': 'w1', 'param': session_id}),
                  timeout=1)


@gen.coroutine
def open_pty(tid, session_id, host, cid):
    t_server = yield name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64(
        {'tid': tid, 'cid': cid, 'cmd': 'open_pty', 'wid': 'w1', 'param': {'session_id': session_id, 'host': host}}),
                  timeout=1)
