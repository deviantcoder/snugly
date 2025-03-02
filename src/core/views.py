from django.shortcuts import render


def welcome_view(request):
    context = {
        'title': 'Welcome'
    }
    return render(request, 'welcome.html', context)