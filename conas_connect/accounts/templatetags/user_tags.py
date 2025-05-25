from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def user_role_badge(user):
    """Display user role as a badge"""
    role_colors = {
        'student': 'primary',
        'lecturer': 'success',
        'president': 'danger',
    }
    color = role_colors.get(user.role, 'secondary')
    return mark_safe(f'<span class="badge badge-{color}">{user.get_role_display()}</span>')

@register.filter
def student_type_badge(user):
    """Display student type as a badge"""
    if user.role != 'student':
        return ''
    
    if user.student_type == 'mubis':
        return mark_safe('<span class="badge badge-success">MUBIS</span>')
    else:
        return mark_safe('<span class="badge badge-warning">Non-MUBIS</span>')

@register.filter
def access_status_badge(user):
    """Display access status as a badge"""
    if user.can_access_premium_content():
        return mark_safe('<span class="badge badge-success">Premium Access</span>')
    else:
        return mark_safe('<span class="badge badge-secondary">Free Access</span>')

@register.simple_tag
def can_access_content(user, content):
    """Check if user can access specific content"""
    return content.can_user_access(user)

@register.simple_tag
def can_upload_content(user):
    """Check if user can upload content"""
    return user.can_upload_content()

@register.simple_tag
def can_delete_content(user):
    """Check if user can delete content"""
    return user.can_delete_content()
