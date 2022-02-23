# Generated by Django 3.2.5 on 2022-02-14 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Photoalbum', '0004_auto_20220212_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_face',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50, verbose_name='user_id')),
                ('face_id', models.ForeignKey(db_column='face_id', on_delete=django.db.models.deletion.CASCADE, to='Photoalbum.face')),
            ],
            options={
                'db_table': 'user_face',
                'unique_together': {('user_id', 'face_id')},
            },
        ),
        migrations.CreateModel(
            name='Group_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50, verbose_name='user_id')),
                ('group_id', models.ForeignKey(db_column='u_id', on_delete=django.db.models.deletion.CASCADE, to='Photoalbum.user')),
            ],
            options={
                'db_table': 'group_user',
                'unique_together': {('group_id', 'user_id')},
            },
        ),
    ]
