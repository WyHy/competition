import requests

from utils import get_jwt, HOST

HEADER = {"Authorization": "JWT %s" % get_jwt('convert')}


def disable_slide_validation():
    response = requests.get('http://%s/api/v1/images/' % HOST, headers=HEADER)
    if response.status_code == 200 and response.json():
        data = response.json()
        ids = []

        for obj in data:
            ids.append(obj['id'])

        image = {
            "is_valid": "NO",
        }

        for image_id in ids:
            response = requests.patch('http://%s/api/v1/images/%s' % (HOST, image_id), json=image, headers=HEADER)
            if response.status_code == 200:
                pass
            else:
                print(response.json())


def clean_slide_diagnose_result():
    response = requests.get('http://%s/api/v1/images/' % HOST, headers=HEADER)
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
            response = requests.patch('http://%s/api/v1/images/%s' % (HOST, image_id), json=image, headers=HEADER)
            if response.status_code == 200:
                pass
            else:
                print(response.json())


def make_selected_valid(file_path):
    with open(file_path) as f:
        lines = [line.replace("\n", "") for line in f.readlines()]

        for slide_name in lines:
            image = None
            for item in ['.kfb', '.tif']:
                response = requests.get('http://%s/api/v1/images/?name=%s' % (HOST, slide_name + item), headers=HEADER)
                if response.status_code == 200 and response.json():
                    data = response.json()
                    if data:
                        image = data[0]['id']
                        break
            else:
                raise Exception("NO TIFF NAMED %s" % slide_name)

            data = {
                "is_valid": "YES",
            }

            response = requests.patch('http://%s/api/v1/images/%s' % (HOST, image), json=data, headers=HEADER)
            if response.status_code == 200:
                pass
            else:
                print(response.json())


if __name__ == '__main__':
    disable_slide_validation()
    clean_slide_diagnose_result()

    file_path = ""
    make_selected_valid(file_path)

