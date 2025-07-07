from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    posts = BlogPost.objects.all() 
    for post in posts:
        if post.image:
            print(post.image.url)
        else:
            print('none')
    return render(request, 'home.html', {'posts': posts})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # assign current user
            post.save()
            return redirect('home')  # or redirect to post detail
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})
