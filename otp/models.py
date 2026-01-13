from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from boarder.models import Boarder


class OTP(models.Model):
    class Channel(models.TextChoices):
        SMS = "sms", "SMS"
        EMAIL = "email", "Email"

    EXPIRY_MINUTES = 5

    boarder = models.ForeignKey(
        Boarder,
        on_delete=models.PROTECT,
        related_name="otps"
    )

    channel = models.CharField(
        max_length=10,
        choices=Channel.choices,
        blank=True,
        null=True,
    )

    code = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r"^\d{6}$",
                message="OTP must be 6 digits"
            )
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['boarder', 'channel', 'created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(
                minutes=self.EXPIRY_MINUTES
            )
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.boarder} - {self.channel} - {self.code} ({'active' if self.is_active else 'inactive'})"
