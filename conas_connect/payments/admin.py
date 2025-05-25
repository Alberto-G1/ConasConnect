from django.contrib import admin
from .models import PaymentPlan, Payment, Subscription

@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'plan', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['transaction_id', 'user__username', 'reference_number']
    readonly_fields = ['transaction_id']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'start_date', 'end_date', 'is_active', 'auto_renew']
    list_filter = ['is_active', 'auto_renew', 'start_date', 'end_date']
    search_fields = ['user__username', 'plan__name']
