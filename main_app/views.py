import uuid
import boto3
import os
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Subforum, Post, Company, Company_Subforum
from .forms import PostForm

# Other View Functions
# Home view function is a Subforum index
def home(request): 
    subforums = Subforum.objects.all()
    # Like this, or can redirect to subforum/index.html instead
    return render(request, 'home', { 
        'subforums': subforums
    })

def about(request): 
    return render(request, 'about')

# Subforum CRUD Views
class SubforumCreate(CreateView): 
    model = Subforum
    fields = ['title', 'pinned']

def subforums_detail(request, subforum_id): 
    subforum = Subforum.objects.get(id=subforum_id)
    post_form = PostForm()
    return render(request, 'subforum/detail.html', {
        'subforum': subforum, 
        'post_form': post_form
        })

class SubforumUpdate(UpdateView):
    model = Subforum
    fields = 'title'

# Post CRUD Views
def add_post(request, subforum_id): 
    form = PostForm(request.POST)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.subforum_id = subforum_id
        new_post.save()
    return redirect('subforums_detail', subforum_id=subforum_id)

def update_post(request, post_id, subforum_id):
    post = Post.objects.get(id=post_id)
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
    return redirect('subforums_detail', subforum_id=subforum_id)

class PostDelete(DeleteView):
    model = Post
    success_url = '/subforums/<int:subforum_id/'

# Company_Subforum CRUD Views
class Company_SubforumCreate(CreateView): 
    model = Company_Subforum
    fields = ['title', 'pinned']

# Question on this one
def company_subfoums_index(request):
    company_subforums = Company_Subforum.objects.all()
    # Where should this live? I picked this one because this file already exists
    return render(request, 'company_index', {
        'company_subforums': company_subforums
    })

def company_subforums_detail(request, company_subforum_id): 
    company_subforum = Company_Subforum.objects.get(id=company_subforum_id)
    post_form = PostForm()
    return render(request, 'company_subforums_detail', {
        'company_subforum': company_subforum, 
        'post_form': post_form
        })

class Company_SubforumUpdate(UpdateView):
    model = Company_Subforum
    fields = 'title'

# Company_Post CRUD Views
def add_company_post(request, company_subforum_id): 
    form = PostForm(request.POST)
    if form.is_valid():
        new_company_post = form.save(commit=False)
        new_company_post.company_subforum_id = company_subforum_id
        new_company_post.save()
    return redirect('company_subforums_detail', company_subforum_id=company_subforum_id)

def update_company_post(request, company_post_id, company_subforum_id):
    company_post = Company_Post.objects.get(id=company_post_id)
    form = PostForm(request.POST)
    if form.is_valid():
        company_post = form.save(commit=False)
        company_post.save()
    return redirect('company_subforums_detail', company_subforum_id=company_subforum_id)

class Company_PostDelete(DeleteView):
    model = Post
    success_url = '/subforums/<int:subforum_id/'

# Company CRUD Views
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