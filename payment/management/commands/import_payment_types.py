from django.core.management.base import BaseCommand
from payment.models import PaymentType


class Command(BaseCommand):
    help = "Loads data into payment type table"

    def handle(self, *args, **options):
        payment_types = [
            {"name": "Rent", "code": "RENT"},
            {"name": "Electricity", "code": "ELECTRICITY"},
            {"name": "Internet", "code": "INTERNET"},
            {"name": "Others", "code": "OTHER"}
        ]

        for payment_type in payment_types:
            PaymentType.objects.create(**payment_type)

        self.stdout.write(self.style.SUCCESS("Data loaded successfully!"))
