from django.forms import ModelForm
from .models import Post, Comment,Company_Subforum, Company_Post, Company_Comment, Subforum 

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

