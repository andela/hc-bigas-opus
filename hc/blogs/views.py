from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hc.front.views import _welcome_check
from .forms import BlogPostsCategoryForm, BlogPostsForm, CommentForm
from .models import BlogPosts, BlogPostsCategory, Comment

def create_categories_and_blogs(request):
    """ New blogposts and categories are created in this functionb"""
    form = BlogPostsCategoryForm(request.POST or None, prefix="create_category")
    form_blog = BlogPostsForm(request.POST or None, prefix="create_blog")
    categories = BlogPostsCategory.objects.all()
    blogs = BlogPosts.objects.all()
    cxt = {
        'form':form,
        'categories':categories,
        'form_blog':form_blog,
        'blogs':blogs
    }
    if request.method == 'POST':
        if "create_category" in request.POST:
            if form.is_valid():
                category = form.save(commit=False)
                category.title = form.cleaned_data['title']
                category.save()
                return render(request, 'blog/create_categories_and_blogs.html', cxt)
            return HttpResponseRedirect('/blog/', cxt)
        elif "create_blog" in request.POST:
            form_blog = BlogPostsForm(request.POST, prefix='create_blog')
            title = request.POST['title']
            category_input = request.POST['selectop']
            content = request.POST['content']
            author = request.user
            if title and category_input and content:
                category_query = BlogPostsCategory.objects.get(id=category_input)
                blog=BlogPosts(author=author, title=title, content=content, category=category_query)
                blog.save()  
                return HttpResponseRedirect('/blog/', cxt)
            return render(request, 'blog/create_categories_and_blogs.html', cxt)
        return HttpResponseRedirect('/blog/', cxt)
    else:
        return render(request, "blog/blogview.html", cxt)
