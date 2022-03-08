from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from .managers import CustomUserManager




DEPT_CHOICES = (
    ("IT", "It"),
    ("HR", "Hr"),
    ("TESTING", "Testing"),
)


class Employee(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    mobile_no = models.PositiveIntegerField()
    department = models.CharField(max_length=200, choices=DEPT_CHOICES, default="IT")
    address = models.CharField(max_length=200)
    pincode = models.PositiveIntegerField()

    def __str__(self):
        return str(self.first_name)

    def get_absolute_url(self):
        return reverse('edit_employee', args=[self.id])


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(_('email address'), unique=True)
    city = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
