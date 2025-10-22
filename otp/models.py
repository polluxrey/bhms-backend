from django.db import models
from boarder.models import Boarder
from django.utils import timezone
from datetime import timedelta


class OTP(models.Model):
    EXPIRY_MINUTES = 5

    boarder = models.ForeignKey(Boarder, on_delete=models.PROTECT)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        expiry_time = self.created_at + timedelta(minutes=self.EXPIRY_MINUTES)
        return timezone.now() > expiry_time
