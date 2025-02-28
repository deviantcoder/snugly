from django.urls import path
from . import views

app_name = 'mentors'

urlpatterns = [
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentor-profile-overview/<str:username>/', views.mentor_profile_overview, name='mentor_profile_overview'),
    path('mentor-skills-list/<str:username>/', views.mentor_skills_list, name='mentor_skills_list'),
    path('dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('mentor-profile-info/', views.mentor_profile_info, name='mentor_profile_info'),
]