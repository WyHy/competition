import queue
import time
from multiprocessing.managers import BaseManager

# 发送任务的队列:
import requests

from tools.utils import get_jwt, HOST

task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()


def return_task_queue():
    global task_queue
    return task_queue


def return_result_queue():
    global result_queue
    return result_queue


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


HEADER = {"Authorization": "JWT %s" % get_jwt('convert')}


def get_game_status():
    response = requests.get('http://%s/api/v1/game/' % HOST, headers=HEADER)
    if response.status_code == 200 and response.json():
        data = response.json()
        status = data['status']
        if status == "1":
            return 1
        else:
            return 0
    else:
        raise Exception(response.json())


if __name__ == '__main__':
    # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
    QueueManager.register('get_task_queue', callable=return_task_queue)
    QueueManager.register('get_result_queue', callable=return_result_queue)
    # 绑定端口5000, 设置验证码'abc':
    # window 需要设置ip地址为127.0.0.1
    # manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    # ubuntu 无需设置
    manager = QueueManager(address=('', 5000), authkey=b'abc')

    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    while 1:
        status = get_game_status()

        # 比赛开始
        if status == 1:
            # 获取图像id及图像名称
            response = requests.get('http://%s/api/v1/images/' % HOST, headers=HEADER)
            if response.status_code == 200 and response.json():
                data = response.json()

                # 添加任务
                for item in data:
                    print("Add task slide_id=%s" % item['id'])
                    task.put(item)

                # 获取任务结果
                task_count = len(task)
                result_count = 0
                while 1:
                    try:
                        r = result.get(timeout=10)
                        print('Result: %s' % r)

                        result_count += 1
                    except queue.Empty:
                        print("Waiting for Process Result.")

                    if result_queue == task_count:
                        break

                # 关闭任务控制中心
                manager.shutdown()
                print('master exit.')

                break

        else:
            print("Waiting for competition start ...")
            time.sleep(3)
