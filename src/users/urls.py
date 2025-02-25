from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register-choice/', views.register_choice, name='register_choice'),
    path('register-user/', views.register_user, name='register_user'),
    path('register-mentor/', views.register_mentor, name='register_mentor'),
]