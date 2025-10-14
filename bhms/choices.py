from django.db import models

class Sex(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHER = "O", "Other / Prefer not to say"

class YearLevel(models.TextChoices):
    FIRST = "FIRST", "1st Year"
    SECOND = "SECOND", "2nd Year"
    THIRD = "THIRD", "3rd Year"
    FOURTH = "FOURTH", "4th Year"