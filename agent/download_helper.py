# -*- coding: utf-8 -*
import re
import requests
import os
import time
import retrying
import logging
import logging.handlers

from retrying import retry

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

def normal_download(url, filename):
    try:
        r = requests.get(url)
        with open(filename, 'ab+') as f:
            f.write(r.content)
    except:
        return False
    return True


pass


@retry(stop_max_attempt_number=100, wait_random_min=5000, wait_random_max=10000)
def chunk_download(url, filename, headers={}):
    finished = False
    tmp_filename = filename + '.downtmp'
    result = False

    with open(tmp_filename, 'ab+') as f:
        size = os.stat(tmp_filename).st_size
        headers['Range'] = "bytes=%d-" % (size,)

        r = requests.get(url, stream=True, verify=False, headers=headers)
        total = __get_length(r)
        if total > 0:
            logging.info("[%s] Size: %dKB" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), total / 1024))
        else:
            logging.info("[+] Size: None")
        start_t = time.time()

        f.seek(size)
        f.truncate()
        try:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    size += len(chunk)
                    f.flush()
                elif (not chunk and size < total):  # 读不到数据但是长度和content-length不等
                    time.sleep(5)
                    continue

            finished = True
            spend = time.time() - start_t
            logging.info('Download Finished!\nTotal Time: %ss\n' % spend)
            result = True
        except Exception as e:
            logging.info(e.message)
            logging.info("\nDownload pause.\n")
            raise e
            # retry 会重试100次

    if finished:
        if os.path.exists(tmp_filename):
            os.rename(tmp_filename, tmp_filename.replace('.downtmp', ''))
    else:
        os.remove(tmp_filename)
    return result


pass


# 服务器是否支持断点续传
def support_chunk(url):
    return False
    headers = {
        'Range': 'bytes=0-4'
    }
    try:
        r = requests.head(url, headers=headers)
        code = r.status_code

        # 不是206就是不支持
        if code != 206:
            return False

        return True
    except:
        pass
    return False
pass

def __get_length(r):
    try:
        crange = r.headers['content-range']
        return int(re.match(ur'^bytes 0-4/(\d+)$', crange).group(1))
    except:
        pass

    try:
        return int(r.headers['content-length'])
    except:
        pass

    return 0
pass
