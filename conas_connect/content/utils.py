from django.db.models import Q
from .models import Content

def get_user_accessible_content(user):
    """Get content accessible to user based on their permissions"""
    if user.can_access_premium_content():
        return Content.objects.filter(is_active=True)
    else:
        return Content.objects.filter(content_type='free', is_active=True)

def search_content(query, user):
    """Search content based on user permissions"""
    accessible_content = get_user_accessible_content(user)
    
    if query:
        return accessible_content.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    return accessible_content
