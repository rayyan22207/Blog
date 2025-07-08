from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Like
from profiles.models import Profile
from events.utils import send_notification_to_user


@receiver(post_save, sender=BlogPost)
def notify_followers_on_new_post(sender, instance, created, **kwargs):
    if created:
        author = instance.author
        try:
            followers = Profile.objects.get(user=author).followers.all()
            for follower in followers:
                send_notification_to_user(
                    follower.user.id,
                    f"{author.username} just posted: “{instance.title}”"
                )
        except Profile.DoesNotExist:
            pass  # No profile for author — skip


@receiver(post_save, sender=Like)
def notify_on_like(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    content = instance.content_object

    if isinstance(content, BlogPost):
        author = content.author
        if author and user != author:
            send_notification_to_user(
                author.id,
                f"{user.username} liked your post “{content.title}”."
            )

    elif isinstance(content, Comment):
        comment = content
        comment_author = comment.user
        post_author = comment.post.author

        if comment_author and user != comment_author:
            send_notification_to_user(
                comment_author.id,
                f"{user.username} liked your comment on “{comment.post.title}”."
            )

        if post_author and post_author != user and post_author != comment_author:
            send_notification_to_user(
                post_author.id,
                f"{user.username} liked a comment on your post “{comment.post.title}”."
            )


@receiver(post_save, sender=Comment)
def notify_on_comment(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        author = post.author
        commenter = instance.user
        if author and commenter and author != commenter:
            send_notification_to_user(
                author.id,
                f"{commenter.username} commented on your post “{post.title}”."
            )
