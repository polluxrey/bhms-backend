from django.core.management.base import BaseCommand
from payment.models import PaymentMethod


class Command(BaseCommand):
    help = "Loads data into payment method table"

    def handle(self, *args, **options):
        payment_methods = [
            {"name": "Cash", "code": "CASH"},
            {"name": "GCash", "code": "GCASH"}
        ]

        for payment_method in payment_methods:
            PaymentMethod.objects.create(**payment_method)

        self.stdout.write(self.style.SUCCESS("Data loaded successfully!"))
