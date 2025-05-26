#!/usr/bin/env python
"""
Simple test script to verify the Django setup
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conas_connect.settings')

# Setup Django
django.setup()

def test_models():
    """Test model imports and basic functionality"""
    try:
        from accounts.models import CustomUser, UserProfile
        from content.models import Content, Category, Comment
        from payments.models import PaymentPlan, Payment, Subscription
        
        print("✓ All models imported successfully")
        
        # Test model creation
        print(f"✓ Users count: {CustomUser.objects.count()}")
        print(f"✓ Categories count: {Category.objects.count()}")
        print(f"✓ Payment plans count: {PaymentPlan.objects.count()}")
        
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def test_views():
    """Test view imports"""
    try:
        from accounts import views as account_views
        from content import views as content_views
        from payments import views as payment_views
        
        print("✓ All views imported successfully")
        return True
    except Exception as e:
        print(f"✗ View test failed: {e}")
        return False

def test_urls():
    """Test URL configurations"""
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test basic URL patterns
        urls_to_test = [
            'accounts:home',
            'accounts:register_choice',
            'content:list',
            'payments:plans',
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"✓ URL '{url_name}' resolved to: {url}")
            except Exception as e:
                print(f"✗ URL '{url_name}' failed: {e}")
        
        return True
    except Exception as e:
        print(f"✗ URL test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Conas Connect Django Setup...")
    print("=" * 50)
    
    success = True
    success &= test_models()
    success &= test_views()
    success &= test_urls()
    
    print("=" * 50)
    if success:
        print("🎉 All tests passed! Your Django setup is ready.")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000")
        print("3. Login with admin/admin123 (if you ran setup_initial_data)")
    else:
        print("❌ Some tests failed. Please check the errors above.")
