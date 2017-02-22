#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import sqlite3
import os
import json

config = {}
execfile('app.conf', config)

db_path = config['db_path']
conn=None
cursor=None


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
pass


def __open():
    try:
        global conn
        conn = sqlite3.connect(db_path)
        conn.text_factory = str
        conn.row_factory = dict_factory
        global cursor
        cursor = conn.cursor()
    except Exception as e:
        raise e
pass


def __close():
    if conn:
        conn.close()
pass


def fetchone(q):
    try:
        __open()
        cursor.execute(q)
        return cursor.fetchone()
    finally:
        __close()
pass



