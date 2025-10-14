from django.core.management.base import BaseCommand
from config.models import BrandingConfig


class Command(BaseCommand):
    help = "Loads data into branding config table"

    def handle(self, *args, **options):
        obj = BrandingConfig(app_name="Rey's Boarding House")

        obj.save()

        self.stdout.write(self.style.SUCCESS(
            "Branding config created successfully!"))
