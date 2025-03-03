from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserCreationForm, UserProfileForm


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/emails/verify_email_sent.html', {'title': 'Email Sent'})
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'title': 'Sign Up'
    }

    return render(request, 'users/register_user.html', context)


@login_required(login_url='accounts:login')
def edit_user_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, form_url_name='users:edit_user_profile')
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was updated')
            return redirect('users:edit_user_profile')

    form = UserProfileForm(instance=profile, form_url_name='users:edit_user_profile')

    context = {
        'title': 'Edit User Profile',
        'form': form,
    }

    return render(request, 'users/edit_user_profile.html', context)