from django.urls import path
from . import api_views

app_name = 'accounts_api'

urlpatterns = [
    path('user-stats/', api_views.user_stats_api, name='user_stats'),
    path('toggle-user-status/<int:user_id>/', api_views.toggle_user_status, name='toggle_user_status'),
]
