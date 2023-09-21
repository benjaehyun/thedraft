from django.contrib import admin
from .models import Subforum, Post, Company, Company_Subforum, Company_Post, Comment, Company_Comment, Photo, Company_Photo, Subforum_Likes, Company_Subforum_Likes, Job_Application, Application_Component, Component_Note, Pdf
# Register your models here.

admin.site.register(Subforum)
admin.site.register(Post)
admin.site.register(Company)
admin.site.register(Photo)
admin.site.register(Company_Subforum)
admin.site.register(Company_Comment)
admin.site.register(Company_Post)
admin.site.register(Company_Photo)
admin.site.register(Comment)
admin.site.register(Subforum_Likes)
admin.site.register(Company_Subforum_Likes)
admin.site.register(Job_Application)
admin.site.register(Application_Component)
admin.site.register(Component_Note)
admin.site.register(Pdf)
