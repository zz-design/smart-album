from django.contrib import admin
from .models import Img,User,User_img,Share,ShareAlbum,Friends,User_SA,User_Share,S_picture,SA_upload,SAU_picture,Face,Person_face,Group_person,Class,Class_Img

@admin.register(Img)
class  ImgAdmin(admin.ModelAdmin):
    list_display = ('img_id','img','time','describe')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('u_id','openid','username','avatarUrl')

@admin.register(User_img)
class User_imgAdmin(admin.ModelAdmin):
    list_display = ('u_id','img_id')

@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ('u_id','f_id')

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('s_id','text','time','public')

@admin.register(S_picture)
class S_pictureAdmin(admin.ModelAdmin):
    list_display = ('s_id','img_id')

@admin.register(User_Share)
class User_ShareAdmin(admin.ModelAdmin):
    list_display = ('u_id','s_id')

@admin.register(ShareAlbum)
class ShareAlbumAdmin(admin.ModelAdmin):
    list_display = ('sa_id','sa_name','time')

@admin.register(User_SA)
class User_SAAdmin(admin.ModelAdmin):
    list_display = ('u_id','sa_id')

@admin.register(SA_upload)
class SA_uploadAdmin(admin.ModelAdmin):
    list_display = ('sau_id', 'u_id','sa_id','time','text')

@admin.register(SAU_picture)
class SAU_pictureAdmin(admin.ModelAdmin):
    list_display = ('sau_id', 'img_id')

@admin.register(Face)
class FaceAdmin(admin.ModelAdmin):
    list_display = ('face_id','face_token','img_id')

@admin.register(Group_person)
class Group_personAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'person_id', 'person_info')

@admin.register(Person_face)
class Person_faceAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'person_id', 'face_id')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('c_id', 'classname')

@admin.register(Class_Img)
class Class_ImgAdmin(admin.ModelAdmin):
    list_display = ('c_id', 'img_id')





# Register your models here.
