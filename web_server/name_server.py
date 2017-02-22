import json
import requests

config = {}
execfile('app.conf', config)


def get_t_server(tid):
    r = requests.get(config['name_server'] + '/get_t_server', {'tid': tid},timeout=1)
    print 'get_t_server return: ' + r.text
    if r.status_code == 200:
        obj = r.json()
        if obj['result']:
            return obj['ip_port']
    else:
        return None


pass


def get_connected_client():
    conn_t_list = []
    r = requests.get(config['name_server'] + '/get_conn_t',timeout=1)
    print 'get_connected_client return: ' + r.text
    if r.status_code == 200:
        result = r.json()
        if result['result']:
            conn_t_list = result['list']
    return conn_t_list


pass
