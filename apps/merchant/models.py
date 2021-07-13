from django.db import models


# Create your models here.

class Merchant(models.Model):
    id_in_bank = models.CharField(max_length=10, null=False, blank=False)
    password_in_bank = models.CharField(max_length=100)