from django.shortcuts import render
from users.models import AppUserProxy



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
