
from django.db import models
from django.db.models import Model


class User(models.Model):
    is_admin = models.BooleanField(default='False')
    username = models.TextField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.URLField(max_length=200, unique = 'True')

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField(unique= 'True')
