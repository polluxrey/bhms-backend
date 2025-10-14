from django.db import models

# Create your models here.


class Module(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    image = models.ImageField(
        upload_to='assets/',
        blank=True,
        null=True,
    )
    redirect_url = models.CharField(max_length=50, unique=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
