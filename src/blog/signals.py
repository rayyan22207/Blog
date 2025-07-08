from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Like

from profiles.models import Profile  # assuming this is where followers are tracked


@receiver(post_save, sender=BlogPost)
def notify_followers_on_new_post(sender, instance, created, **kwargs):
    if created:
        author = instance.author
        try:
            followers = Profile.objects.get(user=author).followers.all()
            for follower in followers:
                print(f"[New Post] Notify {follower.user.username}: {author.username} just posted '{instance.title}' ({instance.slug})")
        except Profile.DoesNotExist:
            print(f"[New Post] Author profile not found for {author.username}")


@receiver(post_save, sender=Like)
def notify_on_like(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    content = instance.content_object

    if isinstance(content, BlogPost):
        # Like on a blog post
        author = content.author
        if author and user != author:
            print(f"[Like] Notify {author.username}: {user.username} liked your post '{content.title}'")

    elif isinstance(content, Comment):
        comment = content
        comment_author = comment.user
        post_author = comment.post.author

        # Notify the comment author (if not the liker)
        if comment_author and user != comment_author:
            print(f"[Like] Notify {comment_author.username}: {user.username} liked your comment on '{comment.post.title}'")

        # Also notify the post author (if not the same as liker or comment author)
        if post_author and post_author != user and post_author != comment_author:
            print(f"[Like] Notify {post_author.username}: {user.username} liked a comment on your post '{comment.post.title}'")

    else:
        print(f"[Like] {user.username} liked '{str(content)}'")


@receiver(post_save, sender=Comment)
def notify_on_comment(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        author = post.author
        commenter = instance.user
        if author and commenter and author != commenter:
            print(f"[Comment] Notify {author.username}: {commenter.username} commented on your post '{post.title}'")
