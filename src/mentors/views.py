from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from accounts.models import AppUserProxy


User = get_user_model()


def mentors_list(request):
    mentors = AppUserProxy.objects.mentors().filter(email_verified=True)

    context = {
        'mentors': mentors,
        'title': 'Find a Mentor'
    }

    return render(request, 'mentors/mentors_list.html', context)


def profile_overview(request, username: str):
    profile = get_object_or_404(User, username=username).profile

    context = {
        'profile': profile,
    }

    return render(request, 'mentors/partials/profile_overview.html', context)


def mentor_profile(request, username: str):
    profile = get_object_or_404(User, username=username).profile

    context = {
        'profile': profile,
        'title': profile.full_name
    }

    return render(request, 'mentors/mentor_profile.html', context)