# -*- coding: UTF-8 -*-
import fnmatch
import json
import datetime, time
import re
import threading
import Queue
import subprocess
import requests
import os
import uuid
from urllib import unquote
import psutil
import retrying
import download_helper
from download_helper import *
import logging
import logging.handlers
from retrying import retry

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
class DirHandler:
    def handle(self, ws, tid, wid, cmd, cid, param):
        # get dir info
        msg = ''
        path = param['path']
        if path == "#":
            disks = psutil.disk_partitions()
            partitions = []
            for d in disks:
                if d.fstype == '' or d.opts == 'cdrom':
                    continue
                partitions.append({'type':'dir','name':d.mountpoint})

            return "dir_resp",{'result': True, 'msg': "Success", 'list': partitions}
        
        pattern = param['pattern']
        if not os.path.isdir(path):
            return 'dir_resp', {'result': False, 'msg': '目录不存在'}

        try:
            items = []
            # it's search ,so walk through the dir
            if pattern:
                pattern = "*" + pattern + "*"
                for root, dirs, files in os.walk(path):
                    # only walk 20 files
                    if len(items) > 20:
                        break

                    matchs = fnmatch.filter(files, pattern)

                    if len(matchs) > 0:
                        matchs = [(os.path.join(root, name), name) for name in matchs]
                        items.extend(matchs)
            else:
                items = os.listdir(path)
                items = [(os.path.join(path, t), t) for t in items]
        except Exception as ex:
            if ex.winerror == 5:
                return 'dir_resp', {'result': False, 'msg': '目录是个连接'}
            else:
                return 'dir_resp', {'result': False, 'msg': '访问目录出错，%s' % ex.message}

        r = {'result': True, 'msg': "Success", 'list': []}

        for full, short in items:

            is_dir = os.path.isdir(full)
            item_type = 'file'
            if is_dir:
                item_type = 'dir'

            try:
                stat = os.stat(full)
                create_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_ctime))
                modify_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
                size = stat.st_size / 1024

                r['list'].append(
                    {'type': item_type, 'name': short, 'full_name': os.path.abspath(full),
                     'create_date': create_date,
                     'update_date': modify_date, 'size': '%s kb' % size})
            except:
                r['list'].append(
                    {'type': item_type, 'name': short})

        return 'dir_resp', r

    pass

class GetProcessList:
    def getProcessInfo(self,pid):
        pro = psutil.Process(pid)
        p_name = pro.name()
        p_cpud = pro.cpu_percent()#interval=5
        p_mem = pro.memory_percent()

        
        return ( p_name, self.format(p_cpud), self.format(p_mem) )


    def format(self,v):
        return float("%02.f" % v)

    def kill(self, ws, tid, wid, cmd, cid, param):
        try:
            p = psutil.Process(int(param))
            p.kill()
        except:
            return 'kill_process_resp', {'result': False, 'msg': '操作失败！'}

        return 'kill_process_resp', {'result': True, 'msg': 'success'}
    
    def handle(self, ws, tid, wid, cmd, cid, param):
        pid_list = psutil.pids()
        process_list = []
        for p in pid_list:
            item = {}
            try:
                p_name, p_cpud, p_mem = self.getProcessInfo(p)
            except:
                continue
            item["p_pid"] = p
            item["p_name"] = p_name
            item["p_cpud"] = p_cpud
            item["p_mem"] = p_mem
            process_list.append(item)
            #break
        return 'process_resp', {'result': True, 'msg': 'success', 'list': process_list}


class UnzipHandler:
    def handle(self, ws, tid, wid, cmd, cid, param):
        path = param['path']
        dir = os.path.dirname(path)
        cmd = ['7za', 'x', '-y', path, r'-o%s'%dir]
        p = subprocess.Popen(' '.join(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE)

        out,err = p.communicate()
        logger.info('unzip out: '+ out)
        if err or 'Everything is Ok' not in out:
            #压缩出错
            logger.info(out,err)
            return 'upload_fin', {'result':False, 'msg':'Unzip the failure'}

        # todo: 验证断网处理
        try:
            return 'unzip_resp', {'result':True}
        except:
            return 'unzip_resp', {'result':False, 'msg':'Unzip the failure'}
    pass
pass

class RestartAgentHandler:

    def handle(self, ws, tid, wid, cmd, cid, param):

        path = 'Client.py'
        dir = os.path.dirname(path)
        cmd = ['python', 'Client.py', '&']
        os.execvp(cmd[0], cmd)
        return 'rs_ag_resp', {'result':True}

    pass
pass


class UpgradeAgentHandler:

    def handle(self, ws, tid, wid, cmd, cid, param):

        url = param['url']
        path = r'./upd.zip'

        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                return 'download_resp', {'result': False, 'msg': '已存在该文件，删除失败'}

        logger.info('upgrade agent ready to download')
        logger.info('url is %s, path is %s' % (url, path))

        if support_chunk(url):
            logger.info('upgrade support chunk')
            result = chunk_download(url, path)
        else:
            logger.info('upgrade not support chunk')
            result = normal_download(url, path)

        logger.info('upgrade download result is %s'%result)
        if result:
            unzip_dir = r'./'
            cmd = ['7za', 'x', '-y', path, r'-o%s'%unzip_dir]
            p = subprocess.Popen(' '.join(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)
            out,err = p.communicate()
            logger.info('unzip out: '+ out)
            if err or 'Everything is Ok' not in out:
                #压缩出错
                logger.info(out,err)
                return 'rs_ag_resp', {'result':False}

            logger.info('unzip success ready to execvp')
            cmd = ['python', 'Client.py', '&']
            os.execvp(cmd[0], cmd)
            return 'upd_ag_resp', {'result':True}
        return 'upd_ag_resp', {'result': False}

    pass
pass



class UploadHandler:
    def handle(self, ws, tid, wid, cmd, cid, param):
        url = param['url']
        path_arr = param['paths']
        
        if not os.path.exists('zip/'):
            os.makedirs('zip')
           
        fn = 'zip/'+str(uuid.uuid4())+ '.7z'
        cmd = ['7za', 'a', fn]
        path_arr[0] = path_arr[0].encode("gbk")
        cmd.extend(path_arr)
        p = subprocess.Popen(' '.join(cmd),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE)
        
        out,err = p.communicate()
        if err or 'Everything is Ok' not in out:
            #压缩出错
            logger.info(out,err)
            return 'upload_fin', {'result':False}

        # todo: 验证断网处理
        try:
            requests.post(url,files={'zipfile': open(fn, 'rb')})
            return 'upload_fin', {'result':True}
        except:
            return 'upload_fin', {'result':False}

    pass

class RenameHandler:
    def handle(self, ws, tid, wid, cmd, cid, param):
        paramJson = json.loads(param)
        fullPath = paramJson['fullName']
        newValue = paramJson['newValue']
        oldValue = paramJson['oldValue']
        newPath = fullPath.replace(oldValue, newValue)
        try:
            os.rename(fullPath, newPath)
            if os.path.exists(newPath):
                return 'rename_resp', {'result': True}
            else:
                return 'rename_resp', {'result': False, 'msg': '重命名不成功'}
        except Exception as e:
            return 'rename_resp', {'result': False, 'msg': e.message}
        pass

class DeleteHandler:
    def handle(self, ws, tid, wid, cmd, cid, param):
        paramJson = json.loads(param)
        fullPath = paramJson['filePath']
        try:
            for path in fullPath:
                os.remove(path)
            return 'delete_resp', {'result': True}
        except Exception as e:
            return 'delete_resp', {'result': False, 'msg': e.message}
        pass


class DownloadHandler:
    def __init__(self):
        self._downloader = None
        self.download_fin_callback = None
        self.size = 0
        self.filename = ''

    pass

    def handle(self, ws, tid, wid, cmd, cid, param):
        url = (param['url'].decode('utf-8'))
        path = (param['path'].decode('utf-8'))

        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                return 'download_resp', {'result': False, 'msg': '已存在该文件，删除失败'}

        if support_chunk(url):
            result = chunk_download(url, path)
        else:
            result = normal_download(url, path)

        return 'download_resp', {'result': result, 'msg': 'download handle finish!'}

        # send message to t_server after download finish

    pass

    def fin_callback(self, cmd, cid):
        pass

    pass


pass
