from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from payments.utils import check_subscription_expiry

class SubscriptionMiddleware:
    """Middleware to check subscription status"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.role == 'student':
            if request.user.student_type == 'non_mubis' and request.user.has_paid_access:
                # Check if subscription is still valid
                if not check_subscription_expiry(request.user):
                    messages.warning(request, 'Your subscription has expired. Please renew to continue accessing premium content.')

        response = self.get_response(request)
        return response

class RoleBasedAccessMiddleware:
    """Middleware to handle role-based access control"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
