from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import Profile
from .forms import ProfileForm


def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_obj)
    viewer = request.user.profile if request.user.is_authenticated else None

    is_own_profile = request.user == user_obj
    is_following = viewer.is_following(profile) if viewer and not is_own_profile else False
    is_blocking = viewer.is_blocking(profile) if viewer and not is_own_profile else False

    context = {
        'profile_user': user_obj,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'is_blocking': is_blocking,
        'followers_count': profile.followers.count(),
        'following_count': profile.following.count(),
        'blocked_count': profile.blocked_by.count(),
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})
