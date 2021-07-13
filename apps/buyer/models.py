from django.db import models


# Create your models here.

class Buyer(models.Model):
    id_in_bank = models.CharField(max_length=10)
    password_in_bank = models.CharField(max_length=100)
