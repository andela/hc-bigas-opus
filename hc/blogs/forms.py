from django import forms
from .models import BlogPostsCategory, BlogPosts, Comments

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogPostsCategory
        fields = ('title')

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPosts
        fields = ('category', 'title','content')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body')
