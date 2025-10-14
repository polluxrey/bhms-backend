from django.core.management.base import BaseCommand
from boarder.models import Boarder


class Command(BaseCommand):
    help = "Loads data into boarder table"

    def handle(self, *args, **options):
        boarders = [
            {
                "last_name": "REY",
                "first_name": "POLLUX",
                "middle_name": "MURILLO",
                "date_of_birth": "1998-09-04",
                "sex": "M",
                "province": "MARINDUQUE",
                "municipality": "SANTA CRUZ",
                "barangay": "BUYABOD",
                "degree_program": "BS COMPUTER SCIENCE",
                "year_level": "FIRST",
                "email": "bhms@yopmail.com",
                "phone_number": "09984585080",
                "room_number": "3FR1",
                "move_in_date": "2025-10-01",
            },
            {
                "last_name": "REY",
                "first_name": "POLLUX",
                "middle_name": "MURILLO",
                "date_of_birth": "1998-09-04",
                "sex": "M",
                "province": "MARINDUQUE",
                "municipality": "SANTA CRUZ",
                "barangay": "BUYABOD",
                "degree_program": "BS COMPUTER SCIENCE",
                "year_level": "FIRST",
                "email": "bhms_2@yopmail.com",
                "phone_number": "09763046669",
                "room_number": "3FR1",
                "move_in_date": "2025-10-01",
            }
        ]

        for boarder in boarders:
            Boarder.objects.create(**boarder)

        self.stdout.write(self.style.SUCCESS("Data loaded successfully!"))
