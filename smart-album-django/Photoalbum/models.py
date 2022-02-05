from django.db import models

# Create your models here.
class Img(models.Model):
    img_id=models.AutoField('id',primary_key=True)
    img=models.ImageField('图片',upload_to='static/img')
    time=models.DateField('时间',max_length=20)
    describe = models.CharField('描述',max_length=100,null=True, blank=True)

    class Meta:
        db_table='img'


class User(models.Model):
    u_id=models.AutoField('id',primary_key=True)
    username=models.CharField('用户名',max_length=20)

    class Meta:
        db_table='user'

class User_img(models.Model):
    u_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='u_id')
    img_id=models.ForeignKey(Img,on_delete=models.CASCADE,db_column='img_id')

    class Meta:
        db_table='user_img'
        unique_together = ("u_id", "img_id")

class Friends(models.Model):
    u_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_id')
    f_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='f_id')

    class Meta:
        db_table='friends'
        unique_together = ("u_id", "f_id")

class Share(models.Model):
    s_id = models.AutoField('id', primary_key=True)
    text = models.CharField('文案',max_length=100,null=True, blank=True)
    time = models.DateTimeField('时间', max_length=50)
    imgs = models.CharField('图片', max_length=100,null=True, blank=True)
    public = models.IntegerField('是否公开',default=0)#0表示不公开，1表示公开

    class Meta:
        db_table='share'

class User_Share(models.Model):
    u_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='u_id')
    s_id=models.ForeignKey(Share,on_delete=models.CASCADE,db_column='s_id')

    class Meta:
        db_table='user_share'
        unique_together = ("u_id", "s_id")

class ShareAlbum(models.Model):
    sa_id = models.AutoField('id', primary_key=True)
    sa_name = models.CharField('相册名', max_length=20,null=True, blank=True)
    text = models.CharField('文案',max_length=100,null=True, blank=True)
    time = models.DateField('时间', max_length=20)
    imgs = models.CharField('图片', max_length=100,null=True, blank=True)

    class Meta:
        db_table='shareAlbum'

class User_SA(models.Model):
    u_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='u_id')
    sa_id=models.ForeignKey(ShareAlbum,on_delete=models.CASCADE,db_column='sa_id')

    class Meta:
        db_table='user_sa'
        unique_together = ("u_id", "sa_id")




