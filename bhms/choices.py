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


class DegreeProgram(models.TextChoices):
    SHS = "SHS", "Senior High School"
    BAC = "BAC", "Bachelor of Arts in Communication"
    BAELS = "BAELS", "Bachelor of Arts in English Language Studies"
    BCAED = "BCAEd", "Bachelor of Culture and Arts Education"
    BEED = "BEEd", "Bachelor of Elementary Education"
    BSENTREP = "BSEntrep", "Bachelor of in Science in Entrepreneurship"
    BPA = "BPA", "Bachelor of Public Administration"
    BSA = "BSA", "Bachelor of Science in Accountancy"
    BSBA = "BSBA", "Bachelor of Science in Business Administration"
    BSCE = "BSCE", "Bachelor of Science in Civil Engineering"
    BSCPE = "BSCpE", "Bachelor of Science in Computer Engineering"
    BSCRIM = "BSCrim", "Bachelor of Science in Criminology"
    BSEE = "BSEE", "Bachelor of Science in Electrical Engineering"
    BSECE = "BSECE", "Bachelor of Science in Electronics and Communications Engineering"
    BSES = "BSES", "Bachelor of Science in Environmental Science"
    BSIT = "BSIT", "Bachelor of Science in Industrial Technology"
    BSIS = "BSIS", "Bachelor of Science in Information Systems"
    BSINFOTECH = "BSI/T", "Bachelor of Science in Information Technology"
    BSME = "BSME", "Bachelor of Science in Mechanical Engineering"
    BSM = "BSM", "Bachelor of Science in Midwifery"
    BSN = "BSN", "Bachelor of Science in Nursing"
    BSSW = "BSSW ", "Bachelor of Science in Social Work"
    BSED = "BSEd", "Bachelor of Secondary Education"
    BTLED = "BTLEd", "Bachelor of Technology and Livelihood Education"


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
