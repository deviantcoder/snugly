from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .forms import UserCreationForm, MentorCreationForm, MentorProfileForm, UserProfileForm

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if all([username, password]):
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome back!')
                return redirect('/')
            else:
                messages.warning(request, 'Username or password is incorrect')
                return redirect('users:login')
        else:
            messages.warning(request, 'Username or password is incorrect')
            return redirect('users:login')

    context = {
        'head_title': 'Sign In'
    }

    return render(request, 'users/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')


def register_choice(request):
    if request.user.is_authenticated:
        return redirect('/')

    context = {
        'head_title': 'Sign Up Choice'
    }

    return render(request, 'users/register_choice.html', context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/emails/verify_email_sent.html')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'head_title': 'Sign Up'
    }

    return render(request, 'users/register_user.html', context)


def register_mentor(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = MentorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/emails/verify_email_sent.html')
    else:
        form = MentorCreationForm()

    context = {
        'form': form,
        'head_title': 'Sign Up as Mentor'
    }
    
    return render(request, 'users/register_mentor.html', context)


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and token_generator.check_token(user, token):
        user.is_active = True
        if hasattr(user, 'email_verified'):
            user.email_verified = True
        user.save()
        login(request, user)
        messages.success(request, "Welcome!")
        return redirect('users:edit_profile')
    
    return render(request, 'users/emails/verify_email_failed.html')


@login_required(login_url='users:login')
def edit_profile(request):
    user = request.user

    if user.role == 'mentor':
        form = MentorProfileForm(instance=user.profile)
    elif user.role == 'user':
        form = UserProfileForm(instance=user.profile)

    if request.method == 'POST':
        if user.role == 'mentor':
            form = MentorProfileForm(request.POST, request.FILES, instance=user.profile)
        elif user.role == 'user':
            form = UserProfileForm(request.POST, request.FILES, instance=user.profile)

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
        'head_title': 'Edit Profile',
        'profile': user.profile,
    }
    
    return render(request, 'users/edit_profile.html', context)
