from django.utils import timezone
from datetime import timedelta
from .models import Subscription

def check_subscription_expiry(user):
    """Check if user's subscription has expired"""
    try:
        subscription = Subscription.objects.get(user=user, is_active=True)
        if subscription.is_expired():
            subscription.is_active = False
            subscription.save()
            user.has_paid_access = False
            user.save()
            return False
        return True
    except Subscription.DoesNotExist:
        return False

def calculate_subscription_end_date(plan):
    """Calculate subscription end date based on plan duration"""
    return timezone.now() + timedelta(days=plan.duration_days)
