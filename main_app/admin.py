from django.contrib import admin
from .models import Subforum, Post, Company

# Register your models here.

admin.site.register(Subforum)
admin.site.register(Post)
admin.site.register(Company)
