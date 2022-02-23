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
    #imgs = models.CharField('图片', max_length=100,null=True, blank=True)
    public = models.IntegerField('是否公开',default=0)#0表示不公开，1表示公开

    class Meta:
        db_table='share'

class S_picture(models.Model):
    s_id = models.ForeignKey(Share,on_delete=models.CASCADE,db_column='s_id')
    img_id = models.ForeignKey(Img,on_delete=models.CASCADE,db_column='img_id')

    class Meta:
        db_table='s_picture'

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
    #imgs = models.CharField('图片', max_length=100,null=True, blank=True)

    class Meta:
        db_table='shareAlbum'

class User_SA(models.Model):
    u_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='u_id')
    sa_id=models.ForeignKey(ShareAlbum,on_delete=models.CASCADE,db_column='sa_id')

    class Meta:
        db_table='user_sa'
        unique_together = ("u_id", "sa_id")

class SA_upload(models.Model):
    sau_id = models.AutoField('id', primary_key=True)
    u_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='u_id')
    sa_id=models.ForeignKey(ShareAlbum,on_delete=models.CASCADE,db_column='sa_id')
    time = models.DateField('时间', max_length=20)

    class Meta:
        db_table='sa_upload'

class SAU_picture(models.Model):
    sau_id = models.ForeignKey(SA_upload, on_delete=models.CASCADE, db_column='sau_id')
    img_id = models.ForeignKey(Img, on_delete=models.CASCADE, db_column='img_id')

    class Meta:
        db_table = 'sau_picture'

class Face(models.Model):
    face_id = models.AutoField('face_id', primary_key=True)
    face_token = models.CharField('face_token',unique=True,max_length=50)
    img_id = models.ForeignKey(Img,on_delete=models.CASCADE,db_column='img_id')

    class Meta:
        db_table = 'face'

class Group_person(models.Model):
    group_id = models.ForeignKey(User,on_delete=models.CASCADE,db_column='u_id')
    person_id = models.CharField('person_id',max_length=50)
    person_info = models.CharField('person_info', max_length=50,null=True, blank=True)

    class Meta:
        db_table = 'group_person'
        unique_together = ("group_id", "person_id")

class Person_face(models.Model):
    group_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='u_id', null=True, blank=True)
    person_id = models.CharField('person_id',max_length=50)
    face_id = models.ForeignKey(Face,on_delete=models.CASCADE,db_column='face_id')

    class Meta:
        db_table = 'person_face'
        unique_together = ("group_id", "person_id", "face_id")


