from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/mubis-student/', views.register_mubis_student, name='register_mubis_student'),
    path('register/non-mubis-student/', views.register_non_mubis_student, name='register_non_mubis_student'),
    path('register/lecturer/', views.register_lecturer, name='register_lecturer'),
    path('register/president/', views.register_president, name='register_president'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/students/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/lecturers/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('users/', views.user_list, name='user_list'),
]
