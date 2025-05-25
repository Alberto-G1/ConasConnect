from django import template
from django.utils.safestring import mark_safe
from ..models import Content, Category

register = template.Library()

@register.filter
def content_type_badge(content):
    """Display content type as a badge"""
    if content.content_type == 'premium':
        return mark_safe('<span class="badge badge-warning">Premium</span>')
    else:
        return mark_safe('<span class="badge badge-info">Free</span>')

@register.inclusion_tag('content/tags/recent_content.html')
def recent_content(user, limit=5):
    """Display recent content accessible to user"""
    if user.can_access_premium_content():
        content = Content.objects.filter(is_active=True)[:limit]
    else:
        content = Content.objects.filter(content_type='free', is_active=True)[:limit]
    
    return {'content_list': content, 'user': user}

@register.inclusion_tag('content/tags/categories_list.html')
def categories_list():
    """Display all categories"""
    categories = Category.objects.all()
    return {'categories': categories}

@register.simple_tag
def content_count_by_type(content_type):
    """Get count of content by type"""
    return Content.objects.filter(content_type=content_type, is_active=True).count()
