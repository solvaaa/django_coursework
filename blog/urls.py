from django.urls import path

from blog.apps import BlogConfig

appname = BlogConfig.name


urlpatterns = [
    #path('', BlogListView.as_view(), name='blog_list'),
]