# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-03 21:12
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('kind', models.CharField(choices=[('email', 'Email'), ('webhook', 'Webhook'), ('hipchat', 'HipChat'), ('slack', 'Slack'), ('pd', 'PagerDuty'), ('po', 'Pushover'), ('victorops', 'VictorOps'), ('sms', 'SMS'), ('telegram', 'Telegram')], max_length=20)),
                ('value', models.TextField(blank=True)),
                ('email_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('tags', models.CharField(blank=True, max_length=500)),
                ('code', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('timeout', models.DurationField(default=datetime.timedelta(1))),
                ('grace', models.DurationField(default=datetime.timedelta(0, 3600))),
                ('nag', models.DurationField(default=datetime.timedelta(0, 60))),
                ('n_pings', models.IntegerField(default=0)),
                ('last_ping', models.DateTimeField(blank=True, null=True)),
                ('alert_after', models.DateTimeField(blank=True, editable=False, null=True)),
                ('nag_after', models.DateTimeField(blank=True, editable=False, null=True)),
                ('status', models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('new', 'New'), ('paused', 'Paused'), ('often', 'Often'), ('nag', 'Nag')], default='new', max_length=6)),
                ('often', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_status', models.CharField(max_length=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('error', models.CharField(blank=True, max_length=200)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Channel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Check')),
            ],
            options={
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='Ping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('scheme', models.CharField(default='http', max_length=10)),
                ('remote_addr', models.GenericIPAddressField(blank=True, null=True)),
                ('method', models.CharField(blank=True, max_length=10)),
                ('ua', models.CharField(blank=True, max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Check')),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='checks',
            field=models.ManyToManyField(to='api.Check'),
        ),
        migrations.AddField(
            model_name='channel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterIndexTogether(
            name='check',
            index_together=set([('status', 'user', 'alert_after')]),
        ),
    ]
