from django.contrib import admin
from .models import Subforum, Post, Company, Photo, Company_Subforum, Company_Post

# Register your models here.

admin.site.register(Subforum)
admin.site.register(Post)
admin.site.register(Company)
admin.site.register(Photo)
admin.site.register(Company_Subforum)
admin.site.register(Company_Post)
