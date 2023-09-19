import uuid
import boto3
import os
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Subforum, Post, Company, Company_Subforum
from .forms import PostForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


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
    comment_form = CommentForm()
    return render(request, 'subforum/detail.html', {
        'subforum': subforum, 
        'post_form': post_form, 
        'comment_form': comment_form 
        })

class SubforumUpdate(UpdateView):
    model = Subforum
    fields = 'title'

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
    return redirect('subforum/detail.html', subforum_id=subforum_id)

def update_post(request, post_id, subforum_id):
    post = Post.objects.get(id=post_id)
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
    return redirect('subforum/<int:subforum_id>', subforum_id=subforum_id)

class PostDelete(DeleteView):
    model = Post
    success_url = '/subforum/<int:subforum_id>/'

# Company_Subforum CRUD Views
class Company_SubforumCreate(CreateView): 
    model = Company_Subforum
    fields = ['title', 'pinned']

# Ben handling these
# def company_subfoums_index(request):
#     company_subforums = Company_Subforum.objects.all()
#     # Where should this live? I picked this one because this file already exists
#     return render(request, 'company_index', {
#         'company_subforums': company_subforums
#     }) 

# def company_subforums_detail(request, company_subforum_id): 
#     company_subforum = Company_Subforum.objects.get(id=company_subforum_id)
#     post_form = PostForm()
#     return render(request, 'company_subforums_detail', {
#         'company_subforum': company_subforum, 
#         'post_form': post_form
#         })

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
    return redirect('company_subforum/detail.html', company_subforum_id=company_subforum_id)

def update_company_post(request, company_post_id, company_subforum_id):
    company_post = Company_Post.objects.get(id=company_post_id)
    form = PostForm(request.POST)
    if form.is_valid():
        company_post = form.save(commit=False)
        company_post.save()
    return redirect('company_subforum/detail.html', company_subforum_id=company_subforum_id)

class Company_PostDelete(DeleteView):
    model = Post
    success_url = '/subforum/<int:subforum_id>/'

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

