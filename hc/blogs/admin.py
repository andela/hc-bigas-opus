from django.contrib import admin

'''
This is the file where blog posts and blog posts category models are registered.
'''
from .models import BlogPosts, BlogPostsCategory

admin.site.register(BlogPosts)
admin.site.register(BlogPostsCategory)