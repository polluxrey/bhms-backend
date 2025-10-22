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


class PaymentStatus(models.TextChoices):
    PENDING_REVIEW = "PENDING", "Pending Review"
    CONFIRMED = "CONFIRMED", "Confirmed"
    REFUNDED = "REFUNDED", "Refunded"


class RequestType(models.TextChoices):
    COMPLAINT = "COMPLAINT", "Complaint"
    MAINTENANCE = "MAINTENANCE", "Maintenance Request"
    SUPPLIES = "SUPPLIES", "Request for Supplies"
    CLARIFICATION = "CLARIFICATION", "Clarification"
    OTHER = "OTHER", "Other"


class RequestStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    RESOLVED = "RESOLVED", "Resolved"
    REJECTED = "REJECTED", "Rejected"
