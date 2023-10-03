from django.views.generic import ListView, DetailView

from blog.models import BlogPost
from mailing.models import Mailing, Client


# Create your views here.

class BlogPostListView(ListView):
    model = BlogPost


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        object.views += 1
        object.save()
        return object


class IndexView(ListView):
    template_name = 'index.html'
    model = BlogPost

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.order_by('?')[:3]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.all().count()
        context['active_mailings'] = Mailing.objects.filter(status='START').count()
        context['unique_clients'] = Client.objects.distinct().count()
        return context