from datetime import time

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
import os
from PIL import Image
import time
from time import strftime
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.files import File


# Create your views here.
from Photoalbum.models import Img

def getAllimg(request):
    json={}#最终返回的json
    jsonlist=[]#列表
    imglist=[]
    data = Img.objects.all().order_by('-time')  #等价于select * from img  (按时间倒序排序)
    temptime=data[0].time
    index=0
    for item in data[:100]:#测试仅取少量数据
        if item.time!=temptime:
            time_json_obj={"time":str(temptime),"imglist":imglist}
            jsonlist.append(time_json_obj)
            temptime = item.time
            imglist = []
        jsonobj={"id":item.img_id,"index":index, "img":str(item.img),"time":item.time, "describe":item.describe}#每条记录转换成json对象
        imglist.append(jsonobj) #json对象添加到列表
        index+=1
    time_json_obj = {"time": str(temptime), "imglist": imglist}
    jsonlist.append(time_json_obj)

    json["imgs"]=jsonlist #图片列表
    return JsonResponse(json,content_type="application/json; charset=UTF-8")

def addimg(request):#只是测试，不是正式的添加图片接口
    from pathlib import Path
    input = '/Users/zerotwo/Pictures/xr photo/相机胶卷' #修改的目录
    # 切换目录
    #os.chdir(input)
    l=os.listdir(input)[:100]
    # 遍历目录下所有的文件
    for image_name in l:
        print(image_name)
        imgPath=os.path.join(input,image_name)
        times=time.gmtime(os.path.getmtime(imgPath))
        ImageDate = time.strftime('%Y-%m-%d',times)
        print(ImageDate)
        with open(imgPath,'rb') as imgf:
            m=Img(time=ImageDate)
            m.img.save(name=image_name,content=File(imgf))
            m.save()
        
    return HttpResponse('add ok')
