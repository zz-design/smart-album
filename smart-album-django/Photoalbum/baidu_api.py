import requests
from Photoalbum.tools import urltoBase64
#百度api

def gettoken():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    id = 'VfSs9gnVtF9CaPCHHEKgvX2Z'
    secret = 'TIaSwlyW4YjkGVZxoMvsm6OOvCXlO0qR'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + id + '&client_secret=' + secret
    response = requests.get(host)
    if response:
        print(response.json().get("access_token"))
        return response.json().get("access_token")

def facedetect(base64_img,at):
    params={}
    params["image"]=base64_img
    params["image_type"]="BASE64"
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    access_token = at
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}

    proxies = {"http": None, "https": None}
    response = requests.post(request_url, data=params, headers=headers,proxies=proxies)
    if response:
        print(response.json())
        return response.json()

def faceSearch(base64_img,at,username):
    params={
        "image": base64_img,
        "image_type": "BASE64",
        "group_id_list": username,
    }
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    access_token = at
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        return response.json()

def faceSearch_multi(base64_img,at,username):
    params = {
        "image": base64_img,
        "image_type": "BASE64",
        "group_id_list": username,
        "max_face_num": 7,
        "match_threshold":20,
    }
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/multi-search"
    access_token = at
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        return response.json()

def getgrouplist(at):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getlist"

    params = {}
    access_token = at
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())

def getuserlist(at,group_id):
    '''
    获取用户列表
    '''
    params = {
        "group_id": group_id,
    }
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers"

    access_token = at
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json()['result']['user_id_list'])
        if response.json()['error_code'] == 0:
             return response.json()['result']['user_id_list']

def getuserface(at,group_id,user_id):
    '''
    获取用户人脸列表
    '''
    params = {
        "user_id" : user_id,
        "group_id": group_id,
    }
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/getlist"
    access_token = at
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        if  response.json()['error_code']==0:
            return response.json()['result']['face_list']


def addface(at,group_id,user_id,face):
    '''
    人脸注册
    '''
    params = {
        "image": face,
        "image_type":"FACE_TOKEN",
        "group_id":str(group_id),
        "user_id":str(user_id),
        "user_info":"test",

    }
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"

    access_token = at
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        return response.json()

if __name__ == '__main__':
    at=gettoken()
    getuserface(at,'01','1')

