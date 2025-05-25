from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Content, ContentView
from django.db.models import F

@login_required
@require_http_methods(["POST"])
def toggle_content_status(request, content_id):
    """API endpoint to toggle content active status"""
    content = get_object_or_404(Content, id=content_id)
    
    # Check permissions
    if not (request.user == content.author or request.user.role == 'president'):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    content.is_active = not content.is_active
    content.save()
    
    return JsonResponse({
        'success': True,
        'is_active': content.is_active,
        'message': f'Content {"activated" if content.is_active else "deactivated"} successfully'
    })

@login_required
@require_http_methods(["GET"])
def content_stats_api(request):
    """API endpoint for content statistics"""
    if request.user.role not in ['lecturer', 'president']:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    if request.user.role == 'lecturer':
        content_filter = {'author': request.user}
    else:
        content_filter = {}
    
    stats = {
        'total_content': Content.objects.filter(**content_filter).count(),
        'active_content': Content.objects.filter(is_active=True, **content_filter).count(),
        'premium_content': Content.objects.filter(content_type='premium', **content_filter).count(),
        'free_content': Content.objects.filter(content_type='free', **content_filter).count(),
        'total_views': sum([c.views_count for c in Content.objects.filter(**content_filter)]),
    }
    
    return JsonResponse(stats)
