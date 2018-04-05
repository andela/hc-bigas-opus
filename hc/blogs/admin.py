"""
Registration of the BlogPosts and BlogPostsCategory models is done in this file.
"""
from django.contrib import admin

# Register your models here.
from .models import BlogPosts, BlogPostsCategory

admin.site.register(BlogPosts)
admin.site.register(BlogPostsCategory)