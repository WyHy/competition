"""
TIFF 文件变动嗅探器
用于检测指定目录内文件变动
"""

import os

import pyinotify
import requests

from utils import get_jwt, HOST

WATCH_PATH = '/home/stimage/Development/DATA/TEST_DATA'

if not WATCH_PATH:
    print("The WATCH_PATH setting MUST be set.")
    exit()
else:
    if os.path.exists(WATCH_PATH):
        print('Found watch path: path=%s.' % (WATCH_PATH))
    else:
        print('The watch path NOT exists, watching stop now: path=%s.' % (WATCH_PATH))
        exit()

ACCEPTED_PATHOLOGY_IMAGE_TYPES = ['.tif', '.kfb']


# 事件回调函数
class OnIOHandler(pyinotify.ProcessEvent):
    # 重写文件写入完成函数
    def process_IN_CLOSE_WRITE(self, event):
        # logging.info("create file: %s " % os.path.join(event.path, event.name))
        # 处理成小图片，然后发送给grpc服务器或者发给kafka
        file_path = os.path.join(event.path, event.name)
        print('文件完成写入', file_path)

        basename, postfix = os.path.splitext(event.name)
        if postfix in ACCEPTED_PATHOLOGY_IMAGE_TYPES:
            image = {
                "name": event.name.replace(" ", "-"),
                "path": event.path,
                "status": "CREATED",
            }

            header = {"Authorization": "JWT %s" % get_jwt('convert')}
            response = requests.post('http://%s/api/v1/images/' % HOST, json=image, headers=header)
            if response.status_code == 201:
                pass
            else:
                print(response.json())

    # 重写文件删除函数
    def process_IN_DELETE(self, event):
        print("文件删除: %s " % os.path.join(event.path, event.name))

    # 重写文件改变函数
    def process_IN_MODIFY(self, event):
        print("文件改变: %s " % os.path.join(event.path, event.name))

    # 重写文件创建函数
    def process_IN_CREATE(self, event):
        print("文件创建: %s " % os.path.join(event.path, event.name))


def auto_compile(path='.'):
    wm = pyinotify.WatchManager()
    # mask = pyinotify.EventsCodes.ALL_FLAGS.get('IN_CREATE', 0)
    # mask = pyinotify.EventsCodes.FLAG_COLLECTIONS['OP_FLAGS']['IN_CREATE']          # 监控内容，只监听文件被完成写入
    mask = pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE
    notifier = pyinotify.ThreadedNotifier(wm, OnIOHandler())  # 回调函数
    notifier.start()
    wm.add_watch(path, mask, rec=True, auto_add=True)
    print('Start monitoring %s' % path)
    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            break


if __name__ == "__main__":
    auto_compile(WATCH_PATH)
    print('monitor close')
    # print(get_jwt('1'))
