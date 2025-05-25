from django.urls import path
from . import additional_views

app_name = 'content_extra'

urlpatterns = [
    path('analytics/', additional_views.content_analytics, name='analytics'),
    path('category/<int:category_id>/', additional_views.content_by_category, name='by_category'),
    path('author/<int:author_id>/', additional_views.content_by_author, name='by_author'),
    path('premium/', additional_views.premium_content_list, name='premium_list'),
]
