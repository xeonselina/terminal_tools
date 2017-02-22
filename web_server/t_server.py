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
                                                                    'param': {'path': path, 'pattern': pattern}}),timeout=1)


pass


def send_cmd(tid, cmd, cid, wid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'cmd', 'wid': wid,
                                                                    'param': cmd}),timeout=1)

pass

def send_pty(tid, data, cid,wid):
    try:
        t_server = name_server.get_t_server(tid)
        requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'pty_input', 'wid': wid,
                                                                    'param': data}),timeout=1)
    except Exception as ex:
        print 'send_pty occur exception'
        print ex


pass

def send_pty_resize(tid, data, cid, wid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'pty_resize', 'wid': wid,
                                                                    'param': data}),timeout=1)

pass

def request_getprocesslist(tid, cmd, cid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'process', 'wid': 'w1',
                                                                    'param': cmd}),timeout=1)

def send_sqlite(tid, cmd, cid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'sqlite', 'wid': 'w1',
                                   'param': {'query': cmd}}),timeout=1)


pass


def request_download(tid, path, url, cid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'download', 'wid': 'w1',
                                   'param': {'path': path, 'url': url}}),timeout=1)


pass


def request_upload(tid, paths, url, cid, wid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'upload', 'wid': wid,
                                   'param': {'paths': paths, 'url': url}}),timeout=1)


pass

def request_rename(tid,cmd,cid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server, b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'rename', 'wid': 'w1',
                                                                    'param': cmd}),timeout=1)
pass

def request_delete_file(tid, cmd, cid):
    t_server = name_server.get_t_server(tid)
    requests.post('http://%s/terminal' % t_server,
                  b64.json_to_b64({'tid': tid, 'cid': cid, 'cmd': 'delete', 'wid': 'w1',
                                   'param': cmd}),timeout=1)

