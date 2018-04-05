"""
Database models and schemas are contained in this file.
We will import and use slugify to create cool looking urls
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from datetime import datetime


# BlogPostCategory model
class BlogPostsCategory(models.Model):
    title = models.CharField(max_length=300, unique = True)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.title

# BlogPosts model
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

    def __str__(self):
        return self.title

    from .utils import unique_slug_generator
    '''
    Right before the model is saved we perform this check
    '''
    def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

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





pre_save.connect(pre_save_post_receiver, sender=BlogPosts)
pre_save.connect(pre_save_post_receiver, sender=BlogPostsCategory)
