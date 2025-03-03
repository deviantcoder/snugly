from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import MentorCreationForm, MentorProfileForm


def register_mentor(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = MentorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/emails/verify_email_sent.html', {'title': 'Email Sent'})
    else:
        form = MentorCreationForm()

    context = {
        'form': form,
        'title': 'Sign Up as Mentor'
    }
    
    return render(request, 'mentors/register_mentor.html', context)


@login_required(login_url='accounts:login')
def edit_mentor_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = MentorProfileForm(request.POST, request.FILES, instance=profile, form_url_name='mentors:edit_mentor_profile')
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was updated')
            return redirect('mentors:edit_mentor_profile')
        
    form = MentorProfileForm(instance=profile, form_url_name='mentors:edit_mentor_profile')

    context = {
        'title': 'Edit Mentor Profile',
        'form': form,
    }

    return render(request, 'mentors/edit_mentor_profile.html', context)