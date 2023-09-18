import uuid
import boto3
import os
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Subforum, Post, Company
from .forms import PostForm

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
    return render(request, 'subforum/detail.html', {
        'subforum': subforum, 
        'post_form': post_form
        })

class SubforumCreate(CreateView): 
    model = Subforum
    fields = ['title', 'pinned']

def add_post(request, subforum_id): 
    form = PostForm(request.POST)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.subforum_id = subforum_id
        new_post.save()
    return redirect('subforums_detail', subforum_id = subforum_id)

class CompanyList(ListView): 
    model = Company 
    template_name = "company/index.html"

class CompanyDetail(DetailView): 
    model = Company 
    template_name = "company/detail.html"

class CompanyCreate(CreateView): 
    model = Company 
    fields = '__all__'
    template_name = "company/form.html"