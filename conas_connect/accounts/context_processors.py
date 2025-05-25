from .models import CustomUser

def user_stats(request):
    """Add user statistics to template context"""
    if request.user.is_authenticated and request.user.role == 'president':
        return {
            'total_users_count': CustomUser.objects.count(),
            'students_count': CustomUser.objects.filter(role='student').count(),
            'lecturers_count': CustomUser.objects.filter(role='lecturer').count(),
        }
    return {}
