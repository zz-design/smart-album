from django.contrib import admin
from .models import Img,User,User_img

@admin.register(Img)
class  ImgAdmin(admin.ModelAdmin):
    list_display = ('id','img','time')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','password')

@admin.register(User_img)
class User_imgAdmin(admin.ModelAdmin):
    list_display = ('user_id','img_id')


# Register your models here.
