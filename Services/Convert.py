"""医学图像上传与处理服务"""
from tslide.TslideDeepZoomGenerator import DeepZoomGenerator as TSDeepZoomer
from multipart import FormParser, create_form_parser
from sanic.exceptions import NotFound, ServerError
from openslide.deepzoom import DeepZoomGenerator
from openslide import ImageSlide, open_slide
from sanic import Sanic, response
from PIL import Image, ImageDraw
from openslide import OpenSlide
from tslide import TSlide
import pydicom as dicom
from io import BytesIO
import pytesseract
import numpy as np
import SimpleITK
import requests
import aiofiles
import json
import uuid
import math
import os

app = Sanic()

tif_path_cache = {}
slide_cache = {}
jwt_cache = {}
StorgePath = '/storge/'

HOST = os.environ.get('tct_backend_host', 'backend:8000')

"""全局变量，标明需要转换的dcm文件的相对路径"""


def get_jwt(information_id):
    if information_id not in jwt_cache:
        login_url = 'http://{HOST}/api/v1/logins/'.format(HOST=HOST)
        response = requests.post(
            login_url, json={'username': 'convert', 'password': 'tsimage357753'})
        if response.status_code != 200:
            raise Exception('can not logins', response.content)
        jwt_cache[information_id] = 'JWT {}'.format(response.json()['token'])
    return jwt_cache[information_id]


def get_slide(tif_path):
    if tif_path in slide_cache:
        slide = slide_cache[tif_path]
    else:
        try:
            slide = OpenSlide(tif_path)
        except Exception as e:
            slide = TSlide(tif_path)
        slide_cache[tif_path] = slide
    return slide


def get_path_by(indentifier):
    indentifier = str(uuid.UUID(indentifier))
    file_dir = os.path.join(StorgePath, indentifier)
    metadata = None
    for file in os.listdir(file_dir):
        file_path = os.path.join(file_dir, file)
        if file.startswith('metadata') and not file.startswith('.'):
            with open(file_path, 'r') as metadata_file:
                metadata = json.loads(metadata_file.read())
    if metadata:
        filename = metadata.get('filename', metadata.get('Filename', None))
        indentifier = metadata.get('indentifier', metadata.get('Indentifier', None))
        if indentifier == indentifier:
            return os.path.join(file_dir, filename)
    else:
        raise Exception('No metadata file found, Can not read the file useing indentifier, please see Convert:get_path_by:indentifier function')


def get_path(information_id, request):
    if information_id in tif_path_cache:
        tif_path = tif_path_cache[information_id]
    else:
        jwt = request.headers.get('Authorization', None)
        if not jwt:
            jwt = get_jwt(information_id)
        information_url = 'http://{HOST}/api/v1/informations/{information_id}/'.format(
            HOST=HOST, information_id=information_id)
        response = requests.get(information_url,  headers={
                                'Authorization': '{}'.format(jwt)})
        if response.status_code != 200:
            raise Exception('can not get resource', response.content)
        tif_path = response.json()['resource']['files']['scanning_film']
        tif_path_cache[information_id] = tif_path
    return(tif_path)


def file(bytes, mime_type, filename):
    """http 文件response"""
    headers = {}
    headers.setdefault(
        'Content-Disposition',
        'attachment; filename="{}"'.format(filename))

    return response.HTTPResponse(status=200,
                                 headers=headers,
                                 content_type=mime_type,
                                 body_bytes=bytes)


async def tiles(request, x, y, z, information_id):
    """TIFF图像瓦片化算法"""
    slide = get_slide(get_path(information_id, request))
    tiles_y = 256
    tiles_x = 256
    z = slide.level_count + 1 - z
    dim = slide.level_dimensions
    #factor_x = dim[0][0] / dim[z][0]
    #factor_y = dim[0][1] / dim[z][1]
    factor_y = factor_x = slide.level_downsamples[z]
    raw_x = factor_x * tiles_x * x
    raw_y = factor_y * tiles_y * y
    return slide.read_region((int(raw_x), int(raw_y)), z, (tiles_x, tiles_y))

@app.route('/convert/ocr/<indentifier>')
async def ocr(request, indentifier):
    slide = get_slide(get_path_by(indentifier))
    associated_images = slide.associated_images.get('label', None)
    text=pytesseract.image_to_string(associated_images, lang='chi_sim')
    text_list = text.split('\n')
    return response.json({
        "indentifier": indentifier,
        "texts": text_list
        })

@app.route('convert/associated_images/<indentifier>/<label>/<format>')
async def thumbnail(request, indentifier, label, format):
    # <label>: marco label thumbnail
    slide = get_slide(get_path_by(indentifier))
    associated_images = slide.associated_images.get(label, None)
    bio = BytesIO()
    associated_images.save(bio, format)
    image_bytes = bio.getvalue()
    return file(bytes=image_bytes, mime_type='image/{}'.format(format.lower()), filename='associated_images_{indentifier}.{format}'.format(indentifier=indentifier, format=format))


@app.route('convert/thumbnail/<indentifier>/<x:int>_<y:int>.<format:[A-z]+>')
async def thumbnail(request, indentifier, x, y, format):
    slide = get_slide(get_path_by(indentifier))
    thumbnail = slide.get_thumbnail((x, y))
    bio = BytesIO()
    thumbnail.save(bio, format)
    image_bytes = bio.getvalue()
    return file(bytes=image_bytes, mime_type='image/{}'.format(format.lower()), filename='thumbnail_{indentifier}_{x}_{y}.{format}'.format(indentifier=indentifier, x=x, y=x, format=format))


@app.route('convert/tiles_dzi/<indentifier>/')
async def tiles_dzi(request, indentifier):
    slide = get_slide(get_path_by(indentifier))
    if isinstance(slide, TSlide):
        zoomer = TSDeepZoomer(slide).get_dzi('jpeg')
    else:
        zoomer = DeepZoomGenerator(slide).get_dzi('jpeg')
    return response.html(zoomer)


@app.route('convert/tiles_dzi/<indentifier>_files/<z:int>/<x:int>_<y:int>.<format:[A-z]+>')
async def tiles_png(request, indentifier, z, x, y, format):
    slide = get_slide(get_path_by(indentifier))
    x = int(x)
    y = int(y)
    z = int(z)
    bio = BytesIO()
    if isinstance(slide, TSlide):
        tiles_image = TSDeepZoomer(slide).get_tile(z, (x, y))
    else:
        tiles_image = DeepZoomGenerator(slide).get_tile(z, (x, y))
    tiles_image.save(bio, 'PNG')
    image_bytes = bio.getvalue()
    return file(bytes=image_bytes, mime_type='image/png', filename='tile_{x}_{y}_{z}'.format(x=x, y=x, z=z))


@app.route("convert/tiles/<information_id>/<x>/<y>/<z>")
async def tiles_request(request, information_id, x, y, z):
    """TIFF图像瓦片化请求体"""
    ix = int(x)
    iy = int(y)
    iz = int(z)

    tiles_image = await tiles(ix, iy, iz, information_id=information_id)
    bio = BytesIO()
    tiles_image.save(bio, 'PNG')
    image_bytes = bio.getvalue()
    return file(bytes=image_bytes, mime_type='image/png', filename='tile_' + x + y + z)


@app.route("convert/raw_tiles/<indentifier>/<x>/<y>/<w>/<h>/<format:[A-z]+>")
async def raw_tiles_request(request, indentifier, x, y, w, h, format):
    """TIFF图像瓦片化请求体"""
    slide = get_slide(get_path_by(indentifier))
    raw_width = slide.dimensions[0]
    tile_width = float(w)
    tile_height = float(h)
    x = float(x)
    y = float(y)
    tilexy = (int(x*raw_width), int(y*raw_width))
    tilewh = (int(tile_width*raw_width), int(tile_height*raw_width))
    tile_image = slide.read_region(tilexy, 0, tilewh)
    bio = BytesIO()
    tile_image.save(bio, format)
    return file(bytes=bio.getvalue(), mime_type='image/png', filename='tile_{x}_{y}_{w}_{h}.{f}'.format(x=x, y=y, w=w, h=h, f=format))


@app.route("convert/tiles/info/<information_id>")
def tilesinfo(request, information_id):
    """TIFF图像信息请求体"""
    slide = get_slide(get_path(information_id, request))
    wh_list = slide.dimensions
    zoom = slide.level_count
    return response.json({'min_zoom': 1, 'max_zoom': zoom, 'img': wh_list})


async def _dicom(filePathName):
    """DICOM图像源数据读取"""
    dm = SimpleITK.GetArrayFromImage(SimpleITK.ReadImage(filePathName))
    arr = dm[0]
    image_array = ((arr - arr.min()) / (arr.max() - arr.min())) * 256
    image_array = image_array.astype(np.int8)
    return image_array


@app.route("convert/dicom/draw/<information_id>/<x>/<y>/<radius>")
async def dicom_draw(request, information_id, x, y, radius):
    """DICOM图像圆形标准请求体"""
    filePathName = get_path(information_id, request)
    bio = BytesIO()
    image_array = await _dicom(filePathName)

    # 如果是二维点阵，先把它变为三维，再创建图片
    if len(image_array.shape) == 2:
        # 先扩展一个维度
        image_array = image_array[:, :, np.newaxis]
        # 然后让最后面的那个维度，元素复制成3份
        image_array = np.tile(image_array, 3)

    # 通过点阵创建图片
    image = Image.fromarray(image_array, mode="RGB")

    zoom = 3
    x = int(float(x) * image.width) + zoom
    y = int(float(y) * image.height) + zoom
    radius = int(float(radius) * image.width / 2)

    start_point_x = x - radius
    start_point_y = y - radius
    end_potint_x = x + radius
    end_potin_y = y + radius

    start_angle = 0
    end_angle = 360

    draw = ImageDraw.Draw(image)
    # 问题区域的圆弧画成标准的红色
    draw.arc([start_point_x, start_point_y, end_potint_x,
              end_potin_y], start_angle, end_angle, fill='red')

    del draw
    image.save(bio, 'PNG')
    image_bytes = bio.getvalue()
    return file(bytes=image_bytes, mime_type='image/PNG', filename=information_id + '.png')


@app.route("convert/dicom/<information_id>")
async def dicom2png(request, information_id):
    """在调用这个函数时，本地的dcm文件会按规则转换为png文件，并提示下载"""
    filePathName = get_path(information_id, request)
    bio = BytesIO()
    image_array = await _dicom(filePathName)
    if len(image_array.shape) == 3:
        image = Image.fromarray(image_array, mode="RGB")
    else:
        image = Image.fromarray(image_array, mode="L")

    image.save(bio, 'PNG')
    image_bytes = bio.getvalue()

    return file(bytes=image_bytes, mime_type='image/PNG', filename=information_id + '.png')


async def _dicom_window(filePathName, c, r):
    """调节中心点和半径的核心函数"""
    # 第1步，得到表明原始振幅的二维数组
    dm = SimpleITK.GetArrayFromImage(SimpleITK.ReadImage(filePathName))
    arr = dm[0]

    # 第2步，根据中心点和半径，按照y = kx+b进行变换，并四舍五入到整数
    c = int(c)
    r = int(r)
    image_array = np.around(127.5 * arr / r - 127.5 * (c - r) / r + 0.00001)

    # 第3步，小于0和大于255的部分，都调整成边界值
    image_array = np.maximum(image_array, 0)
    image_array = np.minimum(image_array, 255)

    # 第4步，将浮点型的数转为整形
    image_array = image_array.astype(np.int8)

    return image_array


@app.route("convert/dicom/window/<information_id>/<c>/<r>")
async def dicom_window(request, information_id, c, r):
    """需要传入DICOM openid，中心点和半径，后两者需要为可以转成整形的数据"""
    filePathName = get_path(information_id, request)
    bio = BytesIO()
    image_array = await _dicom_window(filePathName, c, r)
    if len(image_array.shape) == 3:
        image = Image.fromarray(image_array, mode="RGB")
    else:
        image = Image.fromarray(image_array, mode="L")

    image.save(bio, 'PNG')
    image_bytes = bio.getvalue()

    return file(bytes=image_bytes, mime_type='image/PNG', filename=information_id + '.png')


@app.route("convert/dicom/info/<information_id>")
async def dicom_info(request, information_id):
    """需要传入DICOM openid，获取DICOM信息"""
    filePathName = get_path(information_id, request)
    dm = dicom.read_file(filePathName)
    ret = {}
    for tag in dm.dir():
        # maybe the datas in dir() is not reliable
        if tag not in ['PixelData', 'PixelPaddingValue']:
            if hasattr(dm, tag):
                content = getattr(dm, tag)
                ret.update({tag: content})
    return response.json(ret)


def page_get(next, res=None, *args, **kwargs):
    """调用RESTful接口时使用的分页器"""
    if not res:
        res = []
    next = requests.get(next, *args, **kwargs)
    res += next.json()['results']
    if next.status_code != 200:
        raise Exception('down load err')
    _next = next.json()['next']
    if _next:
        return page_get(_next, res, *args, **kwargs)
    return res


@app.route("convert/dicom/info/zip/<accession_id>")
async def dicom_info_zip(request, accession_id):
    """打包获取DICOM信息"""
    results = page_get('http://{host}:{port}/api/v1/accessions/{accession_id}/images/?limit=100'.format(
        host='backend',
        port='8000',
        accession_id=accession_id))
    res = {}
    for image in results:
        information_id = image['information_id']
        filePathName = get_path(information_id, request)
        dm = dicom.read_file(filePathName)
        ret = {}
        for tag in dm.dir():
            # maybe the datas in dir() is not reliable
            if tag not in ['PixelData', 'PixelPaddingValue']:
                if hasattr(dm, tag):
                    content = getattr(dm, tag)
                    ret.update({tag: content})
        res.update({information_id: ret})

    return response.json(res)


def get_chunk_name(uploaded_filename, chunk_number):
    return uploaded_filename + "_part_%03d" % chunk_number




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8100)
