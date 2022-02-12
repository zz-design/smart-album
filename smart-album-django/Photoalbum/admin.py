from django.contrib import admin
from .models import Img,User,User_img,Share,ShareAlbum,Friends,User_SA,User_Share,S_picture,SA_upload,SAU_picture,Face,Facelist_info

@admin.register(Img)
class  ImgAdmin(admin.ModelAdmin):
    list_display = ('img_id','img','time','describe')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('u_id','username')

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
    list_display = ('sa_id','sa_name','text','time')

@admin.register(User_SA)
class User_SAAdmin(admin.ModelAdmin):
    list_display = ('u_id','sa_id')

@admin.register(SA_upload)
class SA_uploadAdmin(admin.ModelAdmin):
    list_display = ('sau_id', 'u_id','sa_id','time')

@admin.register(SAU_picture)
class SAU_pictureAdmin(admin.ModelAdmin):
    list_display = ('sau_id', 'img_id')

@admin.register(Face)
class FaceAdmin(admin.ModelAdmin):
    list_display = ('face_id','face_token','img_id')

@admin.register(Facelist_info)
class Facelist_infoAdmin(admin.ModelAdmin):
    list_display = ('group_id','user_id','user_info')
# Register your models here.
