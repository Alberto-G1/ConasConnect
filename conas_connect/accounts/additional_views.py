from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .decorators import role_required
from .models import CustomUser
from content.models import Content
from payments.models import Payment

@role_required(['president'])
def admin_dashboard(request):
    """Advanced admin dashboard for president"""
    # User statistics
    user_stats = {
        'total_users': CustomUser.objects.count(),
        'active_users': CustomUser.objects.filter(is_active=True).count(),
        'students': CustomUser.objects.filter(role='student').count(),
        'lecturers': CustomUser.objects.filter(role='lecturer').count(),
        'mubis_students': CustomUser.objects.filter(student_type='mubis').count(),
        'non_mubis_students': CustomUser.objects.filter(student_type='non_mubis').count(),
        'paid_users': CustomUser.objects.filter(has_paid_access=True).count(),
    }
    
    # Content statistics
    content_stats = {
        'total_content': Content.objects.count(),
        'active_content': Content.objects.filter(is_active=True).count(),
        'premium_content': Content.objects.filter(content_type='premium').count(),
        'free_content': Content.objects.filter(content_type='free').count(),
    }
    
    # Payment statistics
    payment_stats = {
        'total_payments': Payment.objects.count(),
        'completed_payments': Payment.objects.filter(status='completed').count(),
        'total_revenue': sum([p.amount for p in Payment.objects.filter(status='completed')]),
        'pending_payments': Payment.objects.filter(status='pending').count(),
    }
    
    # Recent activities
    recent_users = CustomUser.objects.order_by('-created_at')[:5]
    recent_content = Content.objects.order_by('-created_at')[:5]
    recent_payments = Payment.objects.order_by('-created_at')[:5]
    
    context = {
        'user_stats': user_stats,
        'content_stats': content_stats,
        'payment_stats': payment_stats,
        'recent_users': recent_users,
        'recent_content': recent_content,
        'recent_payments': recent_payments,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)

@role_required(['president'])
def manage_users(request):
    """Manage all users"""
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    
    users = CustomUser.objects.all()
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'accounts/manage_users.html', context)

@role_required(['president'])
def user_detail_admin(request, user_id):
    """Detailed view of a user for admin"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # User's content
    user_content = Content.objects.filter(author=user)
    
    # User's payments
    user_payments = Payment.objects.filter(user=user)
    
    # User's activity stats
    total_views = sum([content.views_count for content in user_content])
    
    context = {
        'viewed_user': user,
        'user_content': user_content,
        'user_payments': user_payments,
        'total_views': total_views,
        'content_count': user_content.count(),
        'payment_count': user_payments.count(),
    }
    
    return render(request, 'accounts/user_detail_admin.html', context)
