from django.contrib import admin
from .models import Img,User,User_img,Share,ShareAlbum,Friends,User_SA,User_Share

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
    list_display = ('s_id','text','time','imgs','public')

@admin.register(User_Share)
class User_ShareAdmin(admin.ModelAdmin):
    list_display = ('u_id','s_id')

@admin.register(ShareAlbum)
class ShareAlbumAdmin(admin.ModelAdmin):
    list_display = ('sa_id','sa_name','text','time','imgs')

@admin.register(User_SA)
class User_SAAdmin(admin.ModelAdmin):
    list_display = ('u_id','sa_id')

# Register your models here.
