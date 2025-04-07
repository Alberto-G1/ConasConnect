from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('resources/', views.resources, name='resources'),
    path('team/', views.team, name='team'),
    path('advertise/', views.advertise, name='advertise'),
    path('opportunities/', views.opportunities, name='opportunities'),
    path('contact/', views.contact, name='contact'),
]
