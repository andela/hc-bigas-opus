from django.db import models

# Create your models here.
"""
Database models and schemas are contained in this file.
We will import and use slugify to create cool looking human friendly urls
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from datetime import datetime


# This is the Blog Post Category model
class BlogPostsCategory(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique = True)

    def save (self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(BlogPostsCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# This is the Blog Posts model
class BlogPosts(models.Model):
    author = models.ForeignKey(User, blank=True, null=True)
    title = models.CharField(max_length=300, blank = False)
    content = models.TextField(blank = False)
    slug = models.SlugField(unique = True)
    category = models.ForeignKey(BlogPostsCategory, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    draft = models.BooleanField(default = False)
    updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ['created_on']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog posts"

    def save (self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(BlogPosts, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# This is the Comment model
class Comment(models.Model):
    post = models.ForeignKey(BlogPosts, related_name='comments')
    name = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
