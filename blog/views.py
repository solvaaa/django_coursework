from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import BlogPost


# Create your views here.

class BlogPostListView(ListView):
    model = BlogPost


class BlogPostDetailView(DetailView):
    model = BlogPost