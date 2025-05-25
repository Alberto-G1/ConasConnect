from django.urls import path
from . import additional_views

app_name = 'accounts_admin'

urlpatterns = [
    path('admin-dashboard/', additional_views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', additional_views.manage_users, name='manage_users'),
    path('user-detail/<int:user_id>/', additional_views.user_detail_admin, name='user_detail_admin'),
]
