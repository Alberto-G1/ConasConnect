from django.urls import path
from . import views

urlpatterns = [
    # Registration URLs
    path('register/', views.register_selection, name='register_selection'),
    path('register/mubis/', views.register_mubis, name='register_mubis'),
    path('register/non-mubis/', views.register_non_mubis, name='register_non_mubis'),
    
    # Login URLs
    path('login/', views.login_selection, name='login_selection'),
    path('login/president/', views.login_president, name='login_president'),
    path('login/publicity/', views.login_publicity, name='login_publicity'),
    path('login/mubis/', views.login_mubis, name='login_mubis'),
    path('login/non-mubis/', views.login_non_mubis, name='login_non_mubis'),
    
    # Dashboard URLs
    path('dashboard/president/', views.president_dashboard, name='president_dashboard'),
    path('dashboard/publicity/', views.publicity_dashboard, name='publicity_dashboard'),
    
    # Payment URL
    path('payment-options/', views.payment_options, name='payment_options'),
    
    # Logout URL
    path('logout/', views.logout_view, name='logout'),
]
