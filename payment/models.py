
from django.db import models
from bhms.models import BaseCodeName
from bhms.utils import path_and_rename
from boarder.models import Boarder

# Create your models here.


class PaymentType(BaseCodeName):
    pass


class PaymentMethod(BaseCodeName):
    pass


class Payment(models.Model):
    boarder = models.ForeignKey(
        Boarder, on_delete=models.PROTECT, related_name="payments")
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)

    receipt = models.ImageField(
        upload_to=path_and_rename("payments"),
        blank=True,
        null=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.boarder.last_name} - {self.payment_type.name} - ₱{self.amount}"
