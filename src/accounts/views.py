from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


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
                return redirect('accounts:login')
        else:
            messages.warning(request, 'Username or password is incorrect')
            return redirect('accounts:login')

    context = {
        'title': 'Sign In'
    }

    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, 'Logged out')
    return redirect('/')


def register_choice(request):
    if request.user.is_authenticated:
        return redirect('/')

    context = {
        'title': 'Sign Up Choice'
    }

    return render(request, 'accounts/register_choice.html', context)


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

        redirect_url = 'mentors:edit_mentor_profile' if user.role == User.Roles.MENTOR else 'users:edit_user_profile'

        return redirect(redirect_url)
    user.delete()
    return render(request, 'accounts/emails/verify_email_failed.html', {'title': 'Email Failed'})

