from datetime import time
import requests
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
from .tools import urltoBase64
from .baidu_api import addface,facedetect,gettoken,getuserlist,getgrouplist,faceSearch,faceSearch_multi

# Create your views here.
from Photoalbum.models import Img

def getAllimg(request):
    json={}#最终返回的json
    jsonlist=[]#列表
    imglist=[]
    data = Img.objects.all().order_by('-time')  #等价于select * from img  (按时间倒序排序)
    temptime=data[0].time
    index=0
    for item in data:#测试仅取少量数据
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
    l=os.listdir(input)
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

#上传单张图片
def uploadimg(request):
    img = request.FILES.get('imgs')
    filename=request.FILES['imgs'].name
    print(filename)
    #file_content = img.read()
    #uName = request.POST.get('uName')
    #print('img:', file_content)
    ImageDate = datetime.now().strftime('%Y-%m-%d')
    m = Img(time=ImageDate)
    m.img.save(name=filename, content=File(img))
    m.save()
    return HttpResponse('add ok')

def face_process(request):
    username='01'  #登陆的用户名
    data = Img.objects.all().order_by('-time')
    at=gettoken()
    for item in data[:20]:
        print(item.img_id,item.img)
        base64_data=urltoBase64('./'+str(item.img))
        result=facedetect(base64_data,at)
        if result['error_code']==0:
            if result['result']['face_num']==1:
                result=faceSearch(base64_data,at,username)
                if result['error_code']==0:
                    group_id = result['result']['user_list'][0]['group_id']
                    user_id = result['result']['user_list'][0]['user_id']
                    ft = result['result']['face_token']
                    if result['result']['user_list'][0]['score']>=80:
                        addface(at,group_id,user_id,ft)
                    else:
                        userlistsize=len(getuserlist(at,username))
                        addface(at, username, str(userlistsize), ft)
            else:
                result=faceSearch_multi(base64_data,at,username)
                if result['error_code'] == 0:
                    facelist=result['result']['face_list']
                    for face in facelist:
                        ft=face['face_token']
                        group_id = face['user_list'][0]['group_id']
                        user_id = face['user_list'][0]['user_id']
                        score = face['user_list'][0]['score']
                        if score>=80:
                            addface(at,group_id,user_id,ft)
                        else:
                            userlistsize = len(getuserlist(at, username))
                            addface(at, username, str(userlistsize), ft)
    return HttpResponse('deal ok')



