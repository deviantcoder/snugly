from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import UserCreationForm, MentorCreationForm


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