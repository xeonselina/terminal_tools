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

config = {}
execfile('app.conf', config)

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
        cmd = ['7za', 'x', '-y', path]
        p = subprocess.Popen(' '.join(cmd), shell=True, cwd=dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE)

        out,err = p.communicate()
        print 'unzip out: '+ out
        if err or 'Everything is Ok' not in out:
            #压缩出错
            print out,err
            return 'upload_fin', {'result':False}

        # todo: 验证断网处理
        try:
            return 'unzip_resp', {'result':True}
        except:
            return 'unzip_resp', {'result':False}
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
        self.total = 0
        self.size = 0
        self.filename = ''

    pass

    def handle(self, ws, tid, wid, cmd, cid, param):
        url = (param['url'].decode('utf-8'))
        path = (param['path'].decode('utf-8'))

        '''
        param = [config['down_tool'], '-u', url, '-p', path, '-t', 'zip', '-i', '1']
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
        '''

        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                return 'download_resp', {'result': False, 'msg': '已存在该文件，删除失败'}

        if self.support_chunk(url):
            result = self.chunk_download(url, path)
        else:
            result = self.normal_download(url, path)

        return 'download_resp', {'result': result, 'msg': 'download handle finish!'}

        # send message to t_server after download finish

    pass

    def fin_callback(self, cmd, cid):
        pass

    pass

    def normal_download(self, url, filename):
        try:
            r = requests.get(url)
            with open(filename,'ab+') as f:
                f.write(r.content)
        except:
            return False
        return True
    pass

    def chunk_download(self, url, filename, headers={}):
        finished = False
        tmp_filename = filename + '.downtmp'
        size = self.size
        total = self.total
        result = False

        if self.support_chunk(url):
            try:
                with open(tmp_filename, 'rb') as fin:
                    self.size = int(fin.read())
                    size = self.size + 1
            except:
                pass
            finally:
                headers['Range'] = "bytes=%d-" % (self.size,)

        r = requests.get(url, stream=True, verify=False, headers=headers)
        if(total >0):
            print "[%s] Size: %dKB" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), total/1024)
        else:
            print "[+] Size: None"
        start_t = time.time()
        with open(tmp_filename, 'ab+') as f:
            f.seek(self.size)
            f.truncate()
            try:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        size += len(chunk)
                        f.flush()
                    #print '\b' * 64 + 'time: %s, Now: %d, Total: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), size, total)
                finished = True
                spend = time.time() - start_t
                speed = int((size - self.size) / 1024 / spend)
                print('\nDownload Finished!\nTotal Time: %ss, Download Speed: %sk/s\n' % (spend, speed))
                result = True
            except Exception as e:
                print e.message
                print "\nDownload pause.\n"
            finally:
                if not finished:
                    with open(tmp_filename, 'wb') as ftmp:
                        ftmp.write(str(size))
        if finished:
            if os.path.exists(tmp_filename):
                os.rename(tmp_filename, tmp_filename.replace('.downtmp', ''))
        else:
            os.remove(tmp_filename)
        return result
        pass

    # 服务器是否支持断点续传
    def support_chunk(self, url):
        headers = {
            'Range': 'bytes=0-4'
        }
        try:
            r = requests.head(url, headers=headers)
            crange = r.headers['content-range']
            self.total = int(re.match(ur'^bytes 0-4/(\d+)$', crange).group(1))
            return True
        except:
            pass
        try:
            self.total = int(r.headers['content-length'])
        except:
            self.total = 0
        return False
    pass

pass
