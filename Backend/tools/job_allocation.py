import requests
import random

from utils import get_jwt, HOST


def get_job_list():
    """
    获取 病理图像信息列表
    :return:
    """
    header = {"Authorization": "JWT %s" % get_jwt('convert')}
    response = requests.get('http://%s/api/v1/images/' % HOST, headers=header)
    if response.status_code == 200:
        ids = [item['id'] for item in response.json()]
        return ids
    else:
        raise Exception(response.json())


def get_user_list():
    """
    获取 用户列表
    :return:
    """
    header = {"Authorization": "JWT %s" % get_jwt('convert')}
    response = requests.get('http://%s/api/v1/profiles/?type=1' % HOST, headers=header)
    if response.status_code == 200:
        ids = [item['id'] for item in response.json()]
        return ids
    else:
        raise Exception(response.json())


def do_job_allocate():
    job_ids = get_job_list()
    user_ids = get_user_list()

    header = {"Authorization": "JWT %s" % get_jwt('convert')}

    # 列表shuffle，现阶段按序排列，以对应医生答题顺序
    # random.shuffle(job_ids)

    delta = 10
    lst = [job_ids[i: i + delta] for i in range(0, len(job_ids), delta)]

    for index, user in enumerate(user_ids):
        print("Allocating jobs to user-%s" % user)
        items = lst[index]
        for item in items:
            job = {
                'profile': user,
                'tiff': item,
            }

            response = requests.post('http://%s/api/v1/missions/' % HOST, json=job, headers=header)
            if response.status_code == 201:
                pass
            else:
                raise Exception(response.json())


if __name__ == '__main__':
    do_job_allocate()
    # print("Image count: %s" % len(data))
