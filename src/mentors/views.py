from django.shortcuts import render, redirect

from .forms import MentorCreationForm


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