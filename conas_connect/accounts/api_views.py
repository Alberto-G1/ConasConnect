from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import CustomUser

@login_required
@require_http_methods(["GET"])
def user_stats_api(request):
    """API endpoint for user statistics"""
    if request.user.role != 'president':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    stats = {
        'total_users': CustomUser.objects.count(),
        'students': CustomUser.objects.filter(role='student').count(),
        'lecturers': CustomUser.objects.filter(role='lecturer').count(),
        'mubis_students': CustomUser.objects.filter(student_type='mubis').count(),
        'non_mubis_students': CustomUser.objects.filter(student_type='non_mubis').count(),
        'paid_users': CustomUser.objects.filter(has_paid_access=True).count(),
    }
    
    return JsonResponse(stats)

@login_required
@require_http_methods(["POST"])
def toggle_user_status(request, user_id):
    """API endpoint to toggle user active status"""
    if request.user.role != 'president':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    return JsonResponse({
        'success': True,
        'is_active': user.is_active,
        'message': f'User {"activated" if user.is_active else "deactivated"} successfully'
    })
