# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-28 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_current_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='reports_frequency',
            field=models.CharField(blank=True, default='monthly', max_length=128),
        ),
    ]