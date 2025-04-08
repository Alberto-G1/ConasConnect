from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import MubisStudentRegistrationForm, NonMubisStudentRegistrationForm, CustomAuthenticationForm
from .models import User

def register_selection(request):
    return render(request, 'accounts/register_selection.html')

def register_mubis(request):
    if request.method == 'POST':
        form = MubisStudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = MubisStudentRegistrationForm()
    return render(request, 'accounts/register_mubis.html', {'form': form})

def register_non_mubis(request):
    if request.method == 'POST':
        form = NonMubisStudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('payment_options')
    else:
        form = NonMubisStudentRegistrationForm()
    return render(request, 'accounts/register_non_mubis.html', {'form': form})

def login_selection(request):
    return render(request, 'accounts/login_selection.html')

def login_user(request, user_type):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user_type == 'president' and user.is_president():
                    return redirect('president_dashboard')
                elif user_type == 'publicity' and user.is_publicity():
                    return redirect('publicity_dashboard')
                elif user_type == 'mubis' and user.is_mubis_student():
                    return redirect('index')
                elif user_type == 'non_mubis' and user.is_non_mubis_student():
                    if user.has_paid:
                        return redirect('index')
                    else:
                        return redirect('payment_options')
                else:
                    # If user type doesn't match, log them out and show error
                    from django.contrib.auth import logout
                    logout(request)
                    return render(request, 'accounts/login_error.html', {'message': 'Invalid user type for this login option.'})
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form': form,
        'user_type': user_type
    }
    return render(request, 'accounts/login.html', context)

@login_required
def payment_options(request):
    return render(request, 'accounts/payment_options.html')

@login_required
def president_dashboard(request):
    if not request.user.is_president():
        return redirect('index')
    return render(request, 'accounts/president_dashboard.html')

@login_required
def publicity_dashboard(request):
    if not request.user.is_publicity():
        return redirect('index')
    return render(request, 'accounts/publicity_dashboard.html')
