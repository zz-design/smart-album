from django.db import models

# Create your models here.
class Img(models.Model):
    id=models.IntegerField('id',primary_key=True)
    img=models.ImageField('图片',upload_to='static/img')
    time=models.CharField('时间',max_length=20)

    class Meta:
        db_table='img'


class User(models.Model):
    id=models.IntegerField('账号',primary_key=True)
    password=models.CharField('密码',max_length=20)

    class Meta:
        db_table='user'

class User_img(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id')
    img_id=models.ForeignKey(Img,on_delete=models.CASCADE,db_column='img_id')

    class Meta:
        db_table='user_img'






