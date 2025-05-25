from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import Http404
from accounts.decorators import role_required, premium_required
from .models import Content, Category, Comment

@role_required(['lecturer', 'president'])
def content_analytics(request):
    """Content analytics for lecturers and president"""
    if request.user.role == 'lecturer':
        contents = Content.objects.filter(author=request.user)
    else:
        contents = Content.objects.all()
    
    # Analytics data
    total_content = contents.count()
    total_views = sum([content.views_count for content in contents])
    premium_content = contents.filter(content_type='premium').count()
    free_content = contents.filter(content_type='free').count()
    
    # Top performing content
    top_content = contents.order_by('-views_count')[:10]
    
    # Content by category
    category_stats = contents.values('category__name').annotate(
        count=Count('id'),
        total_views=Count('contentview')
    ).order_by('-count')
    
    context = {
        'total_content': total_content,
        'total_views': total_views,
        'premium_content': premium_content,
        'free_content': free_content,
        'top_content': top_content,
        'category_stats': category_stats,
    }
    
    return render(request, 'content/analytics.html', context)

def content_by_category(request, category_id):
    """List content by category"""
    category = get_object_or_404(Category, id=category_id)
    
    contents = Content.objects.filter(category=category, is_active=True)
    
    # Filter based on user access
    if not request.user.can_access_premium_content():
        contents = contents.filter(content_type='free')
    
    paginator = Paginator(contents, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'content/content_by_category.html', context)

def content_by_author(request, author_id):
    """List content by author"""
    author = get_object_or_404(id=author_id, role__in=['lecturer', 'president'])
    
    contents = Content.objects.filter(author=author, is_active=True)
    
    # Filter based on user access
    if not request.user.can_access_premium_content():
        contents = contents.filter(content_type='free')
    
    paginator = Paginator(contents, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    
    return render(request, 'content/content_by_author.html', context)

@premium_required
def premium_content_list(request):
    """List all premium content"""
    contents = Content.objects.filter(content_type='premium', is_active=True)
    
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    if search_query:
        contents = contents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category_id:
        contents = contents.filter(category_id=category_id)
    
    paginator = Paginator(contents, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    
    return render(request, 'content/premium_content.html', context)
