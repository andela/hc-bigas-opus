
from django.test import TestCase

# Create your tests here.

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
        self.client.login(username="alice@example.org", password="password")
        self.category = BlogPostsCategory(title='Machine Learning')
        self.category.save()
        self.blog = BlogPosts(title='Basics', content='It is the very beginning', 
                        category=self.category)
        self.blog.save()

    
    def test_create_blog(self):
        url = reverse('blogs:hc-category')
        blog = BlogPosts.objects.filter(title='Basics').first()
        self.assertEqual('Basics', blog.title)


    def test_create_category(self):
        url = reverse('blogs:hc-category')
        data = {'create_category-title': ['read'], 'create_category': ['']}
        response = self.client.post(url, data)
        category = BlogPostsCategory.objects.filter(title='read').first()
        self.assertEqual('read', category.title)


    def test_home_page_returns_all_categories(self):
        url = reverse('blogs:hc-category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/view_blogs.html')

    # def test_view_blogs__by_category(self):
    #     category = BlogPostsCategory.objects.get(title='Machine Learning')
    #     url = 'http://localhost:8000/blog/views/1/'
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'blog/view_blogs.html')


    def test_delete_blog(self):
        blog = BlogPosts.objects.filter(title='Basics').first()
        url = reverse('blogs:hc-delete-blog', kwargs={'pk':blog.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 302)


    def test_create_blog_form_invalid(self):
        url = reverse('blogs:hc-category')
        data = {'selectop': ['1'], 'title':[''], 'content': ['read'], 'create_blog': ['']}
        response = self.client.post(url, data)
        self.assertTemplateUsed(response, 'blog/create_categories_and_blogs.html')

    def test_create_category_form_invalid(self):
        url = reverse('blogs:hc-category')
        data = {'create_category-title': [''], 'create_category': ['']}
        response = self.client.post(url, data)
        self.assertRedirects(response, '/blogs/')
        self.assertEqual(response.status_code, 302)

   
    def test_if_get_redirect(self):
        url = reverse('blogs:hc-category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/view_blogs.html')

    def test_no_blogs_to_display(self):
        category = BlogPostsCategory(title='Reads')
        category.save()
        category1 = BlogPostsCategory.objects.get(title='Reads')
        url = reverse('blogs:hc-category-blogs', kwargs={'category':category1.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/view_blogs.html')
    
    def test_view_blog_detail(self):
        blog = BlogPosts.objects.filter(title='Basics').first()
        url = reverse('blogs:hc-view-blog', kwargs={'pk':blog.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/view_posts.html')