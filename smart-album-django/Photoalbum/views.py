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
from Photoalbum.baidu_api import addface,facedetect,gettoken,getuserlist,getgrouplist,faceSearch,faceSearch_multi,getuserface,gettoken1,generalDetect

# Create your views here.
from Photoalbum.models import Img,Face,User,Person_face,Group_person,Class_Img,Class,Share,ShareAlbum,SA_upload,SAU_picture,S_picture,User_SA,User_Share,User_img,Friends

def getAllimg(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    group_id = str(data['user_id']) #登陆用户的id
    r_json={}#最终返回的json
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

    r_json["imgs"]=jsonlist #图片列表
    return JsonResponse(r_json,content_type="application/json; charset=UTF-8")

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
    group_id = str(request.POST.get('user_id'))
    filename=request.FILES['imgs'].name
    print(filename)
    ImageDate = datetime.now().strftime('%Y-%m-%d')
    m = Img(time=ImageDate)
    m.img.save(name=filename, content=File(img))
    m.save()
    img_process(m,group_id)
    return HttpResponse('add ok')

#上传图片后，做一次图片处理(分类)
def img_process(item,group_id):
    user=group_id   #登陆用户的id
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
                    #给分类的图片描述中加上该分组的标签
                    update_person = Group_person.objects.get(group_id=eval(group_id), person_id=user_id)
                    info = update_person.person_info
                    add_describe(imgid,info)
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
                    if score>=70:
                        r=addface(at,group_id,user_id,ft)
                        # 给分类的图片描述中加上该分组的标签
                        update_person = Group_person.objects.get(group_id=eval(group_id), person_id=user_id)
                        info = update_person.person_info
                        add_describe(imgid, info)
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
    else:
        #若不是人脸，进行景物分类
        general_classify(imgid,base64_data)
    return HttpResponse('deal ok')

#景物分类
def general_classify(imgid,base64_data):
    at1 = gettoken1()
    result = generalDetect(base64_data,at1)
    try:
        keyword=result['result'][0]['keyword']
        if Class.objects.filter(classname=keyword).first()==None:
            new_class=Class(classname=keyword)
            new_class.save()
        class_img=Class_Img(c_id=Class.objects.filter(classname=keyword).first(),img_id=Img.objects.filter(img_id=imgid).first())
        class_img.save()
        #把标签添加到describe
        add_describe(imgid, keyword)
    except:
        print("error")

    return HttpResponse('deal ok')


#人脸批量处理，当前不需要用
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

#获取人脸列表
def getfacelist(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    group_id = str(data['user_id'])
    r_json = {}  # 最终返回的json
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
    r_json["persons"]=jsonlist
    return JsonResponse(r_json,content_type="application/json; charset=UTF-8")

def getGeneral(request):
    r_json={}
    jsonlist=[]
    temp_json_obj={}
    time_imglist = []
    time_json_list = []
    all_class=Class.objects.all()
    for c in all_class:
        time_json_list=[]
        #time.sleep(10)
        classname=c.classname
        c_id=c.c_id
        c_imgs=Class_Img.objects.filter(c_id=c)
        imglist=[]#存放每个类别的图片列表
        temp_json_obj={}
        for c_img in c_imgs:
            img_id=c_img.img_id.img_id
            img = Img.objects.filter(img_id=img_id).first()
            imgobj = {"id": img.img_id, "img": str(img.img), "time": img.time,
                      "describe": img.describe}  # 每条记录转换成json对象
            imglist.append(imgobj)  # json对象添加到列表
        imglist.sort(key=lambda x: x["time"], reverse=True)  # 按时间排序
        ###time_sorting
        temptime = imglist[0]["time"]
        index = 0
        time_imglist = []
        for item in imglist:  # 测试仅取少量数据
            if item["time"] != temptime:
                time_json_obj = {"time": str(temptime), "time_imglist": time_imglist}
                time_json_list.append(time_json_obj)
                temptime = item["time"]
                time_imglist = []
            item["index"]=index
            item["time"]=str(item["time"])
            time_imglist.append(item)  # json对象添加到列表
            index += 1
        num=index
        time_json_obj = {"time": str(temptime), "time_imglist": time_imglist}
        time_json_list.append(time_json_obj)

        print(classname)
        print(time_json_list)

        temp_json_obj['class']=classname
        temp_json_obj['num'] = num
        temp_json_obj['imglist']=time_json_list
        jsonlist.append(temp_json_obj)
    jsonlist.sort(key=lambda x: x["num"], reverse=True)  # 人脸数量多的用户排在前面
    r_json['general']=jsonlist
    print(r_json)
    return JsonResponse(r_json, content_type="application/json; charset=UTF-8")


#添加分类标签
def update_info(request):
    r_json={}
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    group_id = str(data['user_id'])
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

def search_img(request):
    r_json={}
    data = json.loads(request.body.decode('utf-8'))
    keyword = data['keyword']
    jsonlist = []  # 列表
    imglist = []
    search_data = Img.objects.filter(describe__contains=keyword).order_by('-time')  # 等价于select * from img  (按时间倒序排序)
    if search_data.exists():#若查询结果不为空
        temptime = search_data[0].time
        index = 0
        for item in search_data:  # 测试仅取少量数据
            if item.time != temptime:
                time_json_obj = {"time": str(temptime), "imglist": imglist}
                jsonlist.append(time_json_obj)
                temptime = item.time
                imglist = []
            jsonobj = {"id": item.img_id, "index": index, "img": str(item.img), "time": item.time,
                       "describe": item.describe}  # 每条记录转换成json对象
            imglist.append(jsonobj)  # json对象添加到列表
            index += 1
        time_json_obj = {"time": str(temptime), "imglist": imglist}
        jsonlist.append(time_json_obj)

        r_json["imgs"] = jsonlist  # 图片列表

    return JsonResponse(r_json,content_type="application/json; charset=UTF-8")

def add_describe(img_id,keyword):
    imgobj=Img.objects.get(img_id=img_id)
    old_describe = imgobj.describe
    if old_describe ==None:
        new_describe = keyword
    else:
        new_describe = old_describe+","+keyword
    imgobj.describe = new_describe
    imgobj.save()

def getUser_id(request):
    r_json = {}
    data = json.loads(request.body.decode('utf-8'))
    openid = data['openid']
    userid=User.objects.get(openid=openid).u_id
    print(userid)
    r_json['userid']=userid
    return JsonResponse(r_json, content_type="application/json; charset=UTF-8")

def create_ShareAlbum(request):
    r_json = {}
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    user_id = str(data['user_id'])
    title = str(data['title'])
    create_Date = datetime.now().strftime('%Y-%m-%d')
    share_album=ShareAlbum(sa_name=title,time=create_Date)
    share_album.save()
    user_sa = User_SA(u_id=User.objects.filter(u_id=eval(user_id)).first(),sa_id=ShareAlbum.objects.filter(sa_id=share_album.sa_id).first())
    user_sa.save()
    r_json['sa_id']=share_album.sa_id
    return JsonResponse(r_json, content_type="application/json; charset=UTF-8")

def get_UserShareAlbum(request):
    r_json = {}
    jsonlist=[]
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    user_id = str(data['user_id'])
    user_sas=User_SA.objects.filter(u_id=User.objects.filter(u_id=eval(user_id)).first()).all()
    for user_sa in user_sas:
        sa_id=user_sa.sa_id
        share_album=ShareAlbum.objects.filter(sa_id=sa_id.sa_id).first()
        temp_json_obj={'sa_id':share_album.sa_id,'sa_name':share_album.sa_name,'time':str(share_album.time)}
        sa_upload=SA_upload.objects.filter(sa_id=share_album).first()
        if sa_upload==None:
            temp_json_obj['titleimg']='static/share_album_titleImg.png'
        else:
            sau_picture=SAU_picture.objects.filter(sau_id=SAU_picture.objects.filter(sau_id=sa_upload.sau_id).first()).first()
            titleimg=Img.objects.filter(img_id=Img.objects.filter(img_id=sau_picture.img_id).first()).first().img
            temp_json_obj['titleimg'] = titleimg
        jsonlist.append(temp_json_obj)
    r_json['share_albums']=jsonlist
    return JsonResponse(r_json, content_type="application/json; charset=UTF-8")

def get_AlbumInfo(request):
    r_json={}
    userlist=[]
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    sa_id = str(data['sa_id'])
    album=ShareAlbum.objects.filter(sa_id=sa_id).first()
    title=album.sa_name
    time=album.time
    user_sas=User_SA.objects.filter(sa_id=album.sa_id).all()
    for user_sa in user_sas:
        u_id=user_sa.u_id
        user=User.objects.get(u_id=u_id.u_id)
        username=user.username
        avatar=user.avatarUrl
        user_j={'u_id':u_id.u_id,'username':username,'avatar':avatar}
        userlist.append(user_j)
    r_json['album_info']={'title':title,'time':str(time),'userlist':userlist}
    return JsonResponse(r_json, content_type="application/json; charset=UTF-8")

def upload_ShareAlbum(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    sa_id = str(data['sa_id'])
    u_id = str(data['user_id'])
    text = str(data['text'])
    Date = datetime.now().strftime('%Y-%m-%d')
    sa_upload=SA_upload(
        u_id=User.objects.filter(u_id=eval(u_id)).first(),
        sa_id=ShareAlbum.objects.filter(sa_id=eval(sa_id)).first(),
        time=Date,
        text=text)
    sa_upload.save()
    r_json={'sau_id':sa_upload.sau_id}
    return JsonResponse(r_json, content_type="application/json; charset=UTF-8")



def upload_SA_img(request):
    img = request.FILES.get('imgs')
    sau_id = str(request.POST.get('sau_id'))
    ImageDate = datetime.now().strftime('%Y-%m-%d')
    filename = request.FILES['imgs'].name
    print(filename)
    m = Img(time=ImageDate)
    m.img.save(name=filename, content=File(img))
    m.save()
    sau_picture=SAU_picture(img_id=m,sau_id=SA_upload.objects.filter(sau_id=eval(sau_id)).first())
    sau_picture.save()
    return HttpResponse('add ok')


#测试
def test(request):
    print(Face.objects.filter(face_token='c343027a089b3d1ca38a15c52cfda2ef').first()==None)
    return HttpResponse('test ok')