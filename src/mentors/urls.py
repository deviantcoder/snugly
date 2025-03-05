from django.urls import path

from . import views

app_name = 'mentors'

urlpatterns = [
    path('', views.mentors_list, name='mentors_list'),
    path('profile-overview/<str:username>/', views.profile_overview, name='profile_overview'),
]