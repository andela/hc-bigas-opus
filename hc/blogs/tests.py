from hc.test import BaseTestCase
from django.contrib.auth.models import User
from .models import BlogPosts, BlogPostsCategory, Comment
from django.shortcuts import reverse
from django.utils import timezone


"""
    All our tests will be in this file and first we initialize all the reusable variables in the setup function
"""
class BlogPostsCategories(BaseTestCase):
    def setUp(self):
        # super(BlogPostsCategories, self).setUp()
        self.client.login(username="alice@example.org", password="password")
        self.category = BlogPostsCategory(title='YOYO')
        self.category.save()
        self.blog = BlogPosts(title='Learning', content='You are accountable to yourself', 
                        category=self.category)
        self.blog.save()



    def test_create_category(self):
        url = reverse('blog:hc-category')
        data = {'create_category-title': ['read'], 'create_category': ['']}
        response = self.client.post(url, data)
        category = BlogPostsCategory.objects.filter(title='read').first()
        self.assertEqual('read', category.title)

    def test_create_blog_post(self):
        url = reverse('blog:hc-category')
        data = {'selectop': ['1'], 'title': ['read'], 'content': ['read'], 'create_blog': ['']}
        response = self.client.post(url, data)
        blog = Blog.objects.filter(title='read').first()
        self.assertEqual('read', blog.title)

