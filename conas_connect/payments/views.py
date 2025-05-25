from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from .models import PaymentPlan, Payment, Subscription
from .forms import PaymentForm
import uuid

@login_required
def payment_plans(request):
    """Display available payment plans"""
    plans = PaymentPlan.objects.filter(is_active=True)
    user_subscription = None
    
    try:
        user_subscription = Subscription.objects.get(user=request.user, is_active=True)
        if user_subscription.is_expired():
            user_subscription.is_active = False
            user_subscription.save()
            request.user.has_paid_access = False
            request.user.save()
            user_subscription = None
    except Subscription.DoesNotExist:
        pass
    
    context = {
        'plans': plans,
        'user_subscription': user_subscription,
        'user': request.user,
    }
    return render(request, 'payments/plans.html', context)

@login_required
def initiate_payment(request, plan_id):
    """Initiate payment for a plan"""
    plan = get_object_or_404(PaymentPlan, id=plan_id, is_active=True)
    
    # Check if user already has active subscription
    try:
        active_subscription = Subscription.objects.get(user=request.user, is_active=True)
        if not active_subscription.is_expired():
            messages.warning(request, 'You already have an active subscription.')
            return redirect('payments:plans')
    except Subscription.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.plan = plan
            payment.amount = plan.price
            payment.transaction_id = uuid.uuid4()
            payment.save()
            
            messages.success(request, 'Payment initiated successfully! Please complete the payment.')
            return redirect('payments:payment_detail', transaction_id=payment.transaction_id)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'plan': plan,
    }
    return render(request, 'payments/initiate_payment.html', context)

@login_required
def payment_detail(request, transaction_id):
    """Payment detail and status"""
    payment = get_object_or_404(Payment, transaction_id=transaction_id, user=request.user)
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/payment_detail.html', context)

@login_required
def complete_payment(request, transaction_id):
    """Complete payment (simulate payment completion)"""
    payment = get_object_or_404(Payment, transaction_id=transaction_id, user=request.user)
    
    if payment.status == 'completed':
        messages.info(request, 'Payment already completed.')
        return redirect('payments:payment_detail', transaction_id=transaction_id)
    
    if request.method == 'POST':
        # Simulate payment completion
        payment.status = 'completed'
        payment.completed_at = timezone.now()
        payment.reference_number = f"REF{uuid.uuid4().hex[:8].upper()}"
        payment.save()
        
        # Create or update subscription
        end_date = timezone.now() + timedelta(days=payment.plan.duration_days)
        
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            defaults={
                'plan': payment.plan,
                'payment': payment,
                'end_date': end_date,
                'is_active': True,
            }
        )
        
        if not created:
            subscription.plan = payment.plan
            subscription.payment = payment
            subscription.end_date = end_date
            subscription.is_active = True
            subscription.save()
        
        # Update user access
        request.user.has_paid_access = True
        request.user.save()
        
        messages.success(request, 'Payment completed successfully! You now have premium access.')
        return redirect('accounts:dashboard')
    
    return render(request, 'payments/complete_payment.html', {'payment': payment})

@login_required
def payment_history(request):
    """User's payment history"""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'payments': payments,
    }
    return render(request, 'payments/payment_history.html', context)

@login_required
def subscription_detail(request):
    """User's subscription details"""
    try:
        subscription = Subscription.objects.get(user=request.user, is_active=True)
        if subscription.is_expired():
            subscription.is_active = False
            subscription.save()
            request.user.has_paid_access = False
            request.user.save()
            subscription = None
    except Subscription.DoesNotExist:
        subscription = None
    
    context = {
        'subscription': subscription,
    }
    return render(request, 'payments/subscription_detail.html', context)

@login_required
def cancel_subscription(request):
    """Cancel user's subscription"""
    try:
        subscription = Subscription.objects.get(user=request.user, is_active=True)
        if request.method == 'POST':
            subscription.is_active = False
            subscription.auto_renew = False
            subscription.save()
            
            request.user.has_paid_access = False
            request.user.save()
            
            messages.success(request, 'Subscription cancelled successfully.')
            return redirect('payments:plans')
        
        return render(request, 'payments/cancel_subscription.html', {'subscription': subscription})
    except Subscription.DoesNotExist:
        messages.error(request, 'No active subscription found.')
        return redirect('payments:plans')

@login_required
def admin_payments(request):
    """Admin view for all payments (President only)"""
    if request.user.role != 'president':
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    payments = Payment.objects.all().order_by('-created_at')
    total_revenue = sum([p.amount for p in payments.filter(status='completed')])
    
    context = {
        'payments': payments,
        'total_revenue': total_revenue,
        'completed_payments': payments.filter(status='completed').count(),
        'pending_payments': payments.filter(status='pending').count(),
    }
    return render(request, 'payments/admin_payments.html', context)
