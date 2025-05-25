from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('president', 'President'),
    )
    
    STUDENT_TYPES = (
        ('mubis', 'MUBIS Student'),
        ('non_mubis', 'Non-MUBIS Student'),
    )
    
    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPES, null=True, blank=True)
    mubis_special_no = models.CharField(max_length=7, unique=True, null=True, blank=True)
    has_paid_access = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generate MUBIS special number for MUBIS students
        if self.student_type == 'mubis' and not self.mubis_special_no:
            self.mubis_special_no = self.generate_mubis_number()
            self.has_paid_access = True
        
        # Non-MUBIS students don't have paid access by default
        if self.student_type == 'non_mubis':
            self.mubis_special_no = None
            
        super().save(*args, **kwargs)
    
    def generate_mubis_number(self):
        """Generate a unique 7-digit MUBIS special number"""
        while True:
            number = ''.join(random.choices(string.digits, k=7))
            if not CustomUser.objects.filter(mubis_special_no=number).exists():
                return number
    
    def can_access_premium_content(self):
        """Check if user can access premium content"""
        return self.has_paid_access or self.role in ['lecturer', 'president']
    
    def can_upload_content(self):
        """Check if user can upload content"""
        return self.role in ['lecturer', 'president']
    
    def can_delete_content(self):
        """Check if user can delete content"""
        return self.role in ['lecturer', 'president']
    
    def can_access_all_dashboards(self):
        """Check if user can access all dashboards"""
        return self.role == 'president'

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
