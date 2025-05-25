from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'student_type', 'mubis_special_no', 'has_paid_access', 'is_active']
    list_filter = ['role', 'student_type', 'has_paid_access', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'mubis_special_no']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'student_type', 'mubis_special_no', 'has_paid_access', 'phone_number', 'profile_picture')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'student_type', 'phone_number')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'birth_date']
    search_fields = ['user__username', 'user__email']

admin.site.register(CustomUser, CustomUserAdmin)
