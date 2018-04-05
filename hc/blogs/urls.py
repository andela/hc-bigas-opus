from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^$', views.create_categories_and_blogs, name="hc-category"),
     url(r'^create/$', views.create_blogs, name="hc-categories"),
     url(r'^view/comment/(?P<post>[\w\-]+)/$', views.add_comment, name='hc-add-comment'),
     url(r'^view/(?P<pk>[\w\-]+)/$', views.view_blog_detail, name='hc-view-blog'),
     url(r'^views/(?P<category>[\w\-]+)/$', views.blog_by_category, name='hc-category-blogs'),
     url(r'^edit/(?P<pk>[\w\-]+)/$', views.edit_blog, name='hc-edit-blog'),
     url(r'^delete/(?P<pk>[\w\-]+)/$', views.delete_blog, name='hc-delete-blog')
 ]