from django.urls import path
from . import views

app_name = 'mentors'

urlpatterns = [
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentor-profile-overview/<str:username>/', views.mentor_profile_overview, name='mentor_profile_overview'),
]