from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=300)
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Company Admin'),
        ('user', 'User'),

    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    class Meta:
        verbose_name = "Foydalanuvchilar_"




