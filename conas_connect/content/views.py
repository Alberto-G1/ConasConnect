from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Content, Category, Comment, ContentView
from .forms import ContentForm, CommentForm, CategoryForm

@login_required
def content_list(request):
    """List all accessible content for user"""
    user = request.user
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    content_type = request.GET.get('type', '')
    
    # Base queryset
    contents = Content.objects.filter(is_active=True)
    
    # Filter based on user access
    if not user.can_access_premium_content():
        contents = contents.filter(content_type='free')
    
    # Apply filters
    if search_query:
        contents = contents.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_id:
        contents = contents.filter(category_id=category_id)
    
    if content_type:
        contents = contents.filter(content_type=content_type)
    
    # Pagination
    paginator = Paginator(contents, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_type': content_type,
    }
    return render(request, 'content/content_list.html', context)

@login_required
def content_detail(request, pk):
    """Content detail view"""
    content = get_object_or_404(Content, pk=pk, is_active=True)
    
    # Check if user can access this content
    if not content.can_user_access(request.user):
        messages.error(request, 'You need premium access to view this content.')
        return redirect('payments:plans')
    
    # Record view
    view, created = ContentView.objects.get_or_create(
        content=content,
        user=request.user
    )
    
    if created:
        # Increment view count
        Content.objects.filter(pk=pk).update(views_count=F('views_count') + 1)
    
    # Handle comment form
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.content = content
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('content:detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    comments = content.comments.all()
    related_content = Content.objects.filter(
        category=content.category,
        is_active=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'content': content,
        'comment_form': comment_form,
        'comments': comments,
        'related_content': related_content,
    }
    return render(request, 'content/content_detail.html', context)

@login_required
def content_create(request):
    """Create new content (Lecturer and President only)"""
    if not request.user.can_upload_content():
        messages.error(request, 'You do not have permission to upload content.')
        return redirect('content:list')
    
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.save()
            messages.success(request, 'Content created successfully!')
            return redirect('content:detail', pk=content.pk)
    else:
        form = ContentForm()
    
    return render(request, 'content/content_create.html', {'form': form})

@login_required
def content_edit(request, pk):
    """Edit content"""
    content = get_object_or_404(Content, pk=pk)
    
    # Check permissions
    if not (request.user == content.author or request.user.role == 'president'):
        messages.error(request, 'You do not have permission to edit this content.')
        return redirect('content:detail', pk=pk)
    
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Content updated successfully!')
            return redirect('content:detail', pk=pk)
    else:
        form = ContentForm(instance=content)
    
    return render(request, 'content/content_edit.html', {'form': form, 'content': content})

@login_required
def content_delete(request, pk):
    """Delete content"""
    content = get_object_or_404(Content, pk=pk)
    
    # Check permissions
    if not (request.user == content.author or request.user.role == 'president'):
        messages.error(request, 'You do not have permission to delete this content.')
        return redirect('content:detail', pk=pk)
    
    if request.method == 'POST':
        content.delete()
        messages.success(request, 'Content deleted successfully!')
        return redirect('content:list')
    
    return render(request, 'content/content_delete.html', {'content': content})

@login_required
def my_content(request):
    """List user's own content"""
    if not request.user.can_upload_content():
        messages.error(request, 'Access denied.')
        return redirect('content:list')
    
    contents = Content.objects.filter(author=request.user).order_by('-created_at')
    
    paginator = Paginator(contents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'content/my_content.html', {'page_obj': page_obj})

@login_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.all().order_by('name')
    return render(request, 'content/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    """Create new category (Lecturer and President only)"""
    if not request.user.can_upload_content():
        messages.error(request, 'You do not have permission to create categories.')
        return redirect('content:category_list')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('content:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'content/category_create.html', {'form': form})

@login_required
def comment_delete(request, pk):
    """Delete comment"""
    comment = get_object_or_404(Comment, pk=pk)
    
    # Check permissions
    if not (request.user == comment.user or request.user.role == 'president'):
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('content:detail', pk=comment.content.pk)
    
    content_pk = comment.content.pk
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('content:detail', pk=content_pk)
