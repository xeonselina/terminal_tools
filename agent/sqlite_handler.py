#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import sqlite3
import os
import json
import logging
import logging.handlers

config = {}
execfile('app.conf', config)
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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqliteHandler:
    def __init__(self):
        self.db_path = config['db_path']

    def __del__(self):
        self.__close()

    def __file_exist(self):
        if os.path.exists(self.db_path):
            return True
        else:
            return False

    def __open(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.text_factory = str
            self.conn.row_factory = dict_factory
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise e

    def __close(self):
        if hasattr(self, 'conn') and self.conn:
            logger.info('close conn')
            self.conn.close()

    def __execute(self, execute_sql):
        try:
            self.__open()
            self.cursor.execute(execute_sql)
            self.conn.commit()
            self.result = self.cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            self.__close()

    def handle(self, ws, tid, wid, cmd, cid, param):
        if param.has_key("db_path") and param["db_path"]:
            self.db_path = param["db_path"]
        else:
            self.db_path = config['db_path']
        if not self.__file_exist():
            return 'sql_resp', {'result': False, 'msg': 'DB File Not Found'}
        else:
            try:
                if not hasattr(self, 'conn') or not self.conn:
                    self.__open()
                self.__execute(param['query'])
                return 'sql_resp', {'result': True,
                                    'data': unicode(json.dumps(self.result, ensure_ascii=False), errors='ignore')}
            except Exception as e:
                return 'sql_resp', {'result': False, 'msg': unicode(e.message, errors='ignore')}


if __name__ == '__main__':
    sqlitehandle = SqliteHandler()
    sql = {'query': 'select * from t_log limit 10'}
    logger.info(sqlitehandle.handle(None, None, None, sql))
