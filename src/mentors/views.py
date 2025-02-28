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
    context = {
        'mentor': mentor.mentorprofile,
    }
    return render(request, 'mentors/mentor_profile_overview.html', context)
