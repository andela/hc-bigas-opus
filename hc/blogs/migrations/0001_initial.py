# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-09 16:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('draft', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog posts',
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='BlogPostsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blogs.BlogPosts')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='blogposts',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.BlogPostsCategory'),
        ),
    ]