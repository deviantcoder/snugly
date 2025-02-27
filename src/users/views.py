from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages

from .forms import UserCreationForm, MentorCreationForm

User = get_user_model()


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
                messages.success(request, 'Successfully logged in')
                return redirect('/')
            else:
                messages.warning(request, 'Username or password is incorrect')
                return redirect('users:login')
        else:
            messages.warning(request, 'Username or password is incorrect')
            return redirect('users:login')

    context = {}
    return render(request, 'users/login.html', context)


def register_choice(request):
    if request.user.is_authenticated:
        return redirect('/')

    context = {
        'head_title': 'Sign Up Choice'
    }
    return render(request, 'users/register_choice.html')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

    context = {
        'form': form,
        'head_title': 'Sign Up'
    }
    return render(request, 'users/register_user.html', context)


def register_mentor(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = MentorCreationForm()

    if request.method == 'POST':
        form = MentorCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

    context = {
        'form': form,
        'head_title': 'Sign Up as Mentor'
    }
    return render(request, 'users/register_mentor.html', context)