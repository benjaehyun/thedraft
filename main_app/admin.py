from django.contrib import admin
from .models import Subforum, Post, Company, Photo, Company_Subforum, Company_Post, Comment, Company_Comment

# Register your models here.

admin.site.register(Subforum)
admin.site.register(Post)
admin.site.register(Company)
admin.site.register(Photo)
admin.site.register(Company_Subforum)
admin.site.register(Company_Post)
admin.site.register(Comment)
