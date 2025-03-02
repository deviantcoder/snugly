from django.shortcuts import render, redirect

from .forms import UserCreationForm


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