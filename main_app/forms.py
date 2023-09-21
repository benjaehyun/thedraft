from django.forms import ModelForm
from .models import Post, Comment,Company_Subforum, Company_Post, Company_Comment, Subforum, Job_Application, Component_Note, Application_Component

class PostForm(ModelForm): 
    class Meta: 
        model = Post 
        fields = ['content']

class SubforumForm(ModelForm): 
    class Meta: 
        model = Subforum 
        fields = ['title', 'pinned', 'content']

class CommentForm(ModelForm): 
    class Meta: 
        model = Comment 
        fields = ['content']

class Company_SubforumForm(ModelForm): 
    class Meta: 
        model = Company_Subforum 
        fields = ['title', 'pinned', 'content']

class Company_PostForm(ModelForm): 
    class Meta: 
        model = Company_Post 
        fields = ['content']

class Company_CommentForm(ModelForm): 
    class Meta: 
        model = Company_Comment 
        fields = ['content']

class Job_ApplicationForm(ModelForm): 
    class Meta: 
        model = Job_Application
        fields = ['role', 'url', 'company', 'description', 'salary', 'date', 'location', 'status']

class Component_NoteForm(ModelForm): 
    class Meta: 
        model = Component_Note
        fields = ['content']

class Application_ComponentForm(ModelForm): 
    class Meta: 
        model = Application_Component
        fields = ['type', 'date', 'contact', 'description']

class StatusForm(ModelForm): 
    class Meta: 
        model = Job_Application
        fields = ['status']
