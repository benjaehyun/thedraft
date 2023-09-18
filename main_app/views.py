import uuid
import boto3
import os
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Subforum, Post, Company
from .forms import PostForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request): 
    subforums = Subforum.objects.all()
    return render(request, 'home.html', {
        'subforums': subforums
    })

def about(request): 
    return render(request, 'about.html')

def subforums_detail(request, subforum_id): 
    subforum = Subforum.objects.get(id=subforum_id)
    post_form = PostForm()
    comment_form = CommentForm()
    return render(request, 'subforum/detail.html', {
        'subforum': subforum, 
        'post_form': post_form, 
        'comment_form': comment_form 
        })

class SubforumCreate(CreateView): 
    model = Subforum
    fields = ['title', 'pinned']

    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def add_post(request, subforum_id): 
    form = PostForm(request.POST)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.subforum_id = subforum_id
        new_post.user_id = request.user.id 
        new_post.save()
    return redirect('subforums_detail', subforum_id = subforum_id)

@login_required
def add_comment(request, subforum_id, post_id): 
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_id = post_id
        new_comment.user_id = request.user.id 
        new_comment.save()
    return redirect('subforums_detail', subforum_id = subforum_id)


class CompanyList(ListView): 
    model = Company 
    template_name = "company/index.html"

class CompanyDetail(DetailView): 
    model = Company 
    template_name = "company/detail.html"
    #query for subforums and pass the functionality of the company_subforum index 

class CompanyCreate(CreateView): 
    model = Company 
    fields = '__all__'
    template_name = "company/form.html"

def signup(request): 
    error_message = ''
    if request.method == 'POST': 
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            login(request, user)
            return redirect('index')
        else: 
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

