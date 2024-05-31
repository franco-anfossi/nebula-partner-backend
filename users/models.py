from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    rut = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    rut = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    company = models.ForeignKey(
        Company,
        related_name="employees",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    employee_type = models.CharField(
        max_length=10,
        choices=(("buyer", "Buyer"), ("seller", "Seller")),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
