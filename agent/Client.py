# -*- coding: UTF-8 -*-
import websocket
import threading
import time
import json
import sys
import os
import logging
import logging.handlers
import traceback
import requests
import cmd_handler
import sqlite_handler
import handler
import b64
import sqlite_helper
import platform
import ctypes

from tendo import singleton

me = singleton.SingleInstance()

reload(sys)
sys.setdefaultencoding("utf-8")
__conn = 0
__tid = None


def get_logger():
    _logger = logging.getLogger('ws_job')
    log_format = '%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s'
    formatter = logging.Formatter(log_format)
    logfile = 'log/ws.log'
    rotate_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024, backupCount=5)
    rotate_handler.setFormatter(formatter)
    _logger.addHandler(rotate_handler)
    _logger.setLevel(logging.DEBUG)
    return _logger


pass

LOG_DIR = os.path.join(os.path.dirname(__file__), 'log').replace('\\', '/')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
logger = get_logger()

_sqlite_handler = sqlite_handler.SqliteHandler()
_cmd_handler = None
_pty_handler = None

__msg_callback = {
    'sqlite': _sqlite_handler.handle,
    'dir': handler.DirHandler().handle,
    'download': handler.DownloadHandler().handle,
    'upload': handler.UploadHandler().handle,
    'rename': handler.RenameHandler().handle,
    'delete': handler.DeleteHandler().handle,
    'process': handler.GetProcessList().handle,
    'kill_proc': handler.GetProcessList().kill,
    'unzip': handler.UnzipHandler().handle,
    'rs_ag': handler.RestartAgentHandler().handle,
    'upd_ag': handler.UpgradeAgentHandler().handle,
}

if os.name == 'nt':
    _cmd_handler = cmd_handler.CmdHandler()
    _cmd_handler.start_loop()
    __msg_callback["cmd"] = _cmd_handler.handle
    __msg_callback["restart_cmd"] = _cmd_handler.restart_cmd
else:
    import pty_handler

    _pty_handler = pty_handler.PtyHandler()
    __msg_callback["open_pty"] = _pty_handler.handle
    __msg_callback["close_pty"] = _pty_handler.handle


def __process_message(ws, json_message):
    cmd = json_message.get('cmd')
    tid = json_message.get('tid')
    wid = json_message.get('wid')
    cid = json_message.get('cid')
    param = json_message.get('param')

    logger.info('received msg: %s ' % json_message)
    if cmd in __msg_callback.keys():
        t, response = __msg_callback.get(cmd)(ws, tid, wid, cmd, cid, param)
        if response is not None:
            logger.info('resp %s,%s ' % (t, response))
            ws.send(b64.json_to_b64(
                {'cmd': t, 'tid': tid, 'wid': wid, 'cid': cid, 'param': response}))
    else:
        pass


def on_message(ws, message):
    __process_message(ws, b64.b64_to_json(message))


pass


def on_error(ws, error):
    # logger.info(error
    logger.error(traceback.format_exc())


pass


def on_close(ws):
    # logger.info("### closed ###"
    logger.info('##### Conection closed ######')
    global __conn
    __conn = 0


pass


def on_ping(ws):
    ws.send(b64.json_to_b64({'tid': __tid}))


def on_open(ws):
    logger.info("##### Connection open #####")
    logger.info("open")
    ws.send(b64.json_to_b64({'cmd': 'reg', 'tid': __tid, 'wid': 'w0', 'cid': 'c0', 'param': {"os": os.name}}))
    global __conn
    __conn = 1

    def hb(websocket):
        while 1:
            logger.info('sending hb')
            websocket.send(b64.json_to_b64({'cmd': 'hb', 'tid': __tid, 'wid': 'w0', 'cid': 'c0', 'param': ''}))
            time.sleep(30)

    pass

    t = threading.Thread(target=hb, args=[ws])
    t.setDaemon(True)
    t.start()


pass


def reg_to_name_server(tid):
    name_server = config['name_server']
    # get t_server ip_port from name_server
    ip_port = None
    try:
        os_name = os.name
        logger.info('request to name_server with name_server: %s, tid: %s, os_name: %s ' % (name_server, tid, os_name))

        if os_name == 'posix':
            libc = ctypes.cdll.LoadLibrary('libc.so.6')
            res_init = libc.__res_init
            res_init()

        response = requests.post(name_server + '/terminal_reg', json={'tid': tid, 'os': os_name,'version':config['version']}, timeout=6)

        if response.status_code == 200:
            logger.info('request to name_server resp:' + response.content)
            result = response.json()
            if result['result']:
                ip_port = result['ip_port']
        else:
            logger.error('request to name_server error, response code: ' + response.status_code)
    except Exception as ex:
        logger.error('request to name_server error')
        logger.error(ex)
        pass
    return ip_port


pass

config = {}
execfile('app.conf', config)

if __name__ == "__main__":
    websocket.enableTrace(True)

    # 终端号
    # todo: for test only
    global __tid
    __tid = config['sn']
    while True:
        row = None
        try:
            row = sqlite_helper.fetchone('select config_value from t_config where config_key = \'CIMC.sn\' limit 1;')
        except:
            logger.info("can't read sn config row from db")

        if row:
            __tid = row['config_value']

        logger.info('get tid: %s' % __tid)
        while True:
            if not __conn:
                t_server = reg_to_name_server(__tid)
                if not t_server:
                    time.sleep(6)
                    continue

                ws = websocket.WebSocketApp("ws://" + t_server + "/server",
                                            on_message=on_message,
                                            on_error=on_error,
                                            on_close=on_close,
                                            )
                ws.on_open = on_open
                ws.run_forever()
            pass

            time.sleep(6)
        pass
        time.sleep(30)

    pass
pass
