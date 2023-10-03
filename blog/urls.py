from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostDetailView

appname = BlogConfig.name


urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path('<int:pk>', BlogPostDetailView.as_view(), name='blog_detail'),
]