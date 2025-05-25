from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import CustomUser, UserProfile
from .forms import CustomUserCreationForm, UserProfileForm, MubisStudentForm, NonMubisStudentForm
from content.models import Content
from payments.models import Payment, Subscription
# from .error_views import custom_404, custom_500

def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return render(request, 'accounts/home.html')

def register_choice(request):
    """Registration choice page"""
    return render(request, 'accounts/register_choice.html')

def register_mubis_student(request):
    """Registration for MUBIS students"""
    if request.method == 'POST':
        form = MubisStudentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.student_type = 'mubis'
            user.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Your MUBIS number is: {user.mubis_special_no}')
            return redirect('accounts:login')
    else:
        form = MubisStudentForm()
    return render(request, 'accounts/register_mubis.html', {'form': form})

def register_non_mubis_student(request):
    """Registration for Non-MUBIS students"""
    if request.method == 'POST':
        form = NonMubisStudentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.student_type = 'non_mubis'
            user.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can upgrade to premium for exclusive content.')
            return redirect('accounts:login')
    else:
        form = NonMubisStudentForm()
    return render(request, 'accounts/register_non_mubis.html', {'form': form})

def register_lecturer(request):
    """Registration for lecturers"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'lecturer'
            user.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Lecturer account created for {username}!')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register_lecturer.html', {'form': form})

def register_president(request):
    """Registration for president"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'president'
            user.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'President account created for {username}!')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register_president.html', {'form': form})

@login_required
def dashboard(request):
    """Main dashboard view"""
    user = request.user
    context = {
        'user': user,
        'total_content': Content.objects.filter(is_active=True).count(),
        'premium_content': Content.objects.filter(content_type='premium', is_active=True).count(),
        'free_content': Content.objects.filter(content_type='free', is_active=True).count(),
    }
    
    if user.role == 'student':
        # Student dashboard
        if user.student_type == 'mubis':
            accessible_content = Content.objects.filter(is_active=True)
        else:
            if user.has_paid_access:
                accessible_content = Content.objects.filter(is_active=True)
            else:
                accessible_content = Content.objects.filter(content_type='free', is_active=True)
        
        context.update({
            'accessible_content': accessible_content[:5],  # Latest 5 content
            'recent_views': user.contentview_set.all()[:5],
        })
        return render(request, 'accounts/student_dashboard.html', context)
    
    elif user.role == 'lecturer':
        # Lecturer dashboard
        context.update({
            'my_content': Content.objects.filter(author=user, is_active=True)[:5],
            'total_my_content': Content.objects.filter(author=user).count(),
            'total_views': sum([content.views_count for content in Content.objects.filter(author=user)]),
        })
        return render(request, 'accounts/lecturer_dashboard.html', context)
    
    elif user.role == 'president':
        # President dashboard with access to all
        context.update({
            'total_users': CustomUser.objects.count(),
            'total_students': CustomUser.objects.filter(role='student').count(),
            'total_lecturers': CustomUser.objects.filter(role='lecturer').count(),
            'mubis_students': CustomUser.objects.filter(student_type='mubis').count(),
            'non_mubis_students': CustomUser.objects.filter(student_type='non_mubis').count(),
            'paid_users': CustomUser.objects.filter(has_paid_access=True).count(),
            'recent_content': Content.objects.filter(is_active=True)[:5],
            'recent_payments': Payment.objects.filter(status='completed')[:5],
        })
        return render(request, 'accounts/president_dashboard.html', context)

@login_required
def student_dashboard(request):
    """Student specific dashboard"""
    if request.user.role != 'student' and request.user.role != 'president':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    students = CustomUser.objects.filter(role='student')
    context = {
        'students': students,
        'mubis_students': students.filter(student_type='mubis'),
        'non_mubis_students': students.filter(student_type='non_mubis'),
        'paid_students': students.filter(has_paid_access=True),
    }
    return render(request, 'accounts/student_dashboard_view.html', context)

@login_required
def lecturer_dashboard(request):
    """Lecturer specific dashboard"""
    if request.user.role not in ['lecturer', 'president']:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    lecturers = CustomUser.objects.filter(role='lecturer')
    context = {
        'lecturers': lecturers,
        'lecturer_content': Content.objects.filter(author__role='lecturer'),
    }
    return render(request, 'accounts/lecturer_dashboard_view.html', context)

@login_required
def profile_view(request):
    """User profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    """Edit user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def user_list(request):
    """List all users (President only)"""
    if request.user.role != 'president':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    users = CustomUser.objects.all().order_by('-created_at')
    context = {'users': users}
    return render(request, 'accounts/user_list.html', context)


def custom_404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)
