from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def role(self):
        if self.groups.filter(name="Owner").exists():
            return "owner"
        elif self.groups.filter(name="Boarder").exists():
            return "boarder"
        else:
            return "user"
