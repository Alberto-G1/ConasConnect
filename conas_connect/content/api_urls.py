from django.urls import path
from . import api_views

app_name = 'content_api'

urlpatterns = [
    path('content-stats/', api_views.content_stats_api, name='content_stats'),
    path('toggle-content-status/<int:content_id>/', api_views.toggle_content_status, name='toggle_content_status'),
]
