import os
from django.core.management.base import BaseCommand
from users.models import User
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Creates or gets owner users from environment variables."

    def handle(self, *args, **options):
        load_dotenv()

        users = [
            {
                "username": "mmrey",
                "email": "mmorillo_rey@yahoo.com",
                "password": os.getenv("OWNER_PASSWORD_1"),
            },
            {
                "username": "pmrey",
                "email": "polluxrey@gmail.com",
                "password": os.getenv("OWNER_PASSWORD_2"),
            },
        ]

        for data in users:
            try:
                user, created = User.objects.get_or_create(
                    email=data["email"], username=data["username"])
                if created:
                    user.set_password(data["password"])
                    user.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"Created user: {user.email}"))
                else:
                    self.stdout.write(f"User already exists: {user.email}")
            except Exception as e:
                self.stderr.write(
                    f"Error creating user '{data['email']}': {e}")
