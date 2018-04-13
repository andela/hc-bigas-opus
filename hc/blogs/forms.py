from django import forms
from .models import BlogPostsCategory, BlogPosts, Comment

'''
This file contains the Blog app forms  and their options.
'''

class BlogPostsCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogPostsCategory
        fields = ('title',)

class BlogPostsForm(forms.ModelForm):
    class Meta:
        model = BlogPosts
        fields = ('category', 'title','content')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
