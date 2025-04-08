from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('president', 'President'),
        ('publicity', 'Publicity Secretary'),
        ('mubis', 'Mubis Student'),
        ('non_mubis', 'Non-Mubis Student'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='non_mubis')
    email = models.EmailField(unique=True)
    mubis_number = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Mubis number must be 10 digits',
            ),
        ]
    )
    has_paid = models.BooleanField(default=False)
    
    def is_president(self):
        return self.user_type == 'president'
    
    def is_publicity(self):
        return self.user_type == 'publicity'
    
    def is_mubis_student(self):
        return self.user_type == 'mubis'
    
    def is_non_mubis_student(self):
        return self.user_type == 'non_mubis'
