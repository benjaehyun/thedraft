from django.db import models
from django.urls import reverse
from datetime import date, datetime
from django.contrib.auth.models import User 
# Create your models here.

class Post(models.Model): 
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=600)
    date = models.DateField(auto_now_add=True)
  
    def __str__(self):
        return f'Photo for post_id: {self.post_id} @{self.url}'


class Photo(models.Model): 
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for post_id: {self.post_id} @{self.url}'

class Subforum(models.Model): 
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)