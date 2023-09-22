import uuid
import boto3
import os
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Subforum, Post, Company, Company_Subforum, Company_Post, Comment, Company_Comment, Photo, Company_Photo, Subforum_Likes, Company_Subforum_Likes, Job_Application, Pdf, Application_Component, Component_Note
from .forms import PostForm, CommentForm, Company_PostForm, Company_CommentForm, Company_SubforumForm, SubforumForm, Job_ApplicationForm, Component_NoteForm, Application_ComponentForm, StatusForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.exceptions import PermissionDenied

def home(request): 
    subforums = Subforum.objects.all()
    return render(request, 'home.html', { 
        'subforums': subforums
    })

def about(request): 
    return render(request, 'about.html')

@login_required
def subforums_new(request): 
    subforum_form = SubforumForm()
    return render(request, 'subforum/form.html', {
        'subforum_form': subforum_form
        })

@login_required
def subforums_create(request): 
    form = SubforumForm(request.POST)
    try: 
        if form.is_valid():
            new_subforum = form.save(commit=False)
            new_subforum.user_id = request.user.id 
            new_subforum.save()
        request_files = request.FILES.getlist('photo-file', None)
        print(f'request_files: {request_files}')
        for photo_file in request_files:
            print(f'photofile: {photo_file} ')
            if photo_file:
                s3 = boto3.client('s3')
                key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
                try:
                    bucket = os.environ['S3_BUCKET']
                    print(f'bucket: {bucket} ')
                    s3.upload_fileobj(photo_file, bucket, key)
                    url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                    print(f'url: {url} ')
                    Photo.objects.create(url=url, subforum=new_subforum)
                except Exception as e:
                    print('An error occurred uploading file to S3')
                    print(e)
        return redirect('subforums_detail', subforum_id = new_subforum.id)
    except Exception as e: 
        return HttpResponseServerError(e)
        

def subforums_detail(request, subforum_id): 
    subforum = Subforum.objects.get(id=subforum_id)
    post_form = PostForm()
    comment_form = CommentForm()
    likes = len(Subforum_Likes.objects.filter(subforum=subforum_id))
    try: 
        subforum_like = Subforum_Likes.objects.get(subforum=subforum, user=request.user)
        is_liked=True
    except: 
        is_liked = False
    return render(request, 'subforum/detail.html', {
        'subforum': subforum, 
        'post_form': post_form, 
        'comment_form': comment_form, 
        'likes': likes, 
        'is_liked': is_liked
        })

class SubforumUpdate(LoginRequiredMixin, UpdateView): 
    model = Subforum
    fields = ['title', 'content']

    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(SubforumUpdate, self).dispatch(
            request, *args, **kwargs)

@login_required
def subforums_like(request, subforum_id): 
    subforum = Subforum.objects.get(id=subforum_id)
    print(f'subforum: {subforum} ')
    try:
        subforum_like = Subforum_Likes.objects.get(subforum=subforum, user=request.user)
        print(f'subforum_like: {subforum_like} ')
        subforum_like.delete()
        is_liked=False
    except Subforum_Likes.DoesNotExist:
        Subforum_Likes.objects.create(subforum=subforum, user=request.user)
        is_liked=True
    likes = len(Subforum_Likes.objects.filter(subforum=subforum_id))
    return JsonResponse({"success": True, 'likes': likes, 'is_liked': is_liked})
    
    
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

    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(PostDelete, self).dispatch(
            request, *args, **kwargs)


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
    
    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(CommentDelete, self).dispatch(
            request, *args, **kwargs)

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


@login_required
def company_subforums_new(request, company_id): 
    subforum_form = Company_SubforumForm()
    company = Company.objects.get(id=company_id)
    return render(request, 'company/subforum/form.html', {
        'subforum_form': subforum_form, 
        'company': company
        })

@login_required
def company_subforums_create(request, company_id): 
    form = Company_SubforumForm(request.POST)
    try: 
        if form.is_valid():
            new_subforum = form.save(commit=False)
            new_subforum.user_id = request.user.id 
            new_subforum.company_id = company_id
            new_subforum.save()
        request_files = request.FILES.getlist('photo-file', None)
        print(f'request_files: {request_files}')
        for photo_file in request_files:
            print(f'photofile: {photo_file} ')
            if photo_file:
                s3 = boto3.client('s3')
                key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
                try:
                    bucket = os.environ['S3_BUCKET']
                    print(f'bucket: {bucket} ')
                    s3.upload_fileobj(photo_file, bucket, key)
                    url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                    print(f'url: {url} ')
                    Company_Photo.objects.create(url=url, subforum=new_subforum)
                except Exception as e:
                    print('An error occurred uploading file to S3')
                    print(e)
        return redirect('company_subforums_detail', company_id = company_id, company_subforum_id = new_subforum.id)
    except Exception as e: 
        return HttpResponseServerError(e)

  
class Company_SubforumUpdate(LoginRequiredMixin, UpdateView):
    model = Company_Subforum
    fields = ['title', 'content']

    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(Company_SubforumUpdate, self).dispatch(
            request, *args, **kwargs)


def company_subforums_detail(request, company_id, company_subforum_id): 
    subforum = Company_Subforum.objects.get(id=company_subforum_id)
    post_form = Company_PostForm()
    comment_form = Company_CommentForm()
    likes = len(Company_Subforum_Likes.objects.filter(subforum=company_subforum_id))
    try: 
        subforum_like = Company_Subforum_Likes.objects.get(subforum=subforum, user=request.user)
        is_liked=True
    except: 
        is_liked = False
    return render(request, 'company/subforum/detail.html', {
        'subforum': subforum, 
        'likes': likes, 
        'is_liked': is_liked,
        'post_form': post_form, 
        'comment_form': comment_form 
        })

@login_required
def company_subforums_like(request, company_id, company_subforum_id): 
    subforum = Company_Subforum.objects.get(id=company_subforum_id)
    print(f'subforum: {subforum} ')
    try:
        subforum_like = Company_Subforum_Likes.objects.get(subforum=subforum, user=request.user)
        print(f'subforum_like: {subforum_like} ')
        subforum_like.delete()
        is_liked=False
    except Company_Subforum_Likes.DoesNotExist:
        Company_Subforum_Likes.objects.create(subforum=subforum, user=request.user)
        is_liked=True
    likes = len(Company_Subforum_Likes.objects.filter(subforum=company_subforum_id))
    return JsonResponse({"success": True, 'likes': likes, 'is_liked': is_liked})


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

    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(Company_CommentDelete, self).dispatch(
            request, *args, **kwargs)


class Company_PostDelete(LoginRequiredMixin, DeleteView): #delete confirmation 
    model = Company_Post

    def get_success_url(self): 
        subforum_id = self.object.subforum_id
        company_id = self.object.subforum.company_id 
        return reverse('company_subforums_detail', kwargs={'company_id': company_id, 'company_subforum_id': subforum_id})

    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(Company_PostDelete, self).dispatch(
            request, *args, **kwargs)


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

def profile(request, user_id): 
    applications = Job_Application.objects.filter(user=user_id)
    return render(request, 'profile/detail.html', { 
        'applications': applications
    })

def applications_new(request, user_id): 
    application_form = Job_ApplicationForm()
    return render(request, 'profile/application/form.html', {
        'application_form': application_form
        })


def applications_create(request, user_id): 
    form = Job_ApplicationForm(request.POST)
    try: 
        if form.is_valid():
            new_application = form.save(commit=False)
            new_application.user_id = request.user.id #this might not work
            new_application.save()
        pdf_file = request.FILES.get('pdf-file', None)
        print(f'pdffile: {pdf_file} ')
        if pdf_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + pdf_file.name[pdf_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                print(f'bucket: {bucket} ')
                s3.upload_fileobj(pdf_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                print(f'url: {url} ')
                Pdf.objects.create(url=url, job_application=new_application, user=request.user)
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)
        return redirect('applications_detail', user_id=user_id, application_id=new_application.id)
    except Exception as e: 
        return HttpResponseServerError(e)


def applications_detail(request, user_id, application_id): 
    application = Job_Application.objects.get(id=application_id)
    pdf = Pdf.objects.get(job_application=application_id) 
    note_form = Component_NoteForm()
    status_form = StatusForm()
    component_form = Application_ComponentForm()
    print(f'pdf: {pdf.url}')
    return render(request, 'profile/application/detail.html', {
        'application': application, 
        'pdf': pdf,
        'note_form': note_form, 
        'status_form':status_form,
        'component_form': component_form
        })

class Job_ApplicationDelete(LoginRequiredMixin, DeleteView): #delete confirmation 
    model = Job_Application

    def get_success_url(self): 
        user_id = self.object.user_id
        return reverse('profile', kwargs={'user_id': user_id})

    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(Job_ApplicationDelete, self).dispatch(
            request, *args, **kwargs)
    
class Application_ComponentDelete(LoginRequiredMixin, DeleteView): #delete confirmation 
    model = Application_Component

    def get_success_url(self): 
        user_id = self.object.user_id
        application_id = self.object.application_id
        return reverse('applications_detail', kwargs={'user_id': user_id, 'application_id': application_id})

    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(Application_ComponentDelete, self).dispatch(
            request, *args, **kwargs)

class Component_NoteDelete(LoginRequiredMixin, DeleteView): #delete confirmation 
    model = Component_Note

    def get_success_url(self): 
        user_id = self.object.user_id
        component = self.object.component
        return reverse('applications_detail', kwargs={'user_id': user_id, 'application_id': component.application_id})

    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(Component_NoteDelete, self).dispatch(
            request, *args, **kwargs)

@login_required
def add_note(request, user_id, application_id, component_id): 
    form = Component_NoteForm(request.POST)
    if form.is_valid():
        new_note = form.save(commit=False)
        new_note.component_id = component_id
        new_note.user_id = request.user.id 
        new_note.save()
    return redirect('applications_detail', user_id = user_id, application_id=application_id)

@login_required
def add_component(request, user_id, application_id): 
    form = Application_ComponentForm(request.POST)
    if form.is_valid():
        new_component = form.save(commit=False)
        new_component.application_id = application_id
        new_component.user_id = request.user.id 
        new_component.save()
    return redirect('applications_detail', user_id = user_id, application_id=application_id)

class Job_ApplicationUpdate(LoginRequiredMixin, UpdateView): 
    model = Job_Application
    fields = '__all__'

    def user_passes_test(self,request):
        if request.user.is_authenticated: 
            self.object = self.get_object()
            return self.object.user == request.user 
        return False 
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(Job_ApplicationUpdate, self).dispatch(
            request, *args, **kwargs)
    
@login_required
def status_update(request, user_id, application_id): 
    application = Job_Application.objects.get(id=application_id)
    form = StatusForm(request.POST, instance=application)
    if form.is_valid():
        new_status = form.save(commit=False)
        new_status.save(update_fields= ['status'] )
    return redirect('applications_detail', user_id = user_id, application_id=application_id)

def liked(request, user_id): 
    user = request.user
    return render(request, 'profile/liked.html', {
        'user': user
    }  )

def faq(request): 
    return render(request, 'faq.html')

def help(request): 
    return render(request, 'help.html')