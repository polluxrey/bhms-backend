from django.db import models

# Create your models here.


class BrandingConfig(models.Model):
    app_name = models.CharField(
        max_length=100, default="Boarding House Management System")
    logo = models.ImageField(upload_to="assets/", null=True, blank=True)
    favicon = models.ImageField(upload_to="assets/", null=True, blank=True)
    theme_color = models.CharField(max_length=20, null=True, blank=True)
    background_color = models.CharField(max_length=20, null=True, blank=True)
    font_family = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and BrandingConfig.objects.exists():
            raise ValueError("Only one branding config instance allowed.")

        return super().save(*args, **kwargs)

    @classmethod
    def get_app_name(cls):
        instance = cls.objects.first()
        return instance.app_name if instance else "Boarding House Management System"

    def __str__(self):
        return "Branding config added!"


class ContactConfig(models.Model):
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and ContactConfig.objects.exists():
            raise ValueError("Only one contact config instance allowed.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Contact config added!"


class FeatureToggle(models.Model):
    maintenance_mode = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and FeatureToggle.objects.exists():
            raise ValueError("Only one feature toggle instance allowed.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Feature toggle added!"
