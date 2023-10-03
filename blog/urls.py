from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostDetailView

appname = BlogConfig.name


urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path('<int:pk>', cache_page(60)(BlogPostDetailView.as_view()), name='blog_detail'),
]
