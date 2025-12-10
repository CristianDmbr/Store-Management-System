from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('almost_done', 'Almost Done')
    ]
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default = False)
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'not_started'
    )

    def __str__(self):
        return self.title