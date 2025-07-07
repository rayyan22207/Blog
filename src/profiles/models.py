from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def user_profile_pic_path(instance, filename):
    return f'profile_pics/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    joined_at = models.DateTimeField(default=timezone.now)

    # Follow system
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    # Block system
    blocked_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='blocked_by',
        blank=True
    )

    def __str__(self):
        return self.user.username

    # Follow methods
    def follow(self, profile):
        """Follow another profile unless blocked."""
        if not self.is_blocking(profile) and not self.is_blocked_by(profile):
            self.following.add(profile)

    def unfollow(self, profile):
        """Unfollow another profile."""
        self.following.remove(profile)

    def is_following(self, profile):
        return self.following.filter(id=profile.id).exists()

    def is_followed_by(self, profile):
        return self.followers.filter(id=profile.id).exists()

    # Block methods
    def block(self, profile):
        """Block a user and remove follow if needed."""
        self.blocked_users.add(profile)
        self.unfollow(profile)  # Optional: unfollow when blocked
        profile.unfollow(self)  # Ensure mutual unfollow

    def unblock(self, profile):
        """Unblock a user."""
        self.blocked_users.remove(profile)

    def is_blocking(self, profile):
        return self.blocked_users.filter(id=profile.id).exists()

    def is_blocked_by(self, profile):
        return self.blocked_by.filter(id=self.id).exists()

