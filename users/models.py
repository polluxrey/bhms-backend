from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)

    @property
    def role(self):
        if self.groups.filter(name="Owner").exists():
            return "owner"
        elif self.groups.filter(name="Boarder").exists():
            return "boarder"
        else:
            return "user"

    @property
    def phone_number(self):
        # Return phone on User if exists1
        if self.phone:
            return self.phone

        """
        # If boarder, get from related Boarder
        if self.role == "boarder":
            try:
                return self.boarder.phone_number
            except AttributeError:
                return None
        """

        return None
