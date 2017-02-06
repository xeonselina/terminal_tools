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


class DirHandler:
    def handle(self, ws, tid, wid, cmd, cid, param):
        # get dir info
        msg = ''
        path = param['path']
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

            if 1:
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
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
        
        out,err = p.communicate()
        if err or 'Everything is Ok' not in out:
            #压缩出错
            print out,err
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


class DownloadHandler:
    def __init__(self):
        self._downloader = None
        self.download_fin_callback = None

    pass

    def handle(self, ws, tid, wid, cmd, cid, param):
        url = param['url']
        path = param['path']
        
        param = [r'F:\work\20451_publish\CIMC.EZ.Download\CIMC.EZ.Download.exe ', '-u', url, '-p', path, '-t', 'zip', '-i', '1']
        path = os.path.dirname(path)
        
        if not os.access(path, os.W_OK | os.X_OK):
            return 'download_resp', {'result': False, 'msg': '没有权限写入该文件夹'}

        def start_down(src, args, onExit):
            src._downloader = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE)
            src._downloader.wait()
            onExit(cmd, cid)
            return

        pass

        # send message to t_server
        t = threading.Thread(target=start_down, args=(self, param, self.fin_callback))
        t.start()

        return 'download_resp', {'result': True, 'msg': 'begin download'}

        # send message to t_server after download finish

    pass

    def fin_callback(self, cmd, cid):
        pass

    pass


pass
