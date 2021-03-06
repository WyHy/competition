import requests

from utils import get_jwt, HOST

HEADER = {"Authorization": "JWT %s" % get_jwt('convert')}


def disable_slide_validation():
    response = requests.get('http://%s/api/v1/images/all/' % HOST, headers=HEADER)
    if response.status_code == 200 and response.json():
        data = response.json()
        ids = []

        for obj in data:
            ids.append(obj['id'])

        image = {
            "is_valid": "NO",
        }

        for image_id in ids:
            response = requests.patch('http://%s/api/v1/images/all/%s/' % (HOST, image_id), json=image, headers=HEADER)
            if response.status_code == 200:
                pass
            else:
                print(response.json())


def remove_old_allocations():
    response = requests.get('http://%s/api/v1/missions/' % HOST, headers=HEADER)
    if response.status_code == 200 and response.json():
        data = response.json()
        ids = []

        for obj in data:
            ids.append(obj['id'])

        for mission_id in ids:
            response = requests.delete('http://%s/api/v1/missions/%s/' % (HOST, mission_id), headers=HEADER)
            if response.status_code == 204:
                pass
            else:
                print(response.json())


def remove_old_labels():
    response = requests.get('http://%s/api/v1/labels/' % HOST, headers=HEADER)
    if response.status_code == 200 and response.json():
        data = response.json()
        ids = []

        for obj in data:
            ids.append(obj['id'])

        for label_id in ids:
            response = requests.delete('http://%s/api/v1/labels/%s/' % (HOST, label_id), headers=HEADER)
            if response.status_code == 204:
                pass
            else:
                print(response.json())


def clean_slide_diagnose_result():
    response = requests.get('http://%s/api/v1/images/all/' % HOST, headers=HEADER)
    if response.status_code == 200 and response.json():
        data = response.json()
        ids = []

        for obj in data:
            ids.append(obj['id'])

        image = {
            "result_auto": "",
            "result_manual": "",
        }

        for image_id in ids:
            response = requests.patch('http://%s/api/v1/images/all/%s/' % (HOST, image_id), json=image, headers=HEADER)
            if response.status_code == 200:
                pass
            else:
                print(response.json())


def make_selected_valid(file_path):
    with open(file_path) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        for line in lines:
            image = None
            response = requests.get('http://%s/api/v1/images/all/?case_no=%s' % (HOST, line), headers=HEADER)
            if response.status_code == 200 and response.json():
                data = response.json()
                if data:
                    image = data[0]['id']
            else:
                raise Exception("NO TIFF NAMED %s" % line)

            data = {
                "is_valid": "YES",
                # "result_status": line,
            }

            response = requests.patch('http://%s/api/v1/images/all/%s/' % (HOST, image), json=data, headers=HEADER)
            if response.status_code == 200:
                pass
            else:
                print(response.json())
                break


if __name__ == '__main__':
    print("1=> disable_slide_validation")
    disable_slide_validation()

    print("2=> clean_slide_diagnose_result")
    clean_slide_diagnose_result()

    print("3=> remove_old_allocations")
    remove_old_allocations()

    print("4=> remove_old_labels")
    remove_old_labels()

    print("5=> make_selected_valid")
    file_path = "./ZHENGZHOU_COMPETITION_SLIDES.txt"
    make_selected_valid(file_path)
