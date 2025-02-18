from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = "Creates a superuser if one does not exist"

    def handle(self, *args, **kwargs):
        email = "admin@gmail.com"
        name = "Admin"
        password = "admin@123"
        tc = True

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, name=name, tc=tc, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser {email} created successfully!"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser {email} already exists."))
