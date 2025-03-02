from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register-user/', views.register_user, name='register_user'),
]