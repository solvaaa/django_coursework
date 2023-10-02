from django.db import models

from mailing.models import NULLABLE


# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='контент')
    image = models.ImageField(verbose_name='изображение', **NULLABLE)
    views = models.IntegerField(default=0, verbose_name='просмотры')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
