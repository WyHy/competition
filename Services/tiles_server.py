from sanic import Sanic, response
from openslide import OpenSlide, ImageSlide, open_slide
from openslide.deepzoom import DeepZoomGenerator
from Aslide.aslide import Aslide
from Aslide.deepzoom import ADeepZoomGenerator
# from tslide.TslideDeepZoomGenerator import DeepZoomGenerator as TSDeepZoomer
from io import BytesIO
from PIL import Image
import os
import requests

app = Sanic()

tif_path_cache = {}
slide_cache = {}
jwt_cache = {}

HOST = 'localhost:8000'
USERNAME = 'convert'
# StorgePath = '/home/stimage/Development/DATA/RESOURCE/TIFFS'

def get_jwt(username):
    if username not in jwt_cache:
        login_url = 'http://%s/api/v1/auth_token/' % HOST
        response = requests.post(login_url, json={'username': 'convert', 'password': 'tsimage666'})
        if response.status_code != 200:
            raise Exception('can not logins', response.content)
        jwt_cache[username] = 'JWT {}'.format(response.json()['token'])

    return jwt_cache[username]


def get_path(image_id, request):
    if image_id in tif_path_cache:
        tif_path = tif_path_cache[image_id]
    else:
        jwt = request.headers.get('Authorization', None)
        if not jwt:
            jwt = get_jwt(USERNAME)

        tiff_url = 'http://%s/api/v1/images/?id=%s' % (HOST, image_id)

        response = requests.get(tiff_url,  headers={'Authorization': 'JWT {}'.format(jwt)})
        if response.status_code != 200:
            raise Exception('can not get resource', response.content)

        image_info = response.json()[0]
        tif_path = os.path.join(image_info['path'], image_info['name'])
        tif_path_cache[image_info['name']] = tif_path

    return tif_path


def get_slide(tif_path):
    basename = os.path.basename(tif_path)

    if basename in slide_cache:
        slide = slide_cache[basename]
    else:
        slide_cache[basename] = Aslide(tif_path)

    return slide


def file(bytes, mime_type, image_id):
    """http 文件response"""
    headers = {}
    headers.setdefault(
        'Content-Disposition',
        'attachment; image_id="{}"'.format(image_id))

    return response.HTTPResponse(status=200,
                                 headers=headers,
                                 content_type=mime_type,
                                 body_bytes=bytes)


@app.route('/tiles/<image_id>/')
async def tiles_dzi(request, image_id):
    slide = get_slide(get_path(image_id, request))
    try:
        zoomer = ADeepZoomGenerator(slide).get_dzi('jpeg')

        return response.html(zoomer)
    except Exception as e:
        return response.html(str(e))    


@app.route('/tiles/<image_id>_files/<z:int>/<x:int>_<y:int>.<format:[A-z]+>')
async def tiles_png(request, image_id, z, x, y, format):
    slide = get_slide(get_path(image_id, request))
    x = int(x)
    y = int(y)
    z = int(z)
    bio = BytesIO()

    tiles_image = ADeepZoomGenerator(slide).get_tile(z, (x, y))
    tiles_image.save(bio, 'jpeg')
    image_bytes = bio.getvalue()
    return file(bytes=image_bytes, mime_type='image/jpeg', image_id='tile_{x}_{y}_{z}'.format(x=x, y=x, z=z))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8073)