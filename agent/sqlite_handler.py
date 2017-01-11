#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import sqlite3
import os
import json

config = {}
execfile('app.conf', config)


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
			print 'close conn'
			self.conn.close()

	def __execute(self, execute_sql):
		try:
			self.cursor.execute(execute_sql)
			self.conn.commit()
			self.result = self.cursor.fetchall()
		except Exception as e:
			raise e

	def handle(self, ws, cmd, cid, param):
		if not self.__file_exist():
			return 'DB File Not Found'
		else:
			try:
				if not hasattr(self, 'conn') or not self.conn:
					self.__open()
				self.__execute(param['query'])
				return 'sql_resp', {'result': True, 'data': unicode(json.dumps(self.result,ensure_ascii=False),errors='ignore')}
			except Exception as e:
				return 'sql_resp', {'result': False, 'msg': unicode(e.message, errors='ignore')}


if __name__ == '__main__':
	sqlitehandle = SqliteHandler()
	sql = {'query': 'select * from t_log limit 10'}
	print sqlitehandle.handle(None, None, None, sql)
