from django import forms
from .models import Payment, PaymentPlan

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

class PaymentPlanForm(forms.ModelForm):
    class Meta:
        model = PaymentPlan
        fields = ['name', 'description', 'price', 'duration_days', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }
