from django.db import models
from django.urls import reverse
from datetime import date, datetime
from django.contrib.auth.models import User 
# Create your models here.


class Subforum(models.Model): 
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    pinned = models.BooleanField(default=False)

    def __str__(self): 
        return f'title of this subforum: {self.title}'
    
    def get_absolute_url(self): 
        return reverse('subforums_detail', kwargs={'subforum_id': self.id})  #refactor with the correct views reference and variable names 
    
class Post(models.Model): 
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=600)
    date = models.DateField(auto_now_add=True)
    subforum = models.ForeignKey(
        Subforum, 
        on_delete=models.CASCADE
    )
  
    def __str__(self):
        return f'title of this post is {self.title}'

    class Meta: 
        ordering = ['-date']


class Company(models.Model): 
    name =  models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    url = models.CharField(max_length=150)
    industry = models.CharField(max_length=100)
    photo_url = models.CharField(max_length=150)

    def __str__(self): 
        return f'{self.name}'
    
    def get_absolute_url(self): 
        return reverse('company_detail', kwargs={'pk': self.id})  #refactor with the correct views reference and variable names 