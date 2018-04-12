''''
This file contains all the crud methods of the blog app like creating blog posts, blog posts categoty and the comments.
'''
from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hc.front.views import _welcome_check
from .forms import BlogPostsCategoryForm, BlogPostsForm, CommentForm
from .models import BlogPosts, BlogPostsCategory, Comment

def create_categories_and_blogs(request):
    """ New blogposts and categories are created in this function"""
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
                try:
                    category.save()
                except IntegrityError:
                    messages.warning(request, 'The category already exists.Create a blog post under that category!')
            return HttpResponseRedirect('/blogs/', cxt)
        elif "create_blog" in request.POST:
            form_blog = BlogPostsForm(request.POST, prefix='create_blog')
            title = request.POST['title']
            category_input = request.POST['selectop']
            content = request.POST['content']
            author = request.user
            if title and category_input and content:
                category_query = get_object_or_404(BlogPostsCategory, title=category_input)
                blog=BlogPosts(author=author, title=title, content=content, category=category_query)
                blog.save()  
                return HttpResponseRedirect('/blogs/', cxt)
        return render(request, 'blog/create_categories_and_blogs.html', cxt)
        # return HttpResponseRedirect('/blogs/', cxt)
    else:
        return render(request, "blog/view_blogs.html", cxt)

@login_required
def create_blogs(request):
    """A function to render the template for creating blog posts"""
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
    return render(request, 'blog/create_categories_and_blogs.html', cxt)

def blog_by_category(request, category):
    """This function displays blogs under a specific category"""
    category = BlogPostsCategory.objects.get(id=category)
    blogs = BlogPosts.objects.filter(category=category)
    categories = BlogPostsCategory.objects.all()
    if blogs:
        cxt = {
            "blogs": blogs,
            'categories':categories,
            "category": category.title
        }
        return render(request, "blog/view_blogs.html", cxt)
    message = "No Blog Stories In This Category"
    cxt = {
        'categories':categories,
        'message': message
        }
    return render(request, 'blog/view_blogs.html', cxt)

@login_required
def add_comment(request, post):
    """This function holds the logic for adding comments to blog posts""" 
    form_comment = CommentForm(request.POST or None)
    comments_list = Comment.objects.all()
    paginator = Paginator(comments_list, 3)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)
    cxt = {
        'form_comment':form_comment,
        'comments':comments
    }
    blog = BlogPosts.objects.get(id=post)
    if request.method == "POST":
        if "add_comment" in request.POST: 
            if form_comment.is_valid():
                comment = form_comment.save(commit=False)
                comment.body = form_comment.cleaned_data['body']
                comment.name = request.user
                comment.post = blog
                form_comment.save()
                messages.success(request, "Comment successfully added")
                return redirect('blogs:hc-view-blog', post)
            return render(request, "blog/view_posts.html", cxt)
    return render(request, "blog/view_posts.html", cxt)
    
def view_blog_detail(request, pk):
    """This function displays a single blog and the comments associated with it"""
    form_comment = CommentForm(request.POST or None)
    tweet_url = 'hc-bigas-opus.herokuapp.com/blog/view/{}'.format(pk)
    blog = BlogPosts.objects.filter(pk=pk).first()
    comments_list = Comment.objects.filter(post=blog)
    paginator = Paginator(comments_list, 5)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)
    ctx = {
        'comments':comments,
        'form_comment':form_comment,
        'blog':blog,
        'post':blog.id,
        'pk': blog.id,
        'tweet_url': tweet_url, 
    }
    return render(request, "blog/view_posts.html", ctx)

@login_required
def edit_blog(request, pk):
    """This function enables editing of a single blog post"""
    post = BlogPosts.objects.get(pk=pk)
    form = BlogPostsForm(instance=post)
    cxt = {
            'form': form,
            'pk': post.id
            }
    current_user = request.user
    logged_in_user = User.objects.get(pk=current_user.id)
    author=User.objects.get(username=post.author)
    if request.method == 'POST':
        if 'editblog' in request.POST:
            blog = BlogPosts.objects.filter(pk=pk).first()
            form = BlogPostsForm(request.POST)  
            if form.is_valid():
                blog.category = form.cleaned_data['category']
                blog.title = form.cleaned_data['title']
                blog.content = form.cleaned_data['content']
                blog.save()
                messages.success(request, "Blog successfully edited")
                return redirect('blogs:hc-view-blog', blog.id)
            return redirect('blogs:hc-edit-blog', post.id)
        else:
            form = BlogPostsForm(instance=post)
            cxt = {
                    'form': form,
                    'pk': pk
                    }
            return render(request, "blog/create_blog.html", cxt)
    return render(request, "blog/create_blog.html", cxt)

@login_required
def delete_blog(request, pk):
    """This function allows for deleting a single blog post"""
    post = get_object_or_404(BlogPosts, pk=pk)
    post.delete()
    return redirect('blogs:hc-category')
