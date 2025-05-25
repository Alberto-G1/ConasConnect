from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from accounts.utils import send_payment_confirmation_email

@receiver(post_save, sender=Payment)
def payment_completed(sender, instance, **kwargs):
    """Handle payment completion"""
    if instance.status == 'completed' and kwargs.get('update_fields') is None:
        # Send confirmation email
        send_payment_confirmation_email(instance.user, instance)
