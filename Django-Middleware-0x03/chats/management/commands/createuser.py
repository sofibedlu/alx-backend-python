from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Creates a new user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the new user')
        parser.add_argument('--password', type=str, help='Password for the new user')
        parser.add_argument('--email', type=str, help='Email for the new user')
        parser.add_argument('--first_name', type=str, help='First name for the new user')
        parser.add_argument('--last_name', type=str, help='Last name for the new user')
        parser.add_argument('--role', type=str, help='Role for the new user (guest, host, or admin)')


    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        password = options['password']
        email = options['email']
        first_name = options['first_name']
        last_name = options['last_name']
        role = options['role']

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f"User with email '{email}' already exists."))
            return

        # Hash the password
        hashed_password = make_password(password)

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            role=role
        )
        
        self.stdout.write(self.style.SUCCESS(f"User '{email}' created successfully with role '{role}'."))