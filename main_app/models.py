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
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    def __str__(self): 
        return f'title of this subforum: {self.title}'
    
    def get_absolute_url(self): 
        return reverse('subforums_detail', kwargs={'subforum_id': self.id})  #refactor with the correct views reference and variable names 
    
class Post(models.Model): 
    content = models.TextField(max_length=600)
    date = models.DateField(auto_now_add=True)
    subforum = models.ForeignKey(
        Subforum, 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
  
    def __str__(self):
        return f'title of this post is {self.title}'

    class Meta: 
        ordering = ['-date']

class Photo(models.Model): 
    url = models.CharField(max_length=200)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE
        )

    def __str__(self):
        return f'Photo for post_id: {self.post_id} @{self.url}'



class Comment(models.Model): 
    content = models.TextField(max_length=250)
    date = models.DateField(auto_now_add=True)
    Post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, 
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
    

class Company_Subforum(models.Model): 
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    pinned = models.BooleanField(default = False)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    def __str__(self): 
        return f'title of this subforum: {self.title}'
    
    def get_absolute_url(self): 
        return reverse('company_subforum_detail', kwargs={'pk': self.id})  #refactor with the correct views reference and variable names 
    
class Company_Post(models.Model): 
    content = models.TextField(max_length=600)
    date = models.DateField(auto_now_add=True)
    subforum = models.ForeignKey(
        Company_Subforum, 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
  
    def __str__(self):
        return f'title of this post is {self.title}'

    class Meta: 
        ordering = ['-date']

class Company_Photo(models.Model): 
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Company_Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for post_id: {self.post_id} @{self.url}'
    