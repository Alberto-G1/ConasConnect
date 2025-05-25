from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_welcome_email(user):
    """Send welcome email to new users"""
    subject = 'Welcome to Conas Connect!'
    html_message = render_to_string('emails/welcome_email.html', {
        'user': user,
        'mubis_number': user.mubis_special_no if user.student_type == 'mubis' else None,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )

def send_payment_confirmation_email(user, payment):
    """Send payment confirmation email"""
    subject = 'Payment Confirmation - Conas Connect'
    html_message = render_to_string('emails/payment_confirmation.html', {
        'user': user,
        'payment': payment,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )

def generate_mubis_number():
    """Generate unique MUBIS number"""
    import random
    import string
    from .models import CustomUser
    
    while True:
        number = ''.join(random.choices(string.digits, k=7))
        if not CustomUser.objects.filter(mubis_special_no=number).exists():
            return number
