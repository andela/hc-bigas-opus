# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-04 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='member_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='check',
            name='membership_access',
            field=models.BooleanField(default=False),
        ),
    ]
