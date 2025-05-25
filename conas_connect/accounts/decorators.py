from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def role_required(allowed_roles):
    """Decorator to check if user has required role"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('accounts:dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def premium_required(view_func):
    """Decorator to check if user has premium access"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.can_access_premium_content():
            messages.error(request, 'You need premium access to view this content.')
            return redirect('payments:plans')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def content_author_required(view_func):
    """Decorator to check if user is content author or president"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        content_id = kwargs.get('pk')
        if content_id:
            from content.models import Content
            try:
                content = Content.objects.get(pk=content_id)
                if not (request.user == content.author or request.user.role == 'president'):
                    messages.error(request, 'You do not have permission to modify this content.')
                    return redirect('content:detail', pk=content_id)
            except Content.DoesNotExist:
                messages.error(request, 'Content not found.')
                return redirect('content:list')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
