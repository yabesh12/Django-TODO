from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

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
    mobile_no = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


PAYMENT_STATUS = (
    ("SUCCESS", "Success"),
    ("FAILURE", "Failure"),
    ("PENDING", "Pending"),
)


# class Order(models.Model):
#     name = models.CharField(max_length=200, blank=True, null=True)
#     amount = models.PositiveIntegerField(blank=True)
#     status = models.CharField(max_length=200, choices=PAYMENT_STATUS, default="PENDING", blank=True, null=True)
#     order_id = models.CharField(max_length=250, null=True, blank=True)
#     payment_id = models.CharField(max_length=250, null=True, blank=True)
#
#     def __str__(self):
#         return str(self.name)
