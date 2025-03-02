from django.urls import path
from . import views

app_name = 'mentors'

urlpatterns = [
    path('register-mentor/', views.register_mentor, name='register_mentor'),
]