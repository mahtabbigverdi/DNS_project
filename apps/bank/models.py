from django.db import models


# Create your models here.
class Customer(models.Model):
    id_in_bank = models.CharField(max_length=10, null=False, blank=False, editable=False)
    password = models.CharField(max_length=100)
    balance = models.CharField(max_length=10, default=0)
    last_transaction_amount = models.IntegerField(default=0)

