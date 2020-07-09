from django.db import models
from django.contrib.auth.models import User

ROLES = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
        ('SuperUser', 'SuperUser'),
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, null=False, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
