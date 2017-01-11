import json
import requests
import name_server
import base64
import b64

config = {}
execfile('app.conf', config)


def get_file_list(tid, path, pattern, cid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'dir', 'wid': 'w1',
                                                                    'param': {'path': path, 'pattern': pattern}}))


pass


def send_cmd(tid, cmd, cid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'cmd', 'wid': 'w1',
                                                                    'param': cmd}))


pass


def send_sqlite(tid, cmd, cid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'sqlite', 'wid': 'w1',
                                   'param': {'query': cmd}}))


pass


def request_download(tid, path, url, cid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'download', 'wid': 'w1',
                                   'param': {'path': path, 'url': url}}))


pass


def request_upload(tid, paths, url, cid, wid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'upload', 'wid': wid,
                                   'param': {'paths': paths, 'url': url}}))


pass
