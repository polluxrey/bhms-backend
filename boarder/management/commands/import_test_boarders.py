from django.core.management.base import BaseCommand
from boarder.models import Boarder


class Command(BaseCommand):
    help = "Loads data into boarder table"

    def handle(self, *args, **options):
        boarders = [
            # {
            #     "last_name": "REY",
            #     "first_name": "POLLUX",
            #     "middle_name": "MURILLO",
            #     "date_of_birth": "1998-09-04",
            #     "sex": "M",
            #     "province": "MARINDUQUE",
            #     "municipality": "SANTA CRUZ",
            #     "barangay": "BUYABOD",
            #     "degree_program": "BS COMPUTER SCIENCE",
            #     "year_level": "FIRST",
            #     "email": "bhms@yopmail.com",
            #     "phone_number": "09984585080",
            #     "room_number": "3FR1",
            #     "move_in_date": "2025-10-01",
            # },
            # {
            #     "last_name": "REY",
            #     "first_name": "MARILOU",
            #     "middle_name": "MURILLO",
            #     "date_of_birth": "1971-01-26",
            #     "sex": "F",
            #     "province": "MARINDUQUE",
            #     "municipality": "SANTA CRUZ",
            #     "barangay": "BUYABOD",
            #     "degree_program": "BS NURSING",
            #     "year_level": "FIRST",
            #     "email": "bhms_2@yopmail.com",
            #     "phone_number": "09763046669",
            #     "room_number": "3FR1",
            #     "move_in_date": "2025-10-01",
            # }
            {
                "last_name": "BAUTISTA",
                "first_name": "CAMILLE",
                "middle_name": "TAGBAGO",
                "sex": "F",
                "province": "MARINDUQUE",
                "municipality": "SANTA CRUZ",
                "barangay": "MORALES",
                "degree_program": "BSIT",
                "year_level": "FIRST",
                "email": "camillebautista208@gmail.com",
                "phone_number": "09263835531",
                "room_number": "2FR3",
                "move_in_date": "2025-07-28",
            },
            {
                "last_name": "CANO",
                "first_name": "JESSA MARIE",
                "middle_name": "DE LA CRUZ",
                "sex": "F",
                "province": "MARINDUQUE",
                "municipality": "SANTA CRUZ",
                "barangay": "BUYABOD",
                "degree_program": "BSBA",
                "year_level": "FIRST",
                "email": "bhms_3@yopmail.com",
                "phone_number": "09150182046",
                "room_number": "2FR3",
                "move_in_date": "2025-07-28",
            }
        ]

        for boarder in boarders:
            Boarder.objects.create(**boarder)

        self.stdout.write(self.style.SUCCESS("Data loaded successfully!"))
