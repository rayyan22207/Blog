from django.contrib import admin
from .models import BlogPost, Comment, Like

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Like)