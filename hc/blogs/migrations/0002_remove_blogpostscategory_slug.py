# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-10 15:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpostscategory',
            name='slug',
        ),
    ]
