from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost, Comment
from profiles.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

@require_POST
@login_required
def api_like_post(request, slug):
    post = BlogPost.objects.get(slug=slug)
    user = request.user

    # toggle like
    existing_like = post.likes.filter(user=user).first()
    if existing_like:
        existing_like.delete()
    else:
        post.likes.create(user=user)

    return JsonResponse({
        'success': True,
        'total_likes': post.likes.count()
    })

@require_POST
@login_required
def api_comment_post(request, slug):
    import json
    data = json.loads(request.body)
    content = data.get('content')

    post = BlogPost.objects.get(slug=slug)
    comment = post.comments.create(user=request.user, content=content)

    return JsonResponse({
        'success': True,
        'content': comment.content,
        'username': comment.user.username
    })


@login_required
@require_POST
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.profile
    user_profile = request.user.profile

    if user_profile.is_following(target_profile):
        user_profile.unfollow(target_profile)
        return JsonResponse({'success': True, 'following': False})
    else:
        user_profile.follow(target_profile)
        return JsonResponse({'success': True, 'following': True})

@login_required
@require_POST
def toggle_block(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.profile
    user_profile = request.user.profile

    if user_profile.is_blocking(target_profile):
        user_profile.unblock(target_profile)
        return JsonResponse({'success': True, 'blocking': False})
    else:
        user_profile.block(target_profile)
        return JsonResponse({'success': True, 'blocking': True})
