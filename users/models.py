from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    is_verified = models.BooleanField(verbose_name='подтверждён', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []