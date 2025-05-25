from .models import Content, Category

def content_stats(request):
    """Add content statistics to template context"""
    return {
        'total_content_count': Content.objects.filter(is_active=True).count(),
        'premium_content_count': Content.objects.filter(content_type='premium', is_active=True).count(),
        'free_content_count': Content.objects.filter(content_type='free', is_active=True).count(),
        'categories_list': Category.objects.all()[:5],  # Top 5 categories
    }
