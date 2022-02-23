import base64
import os
from PIL import Image

def urltoBase64(url):
    url=resize_image(url)  #减小尺寸
    url=compress_image(url)  #压缩大小
    with open(url,'rb') as f:
        base64_data = base64.b64encode(f.read())
        data=base64_data.decode()
        return data

def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024

def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile

def compress_image(infile, outfile='./static/temp', maxkb=2000, step=20, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param maxkb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """

    outfile=outfile+infile[infile.rfind('.'):]
    o_size = get_size(infile)
    if o_size <= maxkb:
        return infile
    #outfile = get_outfile(infile, outfile)
    while o_size > maxkb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile

def resize_image(infile, outfile='./static/temp'):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    outfile=outfile+infile[infile.rfind('.'):]
    maxw = 1920
    maxh = 1080
    img = Image.open(infile)
    img_width, img_height = img.size
    while img_width > maxw or img_height > maxh:
        img_width=int(img_width * 0.2)
        img_height=int(img_height * 0.2)
    img = img.resize((img_width,img_height), Image.ANTIALIAS)
    img.save(outfile)
    return outfile

