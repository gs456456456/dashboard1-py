# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-23 08:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20170823_1637'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configtemp',
            options={'verbose_name': '温度设置'},
        ),
        migrations.AlterModelOptions(
            name='configwater',
            options={'verbose_name': '水压设置'},
        ),
    ]
