from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('register-choice/', views.register_choice, name='register_choice'),

    path('register-user/', views.register, kwargs={'role': 'user'}, name='register_user'),
    path('register-mentor/', views.register, kwargs={'role': 'mentor'}, name='register_mentor'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),
]