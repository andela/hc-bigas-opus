# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-11 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_auto_20180410_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogposts',
            old_name='slug',
            new_name='_slug',
        ),
    ]
