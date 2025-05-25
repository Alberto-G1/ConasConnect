from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from content.models import Category
from payments.models import PaymentPlan

User = get_user_model()

class Command(BaseCommand):
    help = 'Set up initial data for the application'

    def handle(self, *args, **options):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@conasconnect.com',
                password='admin123',
                role='president'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create sample categories
        categories = [
            {'name': 'Programming', 'description': 'Programming tutorials and resources'},
            {'name': 'Mathematics', 'description': 'Mathematical concepts and problems'},
            {'name': 'Science', 'description': 'Scientific articles and research'},
            {'name': 'Business', 'description': 'Business and entrepreneurship content'},
            {'name': 'General', 'description': 'General educational content'},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create payment plans
        plans = [
            {
                'name': 'Monthly Premium',
                'description': 'Access to all premium content for 1 month',
                'price': 10.00,
                'duration_days': 30
            },
            {
                'name': 'Quarterly Premium',
                'description': 'Access to all premium content for 3 months',
                'price': 25.00,
                'duration_days': 90
            },
            {
                'name': 'Annual Premium',
                'description': 'Access to all premium content for 1 year',
                'price': 80.00,
                'duration_days': 365
            },
        ]

        for plan_data in plans:
            plan, created = PaymentPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f'Created payment plan: {plan.name}')

        self.stdout.write(self.style.SUCCESS('Initial data setup completed!'))
