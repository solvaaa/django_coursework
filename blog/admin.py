from django.contrib import admin

from blog.models import BlogPost


# Register your models here.
@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'pub_date')
    sortable_by = ('pub_date', 'views', )
    search_fields = ('title', 'content')
