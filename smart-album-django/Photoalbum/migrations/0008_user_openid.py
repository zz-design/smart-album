# Generated by Django 3.2.5 on 2022-02-24 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Photoalbum', '0007_auto_20220214_0505'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='openid',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='openid'),
        ),
    ]
