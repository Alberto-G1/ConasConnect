from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('plans/', views.payment_plans, name='plans'),
    path('initiate/<int:plan_id>/', views.initiate_payment, name='initiate_payment'),
    path('detail/<uuid:transaction_id>/', views.payment_detail, name='payment_detail'),
    path('complete/<uuid:transaction_id>/', views.complete_payment, name='complete_payment'),
    path('history/', views.payment_history, name='payment_history'),
    path('subscription/', views.subscription_detail, name='subscription_detail'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('admin/', views.admin_payments, name='admin_payments'),
]
