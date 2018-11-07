import csv
import os

import requests

from utils import get_jwt, HOST


def read_and_update(path):
    header = {"Authorization": "JWT %s" % get_jwt('convert')}

    with open(path) as f:
        tiff_name = os.path.splitext(os.path.basename(path))[0]
        tiff_name = tiff_name.replace("_clas", '')

        print("Processing on %s..." % tiff_name)

        image = None
        for item in ['.kfb', '.tif']:
            response = requests.get('http://%s/api/v1/images/?name=%s' % (HOST, tiff_name + item), headers=header)
            if response.status_code == 200 and response.json():
                data = response.json()
                if data:
                    image = data[0]['id']
                    break
        else:
            raise Exception("NO TIFF NAMED %s" % tiff_name)

        reader = csv.reader(f, delimiter=',')
        next(reader)

        for line in reader:
            x_y, label_yolo, accuracy_yolo, label_xception, accuracy_xception, xmin, ymin, xmax, ymax = line
            x0, y0 = x_y.split('_')
            x0, y0, accuracy, xmin, ymin, xmax, ymax = int(x0), int(y0), float(accuracy_xception), float(xmin), float(ymin), float(xmax), float(ymax)
            x, y, w, h = x0 + xmin, y0 + ymin, xmax - xmin, ymax - ymin

            label = {
                'image': image,
                'cell_type': label_xception,
                'accuracy': accuracy,
                'x': x,
                'y': y,
                'w': w,
                'h': h,
                'source_type': "AI",
            }

            response = requests.post('http://%s/api/v1/labels/' % HOST, json=label, headers=header)
            if response.status_code == 201:
                pass
            else:
                raise Exception(response.json())


if __name__ == '__main__':
    dir_path = 'C:/Users/graya/Desktop/META'
    files = os.listdir(dir_path)
    for file in files:
        if file.endswith('_clas.csv'):
            read_and_update(os.path.join(dir_path, file))
