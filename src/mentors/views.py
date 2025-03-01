from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from users.models import AppUserProxy
from users.forms import MentorProfileForm

from utils.htmx_response import htmx_http_response


def mentor_list(request):
    mentors = AppUserProxy.objects.mentors()
    context = {
        'mentors': mentors,
        'head_title': 'Mentors',
    }
    return render(request, 'mentors/mentor_list.html', context)


def mentor_profile_overview(request, username):
    mentor = AppUserProxy.objects.get(username=username)
    skills = mentor.profile.all_skills
    context = {
        'profile': mentor.profile,
        'skills': skills,
    }
    return render(request, 'mentors/mentor_profile_overview.html', context)


def mentor_skills_list(request, username):
    user = AppUserProxy.objects.get(username=username)
    skills = user.profile.skills

    context = {
        'skills': skills,
    }

    return render(request, 'mentors/partials/skills_list.html', context)


@login_required(login_url='users:login')
def mentor_dashboard(request):
    mentor = request.user

    context = {
        'mentor': mentor,
        'head_title': 'Dashboard',
    }

    return render(request, 'mentors/mentor_dashboard.html', context)


@login_required(login_url='users:login')
def edit_profile(request):
    mentor = request.user

    form = MentorProfileForm(instance=mentor.profile)

    if request.method == 'POST' and request.htmx:
        form = MentorProfileForm(request.POST, request.FILES, instance=mentor.profile)
        if form.is_valid():
            form.save()
            
            message = {
                'text': 'Profile was updated',
                'type': 'success'
            }

            return htmx_http_response(204, message, event='profileInfoChanged')

    context = {
        'form': form,
    }

    return render(request, 'mentors/edit_profile.html', context)


@login_required(login_url='users:login')
def mentor_profile_info(request):
    mentor = request.user
    context = {
        'mentor': mentor,
    }
    return render(request, 'mentors/partials/mentor_profile_info.html', context)
