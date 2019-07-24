from django.conf import settings
from django.db import models

# Create your models here.
from django.utils import timezone


class Poll(models.Model):
    CREATED = 'Created'
    ACTIVE = 'Active'
    FINISHED = 'Finished'
    STATUS = (
        (CREATED, 'Created'),
        (ACTIVE, 'Active'),
        (FINISHED, 'Finished'),
    )
    name = models.CharField(max_length=200)
    max_votes = models.IntegerField(default=0)
    description = models.TextField(default=None)
    start = models.DateTimeField('start date')
    expiration = models.DateTimeField('expiration date')
    status = models.CharField(max_length=20, choices=STATUS, default=CREATED)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Voter(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
