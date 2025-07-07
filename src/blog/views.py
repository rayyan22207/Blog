from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import BlogPost, Like
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required

def home(request):
    posts = BlogPost.objects.filter(is_published=True)
    user = request.user

    # If user is authenticated, check likes
    if user.is_authenticated:
        post_ct = ContentType.objects.get_for_model(BlogPost)
        user_likes = Like.objects.filter(user=user, content_type=post_ct, object_id__in=[p.id for p in posts])
        liked_ids = set(like.object_id for like in user_likes)
        for post in posts:
            post.liked_by_user = post.id in liked_ids
    else:
        for post in posts:
            post.liked_by_user = False

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


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    if request.user.is_authenticated:
        ct = ContentType.objects.get_for_model(BlogPost)
        liked = Like.objects.filter(user=request.user, content_type=ct, object_id=post.id).exists()
        post.liked_by_user = liked
    else:
        post.liked_by_user = False

    return render(request, 'post_detail.html', {'post': post})