import uuid
import boto3
import os
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Subforum, Post, Company, Company_Subforum, Company_Post, Photo, Comment, Company_Comment, Company_Photo
from .forms import PostForm, CommentForm, Company_PostForm, Company_CommentForm, Company_SubforumForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Other View Functions
# Home view function is a Subforum index
def home(request): 
    subforums = Subforum.objects.all()
    return render(request, 'home.html', { 
        'subforums': subforums
    })

def about(request): 
    return render(request, 'about.html')

# Subforum CRUD Views
class SubforumCreate(LoginRequiredMixin, CreateView): 
    model = Subforum
    fields = ['title', 'pinned']

    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super().form_valid(form)

def subforums_detail(request, subforum_id): 
    subforum = Subforum.objects.get(id=subforum_id)
    post_form = PostForm()
    comment_form = CommentForm()
    return render(request, 'subforum/detail.html', {
        'subforum': subforum, 
        'post_form': post_form, 
        'comment_form': comment_form 
        })

class SubforumUpdate(LoginRequiredMixin, UpdateView): 
    model = Subforum
    fields = ['title', 'content']
    
    
@login_required
def add_post(request, subforum_id): 
    form = PostForm(request.POST)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.subforum_id = subforum_id
        new_post.user_id = request.user.id 
        new_post.save()
    return redirect('subforums_detail', subforum_id = subforum_id)

def update_post(request, post_id, subforum_id): #double check
    post = Post.objects.get(id=post_id)
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
    return redirect('subforum/<int:subforum_id>', subforum_id=subforum_id)

class PostDelete(LoginRequiredMixin, DeleteView): #probably add delete confirmation
    model = Post 
    def get_success_url(self): 
        subforum_id = self.object.subforum_id
        return reverse('subforums_detail', kwargs={'subforum_id': subforum_id})


@login_required
def add_comment(request, subforum_id, post_id): 
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_id = post_id
        new_comment.user_id = request.user.id 
        new_comment.save()
    return redirect('subforums_detail', subforum_id = subforum_id)

class CommentDelete(LoginRequiredMixin, DeleteView): #probably add delete confirmation
    model = Comment 
    def get_success_url(self): 
        subforum_id = self.object.post.subforum_id
        return reverse('subforums_detail', kwargs={'subforum_id': subforum_id})

class CompanyList(ListView): 
    model = Company 
    template_name = "company/index.html"

class CompanyDetail(DetailView): 
    model = Company 
    template_name = "company/detail.html"
    #query for subforums and pass the functionality of the company_subforum index 

class CompanyCreate(LoginRequiredMixin, CreateView): 
    model = Company 
    fields = '__all__'
    template_name = "company/form.html"

# Company_Subforum CRUD Views
# def company_subforum_create(request, company_id):
#     form = Company_SubforumForm(request.POST)
#     if form.is_valid(): 
#         new_company_subforum = form.save(commit=False)
#         new_company_subforum.company_id = company_id
#         new_company_subforum.save()
#     return redirect('company/detail.html', company_id = company_id)

class Company_SubforumCreate(LoginRequiredMixin, CreateView): 
    model = Company_Subforum
    fields = ['title', 'pinned', 'content']

    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.company = get_object_or_404(Company, pk=self.kwargs['company_id'])
        return super().form_valid(form)

  
class Company_SubforumUpdate(LoginRequiredMixin, UpdateView):
    model = Company_Subforum
    fields = 'title'

# Ben handling these
# def company_subfoums_index(request):
#     company_subforums = Company_Subforum.objects.all()
#     # Where should this live? I picked this one because this file already exists
#     return render(request, 'company_index', {
#         'company_subforums': company_subforums
#     }) 

def company_subforums_detail(request, company_id, company_subforum_id): 
    subforum = Company_Subforum.objects.get(id=company_subforum_id)
    post_form = Company_PostForm()
    comment_form = Company_CommentForm()
    return render(request, 'company/subforum/detail.html', {
        'subforum': subforum, 
        'post_form': post_form, 
        'comment_form': comment_form 
        })


# Company_Post CRUD Views
def add_company_post(request, company_id, company_subforum_id): 
    form = Company_PostForm(request.POST)
    if form.is_valid():
        new_company_post = form.save(commit=False)
        new_company_post.subforum_id = company_subforum_id
        new_company_post.user_id = request.user.id 
        new_company_post.save()
    return redirect('company_subforums_detail', company_id=company_id, company_subforum_id=company_subforum_id)

def update_company_post(request, company_post_id, company_subforum_id):
    company_post = Company_Post.objects.get(id=company_post_id)
    form = PostForm(request.POST)
    if form.is_valid():
        company_post = form.save(commit=False)
        company_post.save()
    return redirect('company_subforum/detail.html', company_subforum_id=company_subforum_id)

def add_company_comment(request, company_id, company_subforum_id, company_post_id):
    form = Company_CommentForm(request.POST)
    if form.is_valid():
        new_company_comment = form.save(commit=False)
        new_company_comment.post_id = company_post_id
        new_company_comment.user_id = request.user.id 
        new_company_comment.save()
    return redirect('company_subforums_detail', company_id=company_id, company_subforum_id = company_subforum_id)

class Company_CommentDelete(LoginRequiredMixin, DeleteView): #probably add delete confirmation
    model = Company_Comment 
    def get_success_url(self): 
        subforum_id = self.object.post.subforum_id
        company_id = self.object.post.subforum.company_id
        return reverse('company_subforums_detail', kwargs={'company_id': company_id, 'company_subforum_id': subforum_id})

class Company_PostDelete(LoginRequiredMixin, DeleteView): #delete confirmation 
    model = Company_Post
    def get_success_url(self): 
        subforum_id = self.object.subforum_id
        company_id = self.object.subforum.company_id 
        return reverse('company_subforums_detail', kwargs={'company_id': company_id, 'company_subforum_id': subforum_id})




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

