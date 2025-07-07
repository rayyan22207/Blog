# blog/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def user_profile_pic_path(instance, filename):
    # upload path: media/profile_pics/user_<id>/<filename>
    return f'profile_pics/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    # Extra fields
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
