from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.content_list, name='list'),
    path('<int:pk>/', views.content_detail, name='detail'),
    path('create/', views.content_create, name='create'),
    path('<int:pk>/edit/', views.content_edit, name='edit'),
    path('<int:pk>/delete/', views.content_delete, name='delete'),
    path('my-content/', views.my_content, name='my_content'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
