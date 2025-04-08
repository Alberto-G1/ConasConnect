from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def index(request):
    # Different content based on user type
    context = {}
    if request.user.is_authenticated:
        if request.user.is_president():
            return redirect('president_dashboard')
        elif request.user.is_publicity():
            return redirect('publicity_dashboard')
        
        # For students, we'll show different content based on their type
        context['is_mubis'] = request.user.is_mubis_student()
        context['has_paid'] = request.user.has_paid
    
    return render(request, 'main/index.html', context)

@login_required
def resources(request):
    # Check if user has access to resources
    if request.user.is_mubis_student() or request.user.has_paid or request.user.is_staff:
        return render(request, 'main/resources.html')
    else:
        # Redirect non-paying non-Mubis students to payment page
        return redirect('payment_options')

@login_required
def premium_content(request):
    # Only allow access to Mubis students or paying non-Mubis students
    if request.user.is_mubis_student() or request.user.has_paid or request.user.is_staff:
        return render(request, 'main/premium_content.html')
    else:
        return redirect('payment_options')


def about(request):
    return render(request, 'main/about.html')

def events(request):
    return render(request, 'main/events.html')

def team(request):
    return render(request, 'main/team.html')

def advertise(request):
    return render(request, 'main/advertise.html')

def opportunities(request):
    return render(request, 'main/opportunities.html')

def contact(request):
    return render(request, 'main/contact.html')
