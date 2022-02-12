# Generated by Django 3.2.5 on 2022-02-08 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Photoalbum', '0002_auto_20220206_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Face',
            fields=[
                ('face_id', models.AutoField(primary_key=True, serialize=False, verbose_name='face_id')),
                ('face_token', models.CharField(max_length=50, unique=True, verbose_name='face_token')),
                ('img_id', models.ForeignKey(db_column='img_id', on_delete=django.db.models.deletion.CASCADE, to='Photoalbum.img')),
            ],
            options={
                'db_table': 'face',
            },
        ),
    ]