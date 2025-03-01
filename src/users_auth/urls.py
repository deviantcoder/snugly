from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register-choice/', views.register_choice, name='register_choice'),
    path('register-user/', views.register_user, name='register_user'),
    path('register-mentor/', views.register_mentor, name='register_mentor'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),
]