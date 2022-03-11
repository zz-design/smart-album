"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Photoalbum import views

urlpatterns = [
    path('admin/', admin.site.urls),#admin账号zzh 密码aa23fve6（需要自创建）
    path('getAllimg/', views.getAllimg),
    #path('addimg/', views.addimg),
    path('uploadimg/', views.uploadimg),
    path('getfacelist/', views.getfacelist),
    path('face_process/', views.face_process),
    path('update_info/', views.update_info),
    path('search_img/', views.search_img),
    path('getUser_id/', views.getUser_id),
    path('getGeneral/', views.getGeneral),
    path('create_ShareAlbum/', views.create_ShareAlbum),
    path('get_UserShareAlbum/', views.get_UserShareAlbum),
    path('get_AlbumInfo/', views.get_AlbumInfo),
    path('upload_ShareAlbum/', views.upload_ShareAlbum),
    path('upload_SA_img/', views.upload_SA_img),


    path('test/', views.test),


]
