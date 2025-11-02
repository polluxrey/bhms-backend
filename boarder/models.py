from django.db import models
from bhms.utils import clean_text
from bhms.choices import Sex, YearLevel, DegreeProgram
from bhms.utils import path_and_rename


class Boarder(models.Model):
    # Name
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)

    # Demographics
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=1, choices=Sex.choices)

    # Address
    province = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)

    # Academic Information
    degree_program = models.CharField(
        max_length=10, choices=DegreeProgram.choices)
    year_level = models.CharField(max_length=10, choices=YearLevel.choices)

    # Contact Details
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    # Boarding Details
    room_number = models.CharField(max_length=10)
    move_in_date = models.DateField()
    move_out_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Profile Image
    profile_photo = models.ImageField(
        upload_to=path_and_rename("boarders"),
        blank=True,
        null=True
    )

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name}, {self.first_name} {self.middle_name}"
        return f"{self.last_name}, {self.first_name}"

    @property
    def full_address(self):
        return f"{self.barangay}, {self.municipality}, {self.province}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.last_name = clean_text(self.last_name)
            self.first_name = clean_text(self.first_name)
            self.middle_name = clean_text(self.middle_name)
            self.province = clean_text(self.province)
            self.municipality = clean_text(self.municipality)
            self.barangay = clean_text(self.barangay)
            self.degree_program = clean_text(self.degree_program)
            self.email = clean_text(
                self.email, uppercase=False, lowercase=True)

        if self.move_out_date and self.is_active:
            self.is_active = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
