# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-16 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180416_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='priority',
            field=models.CharField(default='LOW', max_length=4),
        ),
    ]