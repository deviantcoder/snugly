from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from .forms import MentorCreationForm, MentorProfileForm, UserCreationForm, UserProfileForm


def register_choice(request):
    if request.user.is_authenticated:
        return redirect('/')

    context = {
        'title': 'Sign Up Choice'
    }

    return render(request, 'profiles/register_choice.html', context)


def register(request, role: str = 'user'):
    if request.user.is_authenticated:
        return redirect('/')
    
    role_config = {
        'user': {
            'form': UserCreationForm,
            'title': 'Sign Up',
            'template': 'profiles/register_user.html',
        },
        'mentor': {
            'form': MentorCreationForm,
            'title': 'Sign Up as Mentor',
            'template': 'profiles/register_mentor.html',
        }
    }

    if role not in role_config:
        return Http404()
    
    config = role_config[role]

    if request.method == 'POST':
        form = config['form'](request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'emails/verify_email_sent.html', {'title': 'Email Sent'})
    else:
        form = config['form']()

    context = {
        'form': form,
        'title': config['title'],
    }

    return render(request, config['template'], context)


@login_required(login_url='accounts:login')
def edit_profile(request, role: str = 'user'):
    profile = request.user.profile

    role_map = {
        request.user.Roles.USER: 'user',
        request.user.Roles.MENTOR: 'mentor',
    }

    user_role = role_map.get(request.user.role, 'user')\
    
    if role != user_role:
        return render(request, '404.html')

    role_config = {
        'user': {
            'form': UserProfileForm,
            'title': 'Edit User Profile',
            'template': 'profiles/edit_user_profile.html',
            'form_url': 'profiles:edit_user_profile',
            'redirect_url': 'profiles:edit_user_profile',
        },
        'mentor': {
            'form': MentorProfileForm,
            'title': 'Edit Mentor Profile',
            'template': 'profiles/edit_mentor_profile.html',
            'form_url': 'profiles:edit_mentor_profile',
            'redirect_url': 'profiles:edit_mentor_profile',
        }
    }

    if role not in role_config:
        return Http404()
    
    config = role_config[role]

    if request.method == 'POST':
        form = config['form'](request.POST, request.FILES, instance=profile, form_url_name=config['form_url'])
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was updated')
            return redirect(config['redirect_url'])
    else:
        form = config['form'](instance=profile, form_url_name=config['form_url'])

    context = {
        'form': form,
        'title': config['title'],
    }

    return render(request, config['template'], context)
