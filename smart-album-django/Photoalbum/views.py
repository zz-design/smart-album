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
from Photoalbum.tools import urltoBase64
from Photoalbum.baidu_api import addface,facedetect,gettoken,getuserlist,getgrouplist,faceSearch,faceSearch_multi,getuserface

# Create your views here.
from Photoalbum.models import Img,Face,User,Person_face,Group_person

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
    img_process(m)
    return HttpResponse('add ok')

def img_process(item):
    user='1'  #登陆用户的id
    at=gettoken()
    imgid = item.img_id
    print(imgid,item.img)
    base64_data=urltoBase64('./'+str(item.img))
    result=facedetect(base64_data,at)
    if result['error_code']==0:
        if result['result']['face_num'] ==1:
            ft = result['result']['face_list'][0]['face_token']
            result=faceSearch(base64_data,at,user)
            if result['error_code']==222207:
                userlistsize = len(getuserlist(at, user))
                user_id = str(userlistsize)
                if Group_person.objects.filter(group_id=User.objects.filter(u_id=eval(user)).first(),person_id=user_id).first() == None:
                    # 创建一个新person
                    person = Group_person(group_id=User.objects.filter(u_id=eval(user)).first(),
                                          person_id=user_id)
                    person.save()
                r = addface(at, user, user_id, ft)
                if r['error_code']==0:
                    if Face.objects.filter(face_token=ft).first() == None:
                        face = Face(face_token=ft, img_id=Img.objects.filter(img_id=imgid).first())
                        face.save()
                    person_face = Person_face(group_id=User.objects.filter(u_id=eval(user)).first() ,person_id=user_id,
                                              face_id=Face.objects.filter(face_token=ft).first())
                    person_face.save()

            elif result['error_code']==0:
                group_id = result['result']['user_list'][0]['group_id']
                user_id = result['result']['user_list'][0]['user_id']
                ft = result['result']['face_token']
                if result['result']['user_list'][0]['score']>=70:
                    r=addface(at,group_id,user_id,ft)
                else:
                    userlistsize=len(getuserlist(at,user))
                    user_id=str(userlistsize)
                    if Group_person.objects.filter(group_id=User.objects.filter(u_id=eval(group_id)).first(),person_id=user_id).first() == None:
                        # 创建一个新person
                        person = Group_person(group_id=User.objects.filter(u_id=eval(group_id)).first(),
                                              person_id=user_id)
                        person.save()
                    r=addface(at, group_id, user_id, ft)
                    flag=0
                if r['error_code']==0:
                    if Face.objects.filter(face_token=ft).first() == None:
                        face = Face(face_token=ft, img_id=Img.objects.filter(img_id=imgid).first())
                        face.save()
                    person_face = Person_face(group_id=User.objects.filter(u_id=eval(group_id)).first() ,person_id=user_id,
                                              face_id=Face.objects.filter(face_token=ft).first())
                    person_face.save()
        else:
            result=faceSearch_multi(base64_data,at,user)
            if result['error_code'] == 0:
                facelist=result['result']['face_list']
                for face in facelist:
                    ft=face['face_token']
                    group_id = face['user_list'][0]['group_id']
                    user_id = face['user_list'][0]['user_id']
                    score = face['user_list'][0]['score']
                    if score>=80:
                        r=addface(at,group_id,user_id,ft)
                    else:
                        userlistsize = len(getuserlist(at, user))
                        user_id = str(userlistsize)
                        if Group_person.objects.filter(group_id=User.objects.filter(u_id=eval(group_id)).first(),person_id=user_id).first() == None:
                            # 创建一个新person
                            person = Group_person(group_id=User.objects.filter(u_id=eval(group_id)).first(),
                                                  person_id=user_id)
                            person.save()
                        r = addface(at, group_id, user_id, ft)
                    if r['error_code'] == 0:
                        if Face.objects.filter(face_token=ft).first() == None:
                            face = Face(face_token=ft, img_id=Img.objects.filter(img_id=imgid).first())
                            face.save()
                        person_face = Person_face(group_id=User.objects.filter(u_id=eval(group_id)).first(),
                                                  person_id=user_id,
                                                  face_id=Face.objects.filter(face_token=ft).first())
                        person_face.save()
    return HttpResponse('deal ok')


def face_process(request):
    user='1'  #登陆用户的id
    data = Img.objects.all().order_by('-time')
    at=gettoken()
    for item in data :
        imgid = item.img_id
        print(imgid,item.img)
        base64_data=urltoBase64('./'+str(item.img))
        result=facedetect(base64_data,at)
        if result['error_code']==0:
            if result['result']['face_num'] ==1:
                ft = result['result']['face_list'][0]['face_token']
                result=faceSearch(base64_data,at,user)
                if result['error_code']==222207:
                    userlistsize = len(getuserlist(at, user))
                    user_id = str(userlistsize)
                    if Group_person.objects.filter(group_id=User.objects.filter(u_id=eval(user)).first(),person_id=user_id).first() == None:
                        # 创建一个新person
                        person = Group_person(group_id=User.objects.filter(u_id=eval(user)).first(),
                                              person_id=user_id)
                        person.save()
                    r = addface(at, user, user_id, ft)
                    if r['error_code']==0:
                        if Face.objects.filter(face_token=ft).first() == None:
                            face = Face(face_token=ft, img_id=Img.objects.filter(img_id=imgid).first())
                            face.save()
                        person_face = Person_face(group_id=User.objects.filter(u_id=eval(user)).first() ,person_id=user_id,
                                                  face_id=Face.objects.filter(face_token=ft).first())
                        person_face.save()

                elif result['error_code']==0:
                    group_id = result['result']['user_list'][0]['group_id']
                    user_id = result['result']['user_list'][0]['user_id']
                    ft = result['result']['face_token']
                    if result['result']['user_list'][0]['score']>=80:
                        r=addface(at,group_id,user_id,ft)
                    else:
                        userlistsize=len(getuserlist(at,user))
                        user_id=str(userlistsize)
                        if Group_person.objects.filter(group_id=User.objects.filter(u_id=eval(group_id)).first(),person_id=user_id).first() == None:
                            # 创建一个新person
                            person = Group_person(group_id=User.objects.filter(u_id=eval(group_id)).first(),
                                                  person_id=user_id)
                            person.save()
                        r=addface(at, group_id, user_id, ft)
                        flag=0
                    if r['error_code']==0:
                        if Face.objects.filter(face_token=ft).first() == None:
                            face = Face(face_token=ft, img_id=Img.objects.filter(img_id=imgid).first())
                            face.save()
                        person_face = Person_face(group_id=User.objects.filter(u_id=eval(group_id)).first() ,person_id=user_id,
                                                  face_id=Face.objects.filter(face_token=ft).first())
                        person_face.save()
            else:
                result=faceSearch_multi(base64_data,at,user)
                if result['error_code'] == 0:
                    facelist=result['result']['face_list']
                    for face in facelist:
                        ft=face['face_token']
                        group_id = face['user_list'][0]['group_id']
                        user_id = face['user_list'][0]['user_id']
                        score = face['user_list'][0]['score']
                        if score>=80:
                            r=addface(at,group_id,user_id,ft)
                        else:
                            userlistsize = len(getuserlist(at, user))
                            user_id = str(userlistsize)
                            if Group_person.objects.filter(group_id=User.objects.filter(u_id=eval(group_id)).first(),person_id=user_id).first() == None:
                                # 创建一个新person
                                person = Group_person(group_id=User.objects.filter(u_id=eval(group_id)).first(),
                                                      person_id=user_id)
                                person.save()
                            r = addface(at, group_id, user_id, ft)
                        if r['error_code'] == 0:
                            if Face.objects.filter(face_token=ft).first() == None:
                                face = Face(face_token=ft, img_id=Img.objects.filter(img_id=imgid).first())
                                face.save()
                            person_face = Person_face(group_id=User.objects.filter(u_id=eval(group_id)).first(),
                                                      person_id=user_id,
                                                      face_id=Face.objects.filter(face_token=ft).first())
                            person_face.save()
    return HttpResponse('deal ok')

#baidu——version
# def getfacelist(request):
#     group_id = "01"
#     json = {}  # 最终返回的json
#     jsonlist = []  # 列表
#     at=gettoken()
#     user_id_list=getuserlist(at,group_id)
#     for user_id in user_id_list:
#         time.sleep(0.3)
#         #info=Facelist_info.objects.filter(group_id=User.objects.filter(u_id=group_id).first().u_id,user_id=user_id).first().user_info
#         info=""
#         tempt_json_obj={"user_id":user_id,"info":info}
#         facelist=getuserface(at,group_id,user_id)
#         imglist=[]
#         for face in facelist:
#             img_id=Face.objects.filter(face_token=face['face_token']).first().img_id.img_id
#             img=Img.objects.filter(img_id=img_id).first()
#             imgobj = {"id": img.img_id,"img": str(img.img), "time": str(img.time),"describe": img.describe}  # 每条记录转换成json对象
#             imglist.append(imgobj)  # json对象添加到列表
#         tempt_json_obj["imglist"]=imglist
#         jsonlist.append(tempt_json_obj)
#     jsonlist.sort(key=lambda x: len(x["imglist"]),reverse=True) #人脸数量多的用户排在前面
#     json["users"]=jsonlist
#     return JsonResponse(json,content_type="application/json; charset=UTF-8")

def getfacelist(request):
    group_id = "1"
    json = {}  # 最终返回的json
    jsonlist = []  # 列表
    person_list = Group_person.objects.filter(group_id=User.objects.filter(u_id=group_id).first()).all()
    for person in person_list:
        #time.sleep(0.3)
        info = person.person_info
        person_id = person.person_id
        tempt_json_obj={"person_id":person_id,"info":info}
        facelist = Person_face.objects.filter(group_id=User.objects.filter(u_id=group_id).first(),person_id=person_id).all()
        imglist=[]
        for face in facelist:
            face_id=face.face_id.face_id
            img_id=Face.objects.filter(face_id=face_id).first().img_id.img_id
            img=Img.objects.filter(img_id=img_id).first()
            imgobj = {"id": img.img_id,"img": str(img.img), "time": str(img.time),"describe": img.describe}  # 每条记录转换成json对象
            imglist.append(imgobj)  # json对象添加到列表
        tempt_json_obj["imglist"]=imglist
        jsonlist.append(tempt_json_obj)
    jsonlist.sort(key=lambda x: len(x["imglist"]),reverse=True) #人脸数量多的用户排在前面
    json["persons"]=jsonlist
    return JsonResponse(json,content_type="application/json; charset=UTF-8")

def update_info(request):
    group_id="1"
    r_json={}
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    person = data['person']
    new_info = data['info']
    imglist = person['imglist']
    person_id = person['person_id']
    update_person = Group_person.objects.get(group_id=eval(group_id),person_id=person_id)
    old_info = update_person.person_info
    update_person.person_info=new_info
    update_person.save()
    for imgobj in imglist:
        img=Img.objects.get(img_id=imgobj['id'])
        describe=img.describe
        if describe==None:
            l=[]
        else:
            l=describe.split(',')
        print(l)
        if old_info in l: #删除旧标签
            l.remove(old_info)
        l.append(new_info) #添加新标签
        new_describe=','.join(l)
        print(new_describe)
        img.describe=new_describe
        img.save()

    return JsonResponse(r_json,content_type="application/json; charset=UTF-8")

#测试
def test(request):
    print(Face.objects.filter(face_token='c343027a089b3d1ca38a15c52cfda2ef').first()==None)
    return HttpResponse('test ok')