from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Creates the president and publicity secretary accounts'

    def handle(self, *args, **kwargs):
        # Create president account if it doesn't exist
        if not User.objects.filter(username='matthew').exists():
            User.objects.create_user(
                username='matthew',
                email='matthew@conasconnect.org',
                password='securepassword123',
                first_name='Matthew',
                last_name='President',
                user_type='president',
                is_staff=True,
            )
            self.stdout.write(self.style.SUCCESS('President account created successfully'))
        else:
            self.stdout.write(self.style.WARNING('President account already exists'))
            
        # Create publicity secretary account if it doesn't exist
        if not User.objects.filter(username='publicity').exists():
            User.objects.create_user(
                username='publicity',
                email='publicity@conasconnect.org',
                password='securepassword456',
                first_name='Publicity',
                last_name='Secretary',
                user_type='publicity',
                is_staff=True,
            )
            self.stdout.write(self.style.SUCCESS('Publicity Secretary account created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Publicity Secretary account already exists'))
