from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Job(models.Model):
    writer = models.ForeignKey('auth.User')
    email = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    category = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    description = models.TextField()
    companyName = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title