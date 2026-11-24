from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('General Physician', 'General Physician'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doctors'
    )
    name = models.CharField(max_length=150)
    specialization = models.CharField(
        max_length=100,
        choices=SPECIALIZATION_CHOICES
    )
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name