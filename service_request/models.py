from django.db import models, IntegrityError, transaction
from boarder.models import Boarder
from bhms.choices import RequestType, RequestStatus
from bhms.utils import path_and_rename, generate_random_ref


class ServiceRequest(models.Model):
    reference_number = models.CharField(
        max_length=7, unique=True, editable=False)
    boarder = models.ForeignKey(
        Boarder, on_delete=models.CASCADE, related_name='service_requests')
    request_type = models.CharField(
        max_length=15,
        choices=RequestType.choices,
        default=RequestType.OTHER
    )
    description = models.TextField()
    status = models.CharField(
        max_length=15,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )
    attachment = models.ImageField(
        upload_to=path_and_rename("requests"),
        blank=True,
        null=True
    )
    admin_remarks = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk is None and not self.reference_number:
            MAX_ATTEMPTS = 10
            for _ in range(MAX_ATTEMPTS):
                new_ref = generate_random_ref()
                if not ServiceRequest.objects.filter(reference_number=new_ref).exists():
                    self.reference_number = new_ref
                    break
                else:
                    raise RuntimeError(
                        "Failed to generate a unique reference number.")

        super().save(*args, **kwargs)

    def __str__(self):
        boarder_name = self.boarder.full_name if self.boarder else "No Boarder"
        return f"{boarder_name} - {self.get_request_type_display()} ({self.get_status_display()})"
