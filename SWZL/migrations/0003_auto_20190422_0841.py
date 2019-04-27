# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-04-22 08:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SWZL', '0002_auto_20190418_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruit',
            name='announcer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recruitment',
            name='announcer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='memo',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='备注:'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='手机:'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=32, verbose_name='名字:'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.EmailField(max_length=255, unique=True, verbose_name='用户名:'),
        ),
    ]