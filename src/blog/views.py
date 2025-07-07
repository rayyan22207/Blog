from django.shortcuts import render
from .models import BlogPost

# Create your views here.
def home(request):
    posts = BlogPost.objects.all() 
    for post in posts:
        if post.image:
            print(post.image.url)
        else:
            print('none')
    return render(request, 'home.html', {'posts': posts})