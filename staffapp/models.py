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

class Profile(models.Model):
    user = models.ForeignKey('auth.User')
    age = models.IntegerField()
    role = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user.username


REQUEST_STATUS_CHOICES= (
    ('WT', 'Wait'),
    ('AC', 'Accept'),
    ('DE', 'Decline'),
)
class Requestjob(models.Model):
    user = models.ForeignKey('auth.User')
    job = models.ForeignKey('Job')
    status = models.CharField(max_length=9, choices=REQUEST_STATUS_CHOICES, default="WT")
    processed = models.BooleanField(default =0)
    
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return 'request '+self.job.title+' of '+self.user.username