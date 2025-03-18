
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Task Model
class Task(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title