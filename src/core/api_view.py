from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost, Comment

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
